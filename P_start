from dataclasses import dataclass
from typing import List, Tuple, Dict

@dataclass(frozen=True)
class WordPlacement:
    word: str
    row: int
    col: int
    direction: str  # "across" or "down"
    clue: str

def build_puzzle() -> Tuple[List[List[str]], List[List[bool]], List[WordPlacement]]:
    """
    Grid 10x10.
    Words:
      - JAZMIN (across)
      - MEPERDONAS (down) intersects at 'A' (JAZMIN[1]) == 'A' (MEPERDONAS[5])
    """
    size = 10
    grid = [[" " for _ in range(size)] for _ in range(size)]
    is_block = [[False for _ in range(size)] for _ in range(size)]

    # Mark everything as block first, then carve a plus-shaped corridor
    for r in range(size):
        for c in range(size):
            is_block[r][c] = True

    # Across corridor (row 4, cols 1..6)
    for c in range(1, 7):
        is_block[4][c] = False

    # Down corridor (col 2, rows 0..9)
    for r in range(0, 10):
        is_block[r][2] = False

    # Place words
    placements: List[WordPlacement] = []

    # JAZMIN across at row 4 col 1
    w1 = "JAZMIN"
    r1, c1 = 4, 1
    for i, ch in enumerate(w1):
        grid[r1][c1 + i] = ch
    placements.append(
        WordPlacement(
            word=w1,
            row=r1,
            col=c1,
            direction="across",
            clue="1 Horizontal: Su nombre (6 letras)."
        )
    )

    # MEPERDONAS down at row 0 col 2
    w2 = "MEPERDONAS"
    r2, c2 = 0, 2
    # Intersects at (row 4, col 2) which is w1[1] = 'A'
    # For w2, index 4? Let's check: M E P E R D O N A S
    # index:0 1 2 3 4 5 6 7 8 9
    # Want 'A' at row 4 -> index 4 => that's 'R'. Not good.
    # We'll instead set intersection so that w2 index 4 aligns with row 4; so w2[4] must be 'A'.
    # But w2[8] is 'A'. Align index 8 with row 4 => start row = 4 - 8 = -4 (invalid).
    # Better: choose down word "MEPERDONAS" but intersect at 'M' maybe.
    # Let's adjust: intersect at 'M' = w1[4] is 'I' (no).
    # We'll redesign intersection to be valid by shifting w1 row/col.

    # --- Rebuild with valid intersection:
    # Put JAZMIN across at row 5 col 2, so 'M' is at col 6.
    # Put MEPERDONAS down at row 0 col 6, so it intersects at row 5 with w2[5]='D' (still mismatch).
    # Instead, intersect at 'N' maybe: JAZMIN has 'N' at index 5.
    # For MEPERDONAS, 'N' is at index 7. If intersection row is 4, start row = 4 - 7 = -3 invalid.
    #
    # Simpler: keep a clean puzzle: don't force intersection; place words separately.

    # Clear previous placements and re-place without intersection:
    # Reset grid letters on carved cells
    for r in range(size):
        for c in range(size):
            grid[r][c] = " "

    placements.clear()

    # Carve a second across corridor for MEPERDONAS? We'll keep it down in col 2 and place JAZMIN across row 8
    # Adjust corridors
    for r in range(size):
        for c in range(size):
            is_block[r][c] = True

    # Down corridor (MEPERDONAS) at col 2 rows 0..9
    for r in range(0, 10):
        is_block[r][2] = False

    # Across corridor (JAZMIN) at row 8 cols 3..8
    for c in range(3, 9):
        is_block[8][c] = False

    # Place MEPERDONAS down at (0,2)
    w2 = "MEPERDONAS"  # 10 letters
    for i, ch in enumerate(w2):
        grid[0 + i][2] = ch
    placements.append(
        WordPlacement(
            word=w2,
            row=0,
            col=2,
            direction="down",
            clue="1 Vertical: Dos palabras juntas: lo que quiero pedirte (10 letras, sin espacio)."
        )
    )

    # Place JAZMIN across at (8,3)
    w1 = "JAZMIN"
    for i, ch in enumerate(w1):
        grid[8][3 + i] = ch
    placements.append(
        WordPlacement(
            word=w1,
            row=8,
            col=3,
            direction="across",
            clue="2 Horizontal: La persona que más quiero (6 letras)."
        )
    )

    return grid, is_block, placements

def solution_letter_at(grid: List[List[str]], r: int, c: int) -> str:
    return grid[r][c]

def is_cell_playable(is_block: List[List[bool]], r: int, c: int) -> bool:
    return not is_block[r][c]

