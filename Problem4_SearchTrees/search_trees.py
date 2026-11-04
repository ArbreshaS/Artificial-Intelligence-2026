"""Construct finite BFS search trees for three example problems."""

from collections import deque
from itertools import combinations


def puzzle_moves(state):
    blank = state.index(0)
    row, col = divmod(blank, 3)
    for name, dr, dc in (("up", -1, 0), ("down", 1, 0), ("left", 0, -1), ("right", 0, 1)):
        r, c = row + dr, col + dc
        if 0 <= r < 3 and 0 <= c < 3:
            other = r * 3 + c
            child = list(state)
            child[blank], child[other] = child[other], child[blank]
            yield f"Move blank {name}", tuple(child)


def missionaries_moves(state):
    """State: missionaries left, cannibals left, boat side (0 left, 1 right)."""
    m, c, side = state
    for dm, dc in ((1, 0), (2, 0), (0, 1), (0, 2), (1, 1)):
        direction = -1 if side == 0 else 1
        nm, nc = m + direction * dm, c + direction * dc
        if not (0 <= nm <= 3 and 0 <= nc <= 3):
            continue
        if (nm and nm < nc) or (3 - nm and 3 - nm < 3 - nc):
            continue
        yield f"{dm} missionary, {dc} cannibal: {'right' if side == 0 else 'left'}", (nm, nc, 1 - side)


def workforce_moves(state):
    """Assign two of four workers; no worker may work consecutive days."""
    assignments = state
    if len(assignments) == 3:
        return
    previous = set(assignments[-1]) if assignments else set()
    for pair in combinations('ABCD', 2):
        if previous.isdisjoint(pair):
            yield f"Day {len(assignments) + 1}: {''.join(pair)}", assignments + (pair,)


PROBLEMS = {
    "8-Puzzle": {
        "initial": (1, 2, 3, 4, 5, 6, 0, 7, 8),
        "goal": lambda state: state == (1, 2, 3, 4, 5, 6, 7, 8, 0),
        "moves": puzzle_moves,
    },
    "Missionaries and Cannibals": {
        "initial": (3, 3, 0),
        "goal": lambda state: state == (0, 0, 1),
        "moves": missionaries_moves,
    },
    "Rotating Workforce Scheduling": {
        "initial": (),
        "goal": lambda state: len(state) == 3,
        "moves": workforce_moves,
    },
}


def build_tree(problem, max_depth):
    """Return BFS nodes (state, parent index, action, depth), up to max_depth.

    A state is expanded only on first discovery. Repeated states are omitted,
    making the result a finite BFS spanning tree of the reachable state graph.
    """
    if max_depth < 0:
        raise ValueError("Depth must be non-negative")
    spec = PROBLEMS[problem]
    nodes = [(spec['initial'], None, 'Start', 0)]
    seen = {spec['initial']}
    queue = deque([0])
    while queue:
        index = queue.popleft()
        state, _, _, depth = nodes[index]
        if depth == max_depth or spec['goal'](state):
            continue
        for action, child in spec['moves'](state):
            if child in seen:
                continue
            seen.add(child)
            nodes.append((child, index, action, depth + 1))
            queue.append(len(nodes) - 1)
    return nodes


def solution_path(problem, nodes):
    """Find the first goal in the BFS tree and reconstruct its path."""
    for index, node in enumerate(nodes):
        if PROBLEMS[problem]['goal'](node[0]):
            path = []
            while index is not None:
                state, parent, action, depth = nodes[index]
                path.append((state, action, depth))
                index = parent
            return list(reversed(path))
    return None


def format_state(problem, state):
    if problem == '8-Puzzle':
        return '/'.join(''.join(str(x) if x else '_' for x in state[i:i+3]) for i in (0, 3, 6))
    if problem == 'Missionaries and Cannibals':
        return f"left: {state[0]}M {state[1]}C; boat: {'left' if state[2] == 0 else 'right'}"
    return ' → '.join(''.join(pair) for pair in state) or 'No assignments'


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Build a BFS search tree')
    parser.add_argument('problem', choices=['puzzle', 'missionaries', 'workforce'])
    parser.add_argument('--depth', type=int, default=12)
    args = parser.parse_args()
    names = dict(puzzle='8-Puzzle', missionaries='Missionaries and Cannibals', workforce='Rotating Workforce Scheduling')
    name = names[args.problem]
    if args.depth < 0:
        parser.error('depth must be non-negative')
    nodes = build_tree(name, args.depth)
    for i, (state, parent, action, depth) in enumerate(nodes):
        print(f'{i}: parent={parent}, depth={depth}, {action}: {format_state(name, state)}')
    path = solution_path(name, nodes)
    print(f'Nodes: {len(nodes)}; goal depth: {len(path) - 1 if path else "not found within limit"}')


if __name__ == '__main__':
    main()
