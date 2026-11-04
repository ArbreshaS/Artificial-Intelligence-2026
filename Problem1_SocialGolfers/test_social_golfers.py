
import unittest

from social_golfers import (
    SocialGolfersDFS,
    is_valid,
    objective,
    upper_bound,
)


class TestSocialGolfers(unittest.TestCase):

    def test_search_without_time_limit(self):
        solver = SocialGolfersDFS(3, 3, 4, None)
        schedule, status = solver.solve()
        self.assertEqual(status, "found")
        self.assertTrue(is_valid(schedule, 3, 3))

    def test_bound_without_time_limit(self):
        schedule, status = SocialGolfersDFS(8, 4, 11, None).solve()
        self.assertIsNone(schedule)
        self.assertEqual(status, "impossible_by_bound")

    def test_timeout_keeps_valid_partial_schedule(self):
        solver = SocialGolfersDFS(8, 4, 9, 0.001)
        schedule, status = solver.solve()
        self.assertEqual(status, "timeout")
        self.assertIsNone(schedule)
        self.assertTrue(is_valid(solver.best_schedule, 8, 4))
        self.assertLess(len(solver.best_schedule), 9)

    # Test 1: Kufiri teorik i javeve
    def test_upper_bound(self):
        self.assertEqual(upper_bound(8, 4), 10)
        self.assertEqual(upper_bound(3, 3), 4)

    # Test 2: Orar pa cifte te perseritura
    def test_objective_valid(self):
        schedule = [
            [[0, 1], [2, 3]],
            [[0, 2], [1, 3]]
        ]
        self.assertEqual(objective(schedule), 0)

    # Test 3: Orar me cifte te perseritura
    def test_objective_invalid(self):
        schedule = [
            [[0, 1], [2, 3]],
            [[0, 1], [2, 3]]
        ]
        self.assertEqual(objective(schedule), 2)

    # Test 4: Kontrollimi i orarit valid
    def test_valid_schedule(self):
        schedule = [
            [[0, 1], [2, 3]]
        ]
        self.assertTrue(is_valid(schedule, 2, 2))

    # Test 5: Kontrollimi i orarit invalid
    def test_invalid_schedule(self):
        schedule = [
            [[0, 1], [2, 3]],
            [[0, 1], [2, 3]]
        ]
        self.assertFalse(is_valid(schedule, 2, 2))

    # Test 6: DFS me 9 lojtare
    def test_dfs_small(self):
        solver = SocialGolfersDFS(3, 3, 4, 10)
        schedule, status = solver.solve()

        self.assertEqual(status, "found")
        self.assertTrue(is_valid(schedule, 3, 3))
        self.assertEqual(objective(schedule), 0)

    # Test 7: DFS me 32 lojtare
    def test_dfs_standard(self):
        solver = SocialGolfersDFS(8, 4, 3, 10)
        schedule, status = solver.solve()

        self.assertEqual(status, "found")
        self.assertTrue(is_valid(schedule, 8, 4))
        self.assertEqual(objective(schedule), 0)

    # Test 8: Tejkalimi i kufirit teorik
    def test_impossible_weeks(self):
        solver = SocialGolfersDFS(8, 4, 11, 10)
        schedule, status = solver.solve()

        self.assertIsNone(schedule)
        self.assertEqual(status, "impossible_by_bound")


if __name__ == "__main__":
    unittest.main()
