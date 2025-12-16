import random
import string
from dataclasses import dataclass
from typing import List, Tuple

@dataclass(frozen=True)
class WordPlacement:
    word: str
    positions: list  # list of (row, col)
    clue: str

GRID_SIZE = 12

def random_letter():
    return random.choice(string.ascii_uppercase)

def place_word(grid, positions, word):
    # Coloca letras y valida cruces
    for (r, c), ch in zip(positions, word):
        existing = grid[r][c]
        if existing not in ("", ch):
            return False
    for (r, c), ch in zip(positions, word):
        grid[r][c] = ch
    return True

def build_puzzle() -> Tuple[List[List[str]], List[List[bool]], List[WordPlacement]]:
    grid = [["" for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    is_block = [[False for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    placements: List[WordPlacement] = []

    # PERDON (diagonal escondida)
    perdon_pos = [(1, 9), (2, 8), (3, 7), (4, 6), (5, 5), (6, 4)]
    place_word(grid, perdon_pos, "PERDON")
    placements.append(
        WordPlacement(
            word="PERDON",
            positions=perdon_pos,
            clue="1️⃣ Diagonal: Lo que digo sin excusas."
        )
    )

    # JAZMIN (vertical, lejos de PERDON)
    jazmin_pos = [(0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1)]
    place_word(grid, jazmin_pos, "JAZMIN")
    placements.append(
        WordPlacement(
            word="JAZMIN",
            positions=jazmin_pos,
            clue="2️⃣ Vertical: Tu nombre."
        )
    )

    # TEAMO (en L para hacerlo más difícil)
    # T E A (horizontal) y M O (vertical)
    teamo_pos = [(9, 8), (9, 9), (9,10), (10,10), (11,10)]
    place_word(grid, teamo_pos, "TEAMO")
    placements.append(
        WordPlacement(
            word="TEAMO",
            positions=teamo_pos,
            clue="3️⃣ Forma rara: Lo que siento, aunque me equivoqué."
        )
    )

    # Relleno random
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            if grid[r][c] == "":
                grid[r][c] = random_letter()

    return grid, is_block, placements

