"""Sudoku solved by breadth-first search over partial boards."""

from collections import deque

# 0 represents an empty cell.
PUZZLES = {
    "Easy": "530070000600195000098000060800060003400803001700020006060000280000419005000080079",
    "Medium": "000260701680070090190004500820100040004602900050003028009300074040050036703018000",
    "Hard": "000000907000420180000705026100904000050000040000507009920108000034059000507000000",
}
DIGITS = set(range(1, 10))


def parse(text):
    """Convert an 81-character puzzle into an immutable board."""
    text = ''.join(text.split())
    if len(text) != 81 or any(c not in '0123456789' for c in text):
        raise ValueError("Enter exactly 81 digits; use 0 for empty cells.")
    board = tuple(map(int, text))
    if not valid(board):
        raise ValueError("The given clues conflict.")
    return board


def units():
    rows = [[r * 9 + c for c in range(9)] for r in range(9)]
    cols = [[r * 9 + c for r in range(9)] for c in range(9)]
    boxes = [[(br + dr) * 9 + bc + dc for dr in range(3) for dc in range(3)]
             for br in (0, 3, 6) for bc in (0, 3, 6)]
    return rows + cols + boxes


UNITS = units()
PEERS = [set(j for unit in UNITS if i in unit for j in unit if j != i)
         for i in range(81)]


def valid(board):
    if len(board) != 81 or any(not isinstance(x, int) or x not in range(10) for x in board):
        return False
    for unit in UNITS:
        values = [board[i] for i in unit if board[i] != 0]
        if len(values) != len(set(values)):
            return False
    return True


def candidates(board, index):
    return DIGITS - {board[i] for i in PEERS[index]}


def objective(board):
    """Count empty cells plus duplicate entries in each row, column and box."""
    conflicts = 0
    for unit in UNITS:
        values = [board[i] for i in unit if board[i]]
        conflicts += len(values) - len(set(values))
    return board.count(0) + conflicts


def solve(board, max_states=200000):
    """BFS; discard inconsistent branches (backtracking/pruning).

    Returns (solution, status, visited). A limit is not a proof of impossibility.
    """
    if not valid(board):
        raise ValueError("Invalid board or conflicting clues.")
    if max_states < 1:
        raise ValueError("max_states must be positive.")
    queue = deque([tuple(board)])
    visited = 0
    while queue:
        if visited >= max_states:
            return None, "limit", visited
        current = queue.popleft()
        visited += 1
        empty = [i for i, value in enumerate(current) if value == 0]
        if not empty:
            return current, "solved", visited
        # MRV only chooses which cell to expand; the queue remains FIFO BFS.
        choices = [(candidates(current, i), i) for i in empty]
        options, index = min(choices, key=lambda item: len(item[0]))
        for value in sorted(options):
            child = list(current)
            child[index] = value
            queue.append(tuple(child))
    return None, "no_solution", visited


def format_board(board):
    return '\n'.join(' '.join(str(x) if x else '.' for x in board[r:r+9])
                     for r in range(0, 81, 9))


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Solve Sudoku using BFS")
    parser.add_argument("--level", choices=PUZZLES, default="Easy")
    parser.add_argument("--max-states", type=int, default=200000)
    args = parser.parse_args()
    start = parse(PUZZLES[args.level])
    print("Puzzle:\n" + format_board(start))
    solution, status, visited = solve(start, args.max_states)
    print(f"\nStatus: {status}; visited states: {visited}")
    if solution:
        print(format_board(solution))
