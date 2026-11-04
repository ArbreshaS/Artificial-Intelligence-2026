import unittest

from search_trees import PROBLEMS, build_tree, puzzle_moves, missionaries_moves, solution_path


class TestSearchTrees(unittest.TestCase):
    def test_solution_paths(self):
        expected = {'8-Puzzle': 2, 'Missionaries and Cannibals': 11,
                    'Rotating Workforce Scheduling': 3}
        for name, length in expected.items():
            with self.subTest(problem=name):
                nodes = build_tree(name, 12)
                path = solution_path(name, nodes)
                self.assertIsNotNone(path)
                self.assertEqual(len(path) - 1, length)
                self.assertEqual(path[0][0], PROBLEMS[name]['initial'])
                self.assertTrue(PROBLEMS[name]['goal'](path[-1][0]))
                for (previous, _, _), (current, action, _) in zip(path, path[1:]):
                    self.assertIn((action, current), list(PROBLEMS[name]['moves'](previous)))

    def test_tree_parent_and_unique_states(self):
        for name in PROBLEMS:
            nodes = build_tree(name, 5)
            self.assertEqual(len(nodes), len({node[0] for node in nodes}))
            for index, (state, parent, action, depth) in enumerate(nodes[1:], 1):
                self.assertLess(parent, index)
                self.assertEqual(depth, nodes[parent][3] + 1)
                self.assertIn((action, state), list(PROBLEMS[name]['moves'](nodes[parent][0])))

    def test_moves_and_limit(self):
        self.assertEqual(len(list(puzzle_moves((1, 2, 3, 4, 0, 5, 6, 7, 8)))), 4)
        self.assertTrue(all(m >= 0 and c >= 0 for _, (m, c, _) in missionaries_moves((3, 3, 0))))
        self.assertIsNone(solution_path('Missionaries and Cannibals', build_tree('Missionaries and Cannibals', 10)))
        with self.assertRaises(ValueError):
            build_tree('8-Puzzle', -1)


if __name__ == '__main__':
    unittest.main()
