import React, { useEffect, useMemo, useState } from "react";
import { sendWsMessage } from "./api.js";

const WS_URL = "ws://localhost:8000/ws";

const fileLetters = "abcdefgh";

function parseFenBoard(fen) {
  if (!fen) return [];
  const rows = fen.split(" ")[0].split("/");
  return rows.map((row) => {
    const cells = [];
    for (const ch of row) {
      if (ch >= "1" && ch <= "8") {
        const count = parseInt(ch, 10);
        for (let i = 0; i < count; i += 1) cells.push(null);
      } else {
        cells.push(ch);
      }
    }
    return cells;
  });
}

function coordsToSquare(row, col) {
  return `${fileLetters[col]}${8 - row}`;
}

export default function App() {
  const [state, setState] = useState(null);
  const [socketStatus, setSocketStatus] = useState("connecting");
  const [selectedSquare, setSelectedSquare] = useState(null);
  const [selectedCard, setSelectedCard] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    const socket = new WebSocket(WS_URL);
    socket.onopen = () => setSocketStatus("connected");
    socket.onclose = () => setSocketStatus("disconnected");
    socket.onerror = () => setSocketStatus("error");
    socket.onmessage = (event) => {
      const payload = JSON.parse(event.data);
      if (payload.type === "state") {
        setState(payload.state);
        setError(null);
      } else if (payload.type === "error") {
        setError(payload.message);
      }
    };
    return () => socket.close();
  }, []);

  const board = useMemo(() => parseFenBoard(state?.fen), [state]);

  const playCard = () => {
    if (selectedCard == null) return;
    sendWsMessage({ type: "play_card", index: selectedCard });
  };

  const sendMove = (from, to) => sendWsMessage({ type: "move", start: from, end: to });

  const handleSquareClick = (row, col) => {
    if (!state || state.checkmate) return;
    const square = coordsToSquare(row, col);
    if (!selectedSquare) {
      setSelectedSquare(square);
      return;
    }
    if (selectedSquare === square) {
      setSelectedSquare(null);
      return;
    }
    sendMove(selectedSquare, square);
    setSelectedSquare(null);
  };

  if (!state) {
    return (
      <div className="loading">
        <h1>Chaos Chess</h1>
        <p>Connecting...</p>
      </div>
    );
  }

  return (
    <div className="app">
      <header className="top-bar">
        <div>
          <h1>Chaos Chess</h1>
          <p className="subtitle">Chaos meets strategy</p>
        </div>
        <div className="status">
          <span className={`pill ${state.turn}`}>Turn: {state.turn}</span>
          <span className="pill">Moves left: {state.moves_left}</span>
          {state.check && <span className="pill danger">Check</span>}
          {state.checkmate && (
            <span className="pill danger">Checkmate: {state.winner} wins</span>
          )}
        </div>
      </header>

      <main className="layout">
        <section className="board">
          {board.map((row, r) => (
            <div key={r} className="board-row">
              {row.map((cell, c) => {
                const isDark = (r + c) % 2 === 1;
                const square = coordsToSquare(r, c);
                return (
                  <button
                    key={c}
                    className={`square ${isDark ? "dark" : "light"} ${
                      selectedSquare === square ? "selected" : ""
                    }`}
                    onClick={() => handleSquareClick(r, c)}
                  >
                    <span className={`piece ${cell ? (cell === cell.toUpperCase() ? "white" : "black") : ""}`}>
                      {cell || ""}
                    </span>
                  </button>
                );
              })}
            </div>
          ))}
        </section>

        <aside className="sidebar">
          <div className="panel">
            <h2>Status</h2>
            <p>Socket: {socketStatus}</p>
            {error && <p className="error">{error}</p>}
            <p>Deck: {state.deck_count}</p>
            <p>Discard: {state.discard_top || "-"}</p>
            <p>Opponent hand: {state.opponent_hand_count}</p>
          </div>

          <div className="panel">
            <h2>Moves</h2>
            <ol>
              {state.move_history.slice(-8).map((move, idx) => (
                <li key={idx}>{move.start}-{move.end}</li>
              ))}
            </ol>
          </div>
        </aside>
      </main>

      <section className="tray">
        <div className="tray-header">
          <h2>Your Hand</h2>
          <button className="play" onClick={playCard} disabled={selectedCard == null}>
            Play Card
          </button>
        </div>
        <div className="cards">
          {state.hand.map((card, idx) => (
            <button
              key={`${card}-${idx}`}
              className={`card ${selectedCard === idx ? "selected" : ""}`}
              onClick={() => setSelectedCard(idx)}
            >
              <span>{card}</span>
            </button>
          ))}
        </div>
      </section>
    </div>
  );
}
