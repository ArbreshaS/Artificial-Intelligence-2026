import argparse
import time
from itertools import combinations


def objective(schedule):
    """Count repeated meetings between pairs of players."""
    meetings = {}
    for week in schedule:
        for group in week:
            for pair in combinations(sorted(group), 2):
                meetings[pair] = meetings.get(pair, 0) + 1
    return sum(max(0, count - 1) for count in meetings.values())


def is_valid(schedule, groups, group_size):
    n = groups * group_size
    if not schedule:
        return False
    for week in schedule:
        if len(week) != groups:
            return False
        if any(len(group) != group_size for group in week):
            return False
        players = [player for group in week for player in group]
        if sorted(players) != list(range(n)):
            return False
    return objective(schedule) == 0


def upper_bound(groups, group_size):
    n = groups * group_size
    if group_size < 2:
        raise ValueError("Group size must be at least 2")
    return (n - 1) // (group_size - 1)


class TimeoutReached(Exception):
    pass


class SocialGolfersDFS:
    def __init__(self, groups=8, group_size=4, weeks=3, timeout=30):
        if groups < 1 or group_size < 2 or weeks < 1 or (timeout is not None and timeout <= 0):
            raise ValueError("Invalid configuration")
        self.groups = groups
        self.group_size = group_size
        self.weeks = weeks
        self.n = groups * group_size
        self.timeout = timeout
        self.schedule = []
        self.used_pairs = set()
        self.nodes = 0
        self.backtracks = 0
        self.best_schedule = []

    def solve(self):
        self.nodes = 0
        self.backtracks = 0
        if self.weeks > upper_bound(self.groups, self.group_size):
            return None, "impossible_by_bound"

        self.start = time.perf_counter()
        first_week = [list(range(i, i + self.group_size))
                      for i in range(0, self.n, self.group_size)]
        self.schedule = [first_week]
        self.best_schedule = [[group[:] for group in first_week]]
        self.used_pairs = {
            pair for group in first_week for pair in combinations(group, 2)
        }
        if self.weeks == 1:
            return self.schedule, "found"
        try:
            if self._dfs(1, [], tuple(range(self.n))):
                return self.schedule, "found"
            return None, "no_solution"
        except TimeoutReached:
            return None, "timeout"

    def _dfs(self, week_index, current_week, available):
        self.nodes += 1
        if self.timeout is not None and time.perf_counter() - self.start > self.timeout:
            raise TimeoutReached

        if not available:
            self.schedule.append([group[:] for group in current_week])
            if len(self.schedule) > len(self.best_schedule):
                self.best_schedule = [[group[:] for group in week] for week in self.schedule]
            if week_index + 1 == self.weeks:
                return True
            if self._dfs(week_index + 1, [], tuple(range(self.n))):
                return True
            self.schedule.pop()
            self.backtracks += 1
            return False

        # Fix the smallest free player as the first member of this group.
        first = available[0]
        for others in combinations(available[1:], self.group_size - 1):
            group = (first,) + others
            pairs = set(combinations(group, 2))
            if not pairs.isdisjoint(self.used_pairs):
                continue

            current_week.append(list(group))
            self.used_pairs.update(pairs)
            chosen = set(group)
            remaining = tuple(x for x in available if x not in chosen)

            if self._dfs(week_index, current_week, remaining):
                return True

            self.used_pairs.difference_update(pairs)
            current_week.pop()

        self.backtracks += 1
        return False


def print_schedule(schedule):
    for week_number, week in enumerate(schedule, start=1):
        print(f"Week {week_number}:")
        for group_number, group in enumerate(week, start=1):
            print(f"  Group {group_number}: {group}")


def main():
    parser = argparse.ArgumentParser(description="Social Golfers using DFS and Backtracking")
    parser.add_argument("--groups", type=int, default=8)
    parser.add_argument("--size", type=int, default=4)
    parser.add_argument("--weeks", type=int, default=3)
    parser.add_argument("--timeout", type=float, default=30)
    args = parser.parse_args()

    solver = SocialGolfersDFS(args.groups, args.size, args.weeks, args.timeout)
    print(f"Players: {solver.n}, groups: {args.groups}, players/group: {args.size}")
    print(f"Requested weeks: {args.weeks}; upper bound: {upper_bound(args.groups, args.size)}")
    started = time.perf_counter()
    result, status = solver.solve()
    elapsed = time.perf_counter() - started
    if status == "found":
        print_schedule(result)
        print(f"Objective f(S): {objective(result)}")
        print(f"Valid schedule: {is_valid(result, args.groups, args.size)}")
    elif status == "timeout":
        print("Time limit reached. This does NOT prove that no solution exists.")
        print(f"Best valid partial schedule: {len(solver.best_schedule)} weeks")
        print_schedule(solver.best_schedule)
    elif status == "impossible_by_bound":
        print("Impossible: requested weeks exceed the mathematical upper bound.")
    else:
        print("No solution exists for this configuration (search completed).")
    print(f"Visited nodes: {solver.nodes}, Backtracks: {solver.backtracks}, Time: {elapsed:.3f}s")


if __name__ == "__main__":
    main()
