import unittest

from sudoku import PUZZLES, objective, parse, solve, valid
from landscape import analyze


class TestSudoku(unittest.TestCase):
    def test_landscape_samples_are_reproducible(self):
        scores, changes = analyze('Easy', 20, 42)
        self.assertEqual((scores, changes), analyze('Easy', 20, 42))
        self.assertEqual(len(scores), 20)
        self.assertEqual(sum(changes.values()), 20)
    def test_levels(self):
        for level, text in PUZZLES.items():
            with self.subTest(level=level):
                original = parse(text)
                result, status, _ = solve(original)
                self.assertEqual(status, "solved")
                self.assertTrue(valid(result))
                self.assertEqual(objective(result), 0)
                self.assertTrue(all(not clue or result[i] == clue for i, clue in enumerate(original)))

    def test_invalid_clues(self):
        with self.assertRaises(ValueError):
            parse('11' + '0' * 79)

    def test_invalid_input(self):
        with self.assertRaises(ValueError):
            parse('123')

    def test_limit_is_not_no_solution(self):
        result, status, _ = solve(parse(PUZZLES['Easy']), max_states=1)
        self.assertIsNone(result)
        self.assertEqual(status, 'limit')

    def test_impossible_board(self):
        board = parse('123456780' + '000000009' + '0' * 63)
        result, status, _ = solve(board)
        self.assertIsNone(result)
        self.assertEqual(status, 'no_solution')


if __name__ == '__main__':
    unittest.main()
