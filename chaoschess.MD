# Chaos Chess

## Project Overview

Chaos Chess is a strategy game that combines traditional chess mechanics with UNO-inspired card effects.

Players play chess normally, but each turn may involve special cards that alter the rules of the game, manipulate the board, revive pieces, reverse turns, or create chaotic effects.

The goal of this project is to:
- Learn advanced Python
- Practice object-oriented programming
- Build a large-scale software project
- Create a unique portfolio project for SWE internships

---

# Core Technologies

## Initial Stack
- Python 3
- Pygame
- Git/GitHub

## Future Stack
- FastAPI
- PostgreSQL
- WebSockets
- React (optional)

---

# Main Programming Concepts

This project should heavily use:
- Classes
- Objects
- Inheritance
- Polymorphism
- Encapsulation
- Composition
- State management
- Event systems

---

# Core Gameplay Rules

## Base Rules
- Standard chess board
- Standard chess movement
- Turn-based gameplay

## Chaos Rules
Players can draw and play special cards.

Example cards:
- Reverse Turn
- +2 Pieces
- Swap Pieces
- Skip Turn
- Shield Piece
- Wild Move
- Chaos Event

---

# Recommended Folder Structure

```txt
chaos_chess/
│
├── main.py
│
├── game/
│   ├── board.py
│   ├── game_manager.py
│   ├── turn_manager.py
│   ├── game_state.py
│
├── pieces/
│   ├── piece.py
│   ├── pawn.py
│   ├── rook.py
│   ├── bishop.py
│   ├── knight.py
│   ├── queen.py
│   ├── king.py
│
├── cards/
│   ├── card.py
│   ├── reverse_card.py
│   ├── plus_two_card.py
│   ├── swap_card.py
│   ├── skip_card.py
│
├── players/
│   ├── player.py
│
├── ui/
│   ├── renderer.py
│   ├── input_handler.py
│
├── assets/
│   ├── images/
│   ├── sounds/
│
└── utils/
```

---

# Main System Architecture

## Board System

Responsibilities:
- Store piece positions
- Validate moves
- Handle captures
- Track board state

Example:

```python
class Board:
    def move_piece(self, start, end):
        pass
```

---

# Piece System

All pieces inherit from a base Piece class.

Example:

```python
class Piece:
    def valid_moves(self, board):
        pass
```

Derived classes:
- Pawn
- Bishop
- Knight
- Queen
- King
- Rook

---

# Card System

Cards should modify the GAME STATE, not directly manipulate UI.

Base class:

```python
class Card:
    def apply_effect(self, game):
        pass
```

Examples:
- ReverseCard
- PlusTwoCard
- SwapCard
- ShieldCard

This should use polymorphism.

---

# Turn Manager

Responsible for:
- Current player
- Turn order
- Reverse effects
- Skip turns

Example:

```python
class TurnManager:
    def next_turn(self):
        pass
```

---

# Game Manager

Main controller for the game.

Responsibilities:
- Main game loop
- Win conditions
- Applying card effects
- Updating game state

Example:

```python
class GameManager:
    def run(self):
        pass
```

---

# Recommended Development Order

## Phase 1 — Terminal Chess
Goal:
- Fully working chess in terminal

Focus:
- OOP
- Game logic
- Move validation

Do NOT start with graphics.

---

## Phase 2 — Add Card System
Goal:
- Functional card effects

Focus:
- Inheritance
- Polymorphism
- State management

---

## Phase 3 — Pygame UI
Goal:
- Visual board
- Mouse input
- Piece rendering

Focus:
- Event handling
- Rendering systems

---

## Phase 4 — Polish
Add:
- Animations
- Sounds
- Menus
- Piece highlights
- Card animations

---

## Phase 5 — Save System
Features:
- Save/load matches
- Replay system

---

## Phase 6 — AI Opponent
Start simple:
- Random AI

Later:
- Minimax
- Evaluation algorithms

---

## Phase 7 — Multiplayer
Add:
- Online lobbies
- Matchmaking
- WebSocket syncing

Suggested backend:
- FastAPI

---

# Important Design Principles

## 1. Keep Logic Separate From UI
Game logic should work WITHOUT graphics.

Good:
- GameManager handles logic
- Renderer only draws

Bad:
- Pygame code mixed into piece logic

---

## 2. Use Composition When Appropriate

Example:
A Player HAS a Deck.

Not:
Player IS a Deck.

---

## 3. Avoid Massive Classes
If a class becomes too large:
- split responsibilities
- create managers/services

---

## 4. Commit Often
Use GitHub from the beginning.

Commit examples:
- "Added bishop movement validation"
- "Implemented reverse card effect"

---

# Recommended Python Topics To Learn

## Beginner
- Classes
- Methods
- Constructors
- Lists/dictionaries

## Intermediate
- Inheritance
- Encapsulation
- Composition
- Abstract classes

## Advanced
- Design patterns
- Networking
- Concurrency
- Serialization

---

# Future Stretch Features

## Ranked Mode
Track:
- Wins/losses
- ELO rating

## Replay Viewer
Replay entire matches.

## Custom Cards
Allow players to build custom decks.

## Themes
Different:
- Boards
- Pieces
- Sounds

## Steam Release
Potential long-term goal.

---

# Resume Description

Built an original strategy game combining chess and UNO mechanics using Python and object-oriented architecture. Implemented custom game rules, inheritance-based piece systems, card effect engines, game-state management, and interactive UI systems.

---

# Recommended Libraries

## Graphics
- pygame

## Backend
- fastapi

## Database
- sqlalchemy
- psycopg2

## Networking
- websockets

---

# Learning Resources

## Python OOP
Corey Schafer YouTube Playlist

## Pygame
Clear Code YouTube Channel

## Chess Programming
https://www.chessprogramming.org/

---

# Main Goal

This project is NOT just about finishing a game.

The goal is to learn:
- software engineering
- architecture
- debugging
- object-oriented programming
- large project organization

Build slowly.
Do not restart repeatedly.
Focus on consistency and incremental improvement.