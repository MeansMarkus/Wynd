import json
import os
import sys
from typing import Dict, List

from fastapi import FastAPI, WebSocket, WebSocketDisconnect

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from cards.card import Deck
from cards.number import NumberCard
from cards.plus_two import PlusTwoCard
from cards.reverse import ReverseCard
from game.board import Board
from game.game_state import GameState
from game.turn_manager import TurnManager
from players.player import Player


app = FastAPI()


class ConnectionManager:
    def __init__(self):
        self.active: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active:
            self.active.remove(websocket)

    async def broadcast(self, message: Dict):
        for ws in list(self.active):
            await ws.send_text(json.dumps(message))


def build_deck():
    cards = []
    cards.extend(ReverseCard() for _ in range(2))
    cards.extend(PlusTwoCard() for _ in range(3))
    for number in range(1, 6):
        cards.extend(NumberCard(number) for _ in range(2))
    return Deck(cards)


board = Board()
board.setup_initial()
players = [Player("White", "white"), Player("Black", "black")]
turn_manager = TurnManager(players)
deck = build_deck()
state = GameState(board, players, turn_manager, deck)
turn_started = True
manager = ConnectionManager()


def ensure_turn_start():
    global turn_started
    if not turn_started:
        return
    current = turn_manager.current_player()
    if len(current.hand) < 5:
        current.draw(deck)
    state.moves_left = 1
    turn_started = False


def serialize_state():
    ensure_turn_start()
    current = turn_manager.current_player()
    turn = current.color
    is_checkmate = board.is_checkmate(turn)
    winner = "white" if turn == "black" else "black"
    return {
        "fen": board.to_fen(turn),
        "turn": turn,
        "moves_left": state.moves_left,
        "hand": [str(card) for card in current.hand],
        "opponent_hand_count": len(players[0].hand) if current is players[1] else len(players[1].hand),
        "deck_count": len(deck.draw_pile),
        "discard_top": str(deck.discard_pile[-1]) if deck.discard_pile else None,
        "move_history": board.move_history,
        "check": board.is_in_check(turn),
        "checkmate": is_checkmate,
        "winner": winner if is_checkmate else None,
    }


def apply_move(start: str, end: str):
    global turn_started
    ensure_turn_start()
    current = turn_manager.current_player()
    board.move_piece(start, end, current.color)
    state.moves_left -= 1
    if state.moves_left <= 0:
        turn_manager.advance()
        turn_started = True


def apply_card(index: int):
    ensure_turn_start()
    current = turn_manager.current_player()
    current.play_card(index, state)


@app.get("/state")
async def get_state():
    return serialize_state()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        await websocket.send_text(json.dumps({"type": "state", "state": serialize_state()}))
        while True:
            raw = await websocket.receive_text()
            data = json.loads(raw)
            if data.get("type") == "move":
                apply_move(data.get("start"), data.get("end"))
            elif data.get("type") == "play_card":
                apply_card(int(data.get("index")))
            await manager.broadcast({"type": "state", "state": serialize_state()})
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as exc:
        await websocket.send_text(json.dumps({"type": "error", "message": str(exc)}))
        manager.disconnect(websocket)
