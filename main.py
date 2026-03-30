from collections import deque
from functools import lru_cache

def read_graph(filename):
    with open(filename, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    s, t = map(int, lines[0].split(','))
    adj = {}

    for line in lines[1:]:
        v, neighbors = line.split(':')
        v = int(v)
        adj[v] = list(map(int, neighbors.split(',')))

    return s, t, adj


def is_connected(adj, owned, s, t):
    """Check if s and t are connected using only vertices in 'owned'."""
    if s not in owned or t not in owned:
        return False

    visited = set()
    queue = deque([s])

    while queue:
        v = queue.popleft()
        if v == t:
            return True
        for u in adj[v]:
            if u in owned and u not in visited:
                visited.add(u)
                queue.append(u)

    return False


def solve_game(s, t, adj):
    vertices = list(adj.keys())
    n = len(vertices)
    index = {v: i for i, v in enumerate(vertices)}

    @lru_cache(None)
    def dfs(mask, turn):
        """
        mask: 2*n bits
            first n bits → Constructor vertices
            next n bits → Destructor vertices
        turn: 0 = Destructor, 1 = Constructor
        """

        # Decode ownership
        constructor = set()
        destructor = set()

        for v in vertices:
            i = index[v]
            if mask & (1 << i):
                constructor.add(v)
            elif mask & (1 << (i + n)):
                destructor.add(v)

        # Terminal: all vertices assigned
        if len(constructor) + len(destructor) == n:
            return not is_connected(adj, constructor, s, t)  # True = Destructor wins

        # Try all unassigned vertices
        for v in vertices:
            i = index[v]
            if not (mask & (1 << i)) and not (mask & (1 << (i + n))):

                if turn == 0:
                    # Destructor move
                    new_mask = mask | (1 << (i + n))
                    if dfs(new_mask, 1):  # still winning
                        return True
                else:
                    # Constructor move
                    new_mask = mask | (1 << i)
                    if not dfs(new_mask, 0):  # Constructor forces win
                        return False

        return turn == 1  # if Constructor can't win → Destructor wins

    return dfs(0, 0)


if __name__ == "__main__":
    s, t, adj = read_graph("dane.txt")
    result = solve_game(s, t, adj)
    print(result)
