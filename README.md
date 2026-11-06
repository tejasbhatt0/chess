# Pygame Chess: Object-Oriented Rules Engine

A fully playable, local two-player chess application built in Python. This project serves as a complete rules engine, strictly enforcing all complex board states, move validations, and edge cases in real-time.

![Gameplay Demo](link-to-your-gif-or-screenshot.gif)

## ⚙️ Tech Stack
- **Language:** Python 3
- **Graphics & Event Loop:** Pygame
- **Architecture:** Object-Oriented Programming (OOP)

## ♟️ Features & Rule Enforcement
The engine accurately calculates and enforces standard FIDE rules without relying on external chess libraries:
- [x] Piece-specific pseudo-legal move generation
- [x] Absolute and relative pin detection (preventing moving into check)
- [x] En Passant captures
- [x] Kingside and Queenside Castling (with line-of-sight and check validation)
- [x] Pawn Promotion
- [x] Checkmate and Stalemate detection

## 🧠 Under the Hood (Architecture)
The application relies on a modular OOP structure to separate the game logic from the graphical interface:
* **State Management:** A central `GameState` class logs the move history, tracks whose turn it is, and generates the legal move tree for the current board state.
* **Class Inheritance:** Standardized piece behaviors are inherited from a base `Piece` class, keeping move-generation logic cleanly isolated for sliding pieces (Rooks, Bishops, Queens) versus stepping pieces (Knights, Kings).
* **Event Handling:** The Pygame loop runs completely decoupled from the board math, mapping pixel-coordinate mouse clicks to the internal 8x8 2D array representation of the board.

## 🚀 Quick Start

### Prerequisites
Make sure you have Python installed, along with the Pygame library:
```bash
pip install pygame
