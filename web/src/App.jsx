import React, { useEffect, useMemo, useRef, useState } from "react";
import wpawn from "./assets/pieces/wpawn.svg";
import wrook from "./assets/pieces/wrook.svg";
import wknight from "./assets/pieces/wknight.svg";
import wbishop from "./assets/pieces/wbishop.svg";
import wqueen from "./assets/pieces/wqueen.svg";
import wking from "./assets/pieces/wking.svg";
import bpawn from "./assets/pieces/bpawn.svg";
import brook from "./assets/pieces/brook.svg";
import bknight from "./assets/pieces/bknight.svg";
import bbishop from "./assets/pieces/bbishop.svg";
import bqueen from "./assets/pieces/bqueen.svg";
import bking from "./assets/pieces/bking.svg";

const WS_URL = "ws://localhost:8000/ws";

const fileLetters = "abcdefgh";

const pieceMap = {
  P: wpawn,
  R: wrook,
  N: wknight,
  B: wbishop,
  Q: wqueen,
  K: wking,
  p: bpawn,
  r: brook,
  n: bknight,
  b: bbishop,
  q: bqueen,
  k: bking
};

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
  const [dragging, setDragging] = useState(null);
  const [dragPos, setDragPos] = useState({ x: 0, y: 0 });
  const socketRef = useRef(null);
  const boardRef = useRef(null);

  useEffect(() => {
    const socket = new WebSocket(WS_URL);
    socketRef.current = socket;
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

  const sendMessage = (message) => {
    const socket = socketRef.current;
    if (!socket || socket.readyState !== WebSocket.OPEN) {
      setError("WebSocket not connected");
      return;
    }
    socket.send(JSON.stringify(message));
  };

  const playCard = () => {
    if (selectedCard == null) return;
    sendMessage({ type: "play_card", index: selectedCard });
  };

  const sendMove = (from, to) => sendMessage({ type: "move", start: from, end: to });

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

  const squareFromPoint = (x, y) => {
    const rect = boardRef.current?.getBoundingClientRect();
    if (!rect) return null;
    const size = rect.width / 8;
    const col = Math.floor((x - rect.left) / size);
    const row = Math.floor((y - rect.top) / size);
    if (row < 0 || col < 0 || row > 7 || col > 7) return null;
    return { row, col, square: coordsToSquare(row, col) };
  };

  const handlePointerDown = (row, col, cell, event) => {
    if (!state || state.checkmate || !cell) return;
    const isWhite = cell === cell.toUpperCase();
    if ((state.turn === "white" && !isWhite) || (state.turn === "black" && isWhite)) {
      return;
    }
    event.currentTarget.setPointerCapture(event.pointerId);
    setDragging({ from: coordsToSquare(row, col), piece: cell, start: { x: event.clientX, y: event.clientY } });
    setDragPos({ x: event.clientX, y: event.clientY });
  };

  const handlePointerMove = (event) => {
    if (!dragging) return;
    setDragPos({ x: event.clientX, y: event.clientY });
  };

  const handlePointerUp = (event) => {
    if (!dragging) return;
    const target = squareFromPoint(event.clientX, event.clientY);
    if (target && target.square !== dragging.from) {
      sendMove(dragging.from, target.square);
    } else if (target && target.square === dragging.from) {
      setSelectedSquare(dragging.from);
    }
    setDragging(null);
  };

  useEffect(() => {
    if (!dragging) return undefined;
    const onMove = (event) => handlePointerMove(event);
    const onUp = (event) => handlePointerUp(event);
    window.addEventListener("pointermove", onMove);
    window.addEventListener("pointerup", onUp);
    return () => {
      window.removeEventListener("pointermove", onMove);
      window.removeEventListener("pointerup", onUp);
    };
  }, [dragging]);

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
        <section className="board" ref={boardRef}>
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
                    onPointerDown={(event) => handlePointerDown(r, c, cell, event)}
                    onPointerUp={handlePointerUp}
                  >
                    {cell && (
                      <img
                        className={`piece-img ${cell === cell.toUpperCase() ? "white" : "black"}`}
                        src={pieceMap[cell]}
                        alt={cell}
                      />
                    )}
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

          <div className="panel moves">
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

      {dragging && (
        <img
          className="drag-ghost"
          src={pieceMap[dragging.piece]}
          alt="dragging"
          style={{ left: dragPos.x, top: dragPos.y }}
        />
      )}
    </div>
  );
}
