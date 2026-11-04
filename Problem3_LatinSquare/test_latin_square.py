import unittest

from latin_square import objective, solve, valid
from landscape import analyze


class TestLatinSquare(unittest.TestCase):
    def test_landscape_samples_are_reproducible(self):
        scores, changes = analyze(5, 20, 42)
        self.assertEqual((scores, changes), analyze(5, 20, 42))
        self.assertEqual(len(scores), 20)
        self.assertEqual(sum(changes.values()), 20)
    def test_sizes(self):
        for n in range(1, 6):
            with self.subTest(n=n):
                square, visited = solve(n)
                self.assertTrue(valid(square))
                self.assertEqual(objective(square), 0)
                self.assertGreater(visited, n * n)

    def test_invalid(self):
        self.assertFalse(valid([[1, 1], [2, 2]]))
        self.assertGreater(objective([[1, 1], [2, 2]]), 0)
        self.assertFalse(valid([[1, 2], [2]]))

    def test_partial_objective(self):
        self.assertEqual(objective([[1, 0], [0, 1]]), 2)

    def test_invalid_size(self):
        for n in (0, -1, 1.5, True):
            with self.subTest(n=n), self.assertRaises(ValueError):
                solve(n)


if __name__ == '__main__':
    unittest.main()
