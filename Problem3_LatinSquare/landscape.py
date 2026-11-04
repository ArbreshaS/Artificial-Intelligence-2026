"""Sample Latin-square scores and single-cell neighbors (seeded)."""
import argparse
import random
from collections import Counter

from latin_square import objective


def analyze(n=5, samples=500, seed=42):
    if n < 2 or samples < 1:
        raise ValueError('n must be at least 2 and samples must be positive')
    rng = random.Random(seed)
    scores, changes = [], Counter()
    for _ in range(samples):
        square = [[rng.randint(1, n) for _ in range(n)] for _ in range(n)]
        score = objective(square)
        scores.append(score)
        row, col = rng.randrange(n), rng.randrange(n)
        square[row][col] = rng.choice([x for x in range(1, n + 1) if x != square[row][col]])
        delta = objective(square) - score
        changes['better' if delta < 0 else 'worse' if delta > 0 else 'equal'] += 1
    return scores, changes


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--size', type=int, default=5)
    parser.add_argument('--samples', type=int, default=500)
    parser.add_argument('--seed', type=int, default=42)
    args = parser.parse_args()
    scores, changes = analyze(args.size, args.samples, args.seed)
    print(f'Samples: {len(scores)}; min: {min(scores)}; max: {max(scores)}; mean: {sum(scores)/len(scores):.2f}')
    print(f'Histogram: {dict(sorted(Counter(scores).items()))}')
    print(f'Neighbor changes: {dict(changes)}')
