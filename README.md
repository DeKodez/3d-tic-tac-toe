# 3D Tic-Tac-Toe

A 2-player local game with 6 independent 3×3 tic-tac-toe faces. Players alternate turns placing X or O on any unlocked face. A face locks when won or drawn. The game ends when all 6 faces are resolved — the player with the most face wins takes the game.

<img width="694" height="568" alt="image" src="https://github.com/user-attachments/assets/05ef94d9-c1ed-405d-bd23-320803adc387" />


## Setup

```
pip install -r requirements.txt
python main.py
```

## Rules

- Player X goes first. Turns alternate globally.
- On your turn, pick any unlocked face and place your mark.
- Win a face by getting 3-in-a-row (row, column, or diagonal).
- A full face with no winner is a draw — no points awarded.
- Most face wins at the end takes the game. Ties are possible.
- **Nukes** (optional) — each player gets one nuke per game. Using it wipes the current board clean and costs a turn. Can only target in-progress boards. Enable on the start screen.

## Attribution

- <a href="https://www.flaticon.com/free-icons/nuke" title="nuke icons">Nuke icons created by heisenberg_jr - Flaticon</a>