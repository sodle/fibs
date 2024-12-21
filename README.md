# Fibs

Like _Threes_ or _2048_ but it's the Fibonacci numbers instead.

## Requirements

- Python 3.12+
- Poetry

## Install

```python
poetry install
```

## Play

- Run `fibs`
- Arrow keys or WASD to move tiles
- Tiles will only join if they are adjacent in the Fibonacci sequence: `1, 1, 2, 3, 5, 8, 13, 21, 34, ...`
- Any movement will also add a new `1` tile in a random empty space
- Fill the board, and you lose
