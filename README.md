# Pygame Chess Environment and Rules Engine

A complete, object-oriented two-player chess application built in Python. This project serves as a strict rules engine, enforcing all complex board states, move validations, and edge cases to function as the foundational testing environment for future algorithmic search and machine learning integration.

![Gameplay Demo](assets/demo.gif)

## Technical Stack
- **Language:** Python 3
- **Graphics & Event Loop:** Pygame
- **Matrix Operations:** NumPy
- **Architecture:** Object-Oriented Programming (OOP)

## Features and Rule Enforcement
The engine accurately calculates and enforces standard FIDE rules without relying on external chess libraries.
- Piece-specific pseudo-legal move generation.
- Absolute and relative pin detection (prevents moving into check via game-state simulation).
- En Passant captures and target tracking.
- Kingside and Queenside Castling (with line-of-sight validation).
- Dynamic Pawn Promotion (features an interactive graphical overlay).
- Checkmate and Stalemate detection.
- Dynamic board flipping and invalid-move visual feedback.

## System Architecture
The application utilizes a modular OOP structure to cleanly separate mathematical game logic from the graphical interface:
- **State Management:** The board state is maintained within an 8x8 2D array. Move validation calculates pseudo-legal moves and simulates them internally to ensure king safety before finalizing the state transition.
- **Class Inheritance:** Standardized piece behaviors are inherited from a base `Piece` class. This keeps move-generation logic strictly isolated for sliding pieces (Rooks, Bishops, Queens) versus stepping pieces (Knights, Kings, Pawns).
- **Decoupled Event Handling:** The Pygame loop runs independently of the board mathematics, translating pixel-coordinate mouse events into array indices and handling asynchronous UI updates without interrupting state logic.

## Installation and Execution

### Prerequisites
Ensure Python 3.x is installed along with the required libraries:
```bash
pip install pygame numpy
