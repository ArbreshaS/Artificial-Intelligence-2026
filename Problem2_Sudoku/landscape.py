"""Sample Sudoku objective scores and single-cell neighbors (seeded)."""
import argparse
import random
from collections import Counter

from sudoku import PUZZLES, objective, parse


def analyze(level='Easy', samples=500, seed=42):
    if samples < 1:
        raise ValueError('samples must be positive')
    rng = random.Random(seed)
    original = parse(PUZZLES[level])
    empty = [i for i, value in enumerate(original) if not value]
    scores, changes = [], Counter()
    for _ in range(samples):
        board = [value or rng.randint(1, 9) for value in original]
        score = objective(board)
        scores.append(score)
        if empty:
            i = rng.choice(empty)
            choices = [x for x in range(1, 10) if x != board[i]]
            board[i] = rng.choice(choices)
            delta = objective(board) - score
            changes['better' if delta < 0 else 'worse' if delta > 0 else 'equal'] += 1
    return scores, changes


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--level', choices=PUZZLES, default='Easy')
    parser.add_argument('--samples', type=int, default=500)
    parser.add_argument('--seed', type=int, default=42)
    args = parser.parse_args()
    scores, changes = analyze(args.level, args.samples, args.seed)
    print(f'Samples: {len(scores)}; min: {min(scores)}; max: {max(scores)}; mean: {sum(scores)/len(scores):.2f}')
    print(f'Histogram: {dict(sorted(Counter(scores).items()))}')
    print(f'Neighbor changes: {dict(changes)}')
