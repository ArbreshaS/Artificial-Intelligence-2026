"""Construct a Latin square using iterative deepening DFS and backtracking."""

import argparse


def objective(square):
    """Count empty cells and duplicate entries in rows and columns."""
    n = len(square)
    empty = sum(value == 0 for row in square for value in row)
    lines = list(square) + [[square[r][c] for r in range(n)] for c in range(n)]
    return empty + sum(len(values) - len(set(values))
                       for line in lines
                       for values in [[value for value in line if value]])


def valid(square):
    n = len(square)
    return (n > 0 and all(len(row) == n for row in square)
            and all(set(row) == set(range(1, n + 1)) for row in square)
            and all({square[r][c] for r in range(n)} == set(range(1, n + 1))
                    for c in range(n)))


def solve(n):
    """Return (square, visited nodes) after depth limits 0 through n².

    Each edge fills exactly one cell. A completed result is copied before
    backtracking restores the board, so no partial changes escape the search.
    """
    if not isinstance(n, int) or isinstance(n, bool) or n < 1:
        raise ValueError("n must be a positive integer")
    board = [[0] * n for _ in range(n)]
    rows = [set() for _ in range(n)]
    columns = [set() for _ in range(n)]
    visited = 0

    def depth_limited(depth, limit):
        nonlocal visited
        visited += 1
        if depth == n * n:
            return [row[:] for row in board]
        if depth == limit:
            return None
        row, col = divmod(depth, n)
        for value in range(1, n + 1):
            # Normalize the first row and column to remove equivalent squares.
            if row == 0 and value != col + 1:
                continue
            if col == 0 and value != row + 1:
                continue
            if value in rows[row] or value in columns[col]:
                continue
            board[row][col] = value
            rows[row].add(value)
            columns[col].add(value)
            result = depth_limited(depth + 1, limit)
            rows[row].remove(value)
            columns[col].remove(value)
            board[row][col] = 0
            if result is not None:
                return result
        return None

    for limit in range(n * n + 1):
        result = depth_limited(0, limit)
        if result is not None:
            return result, visited
    return None, visited


def main():
    parser = argparse.ArgumentParser(description="Latin square using IDDFS and backtracking")
    parser.add_argument("n", nargs="?", type=int, default=3, help="square size (default: 3)")
    args = parser.parse_args()
    try:
        square, visited = solve(args.n)
    except ValueError as error:
        parser.error(str(error))
    for row in square:
        print(' '.join(map(str, row)))
    print(f"Valid: {valid(square)}; objective: {objective(square)}; visited: {visited}")


if __name__ == '__main__':
    main()
