import sys
import collections
from functools import lru_cache


with open('dane.txt', 'r') as f:
    lines = [line.strip() for line in f if line.strip()]


s_t_line = lines[0]
s, t = map(int, s_t_line.split(','))

adj = {}
vertices = set()
for line in lines[1:]:
    if ':' in line:
        v_str, neigh_str = line.split(':', 1)
        v = int(v_str.strip())
        neigh = [int(x.strip()) for x in neigh_str.split(',') if x.strip()]
        adj[v] = set(neigh)
        vertices.add(v)
        for nb in neigh:
            vertices.add(nb)

for u in list(adj):
    for v in list(adj[u]):
        if v not in adj:
            adj[v] = set()
        adj[v].add(u)

play_vertices = [v for v in sorted(vertices) if v != s and v != t]
n_play = len(play_vertices)
vertex_to_bit = {v: i for i, v in enumerate(play_vertices)}
full_mask = (1 << n_play) - 1 if n_play > 0 else 0

def has_path(short_verts):
    allowed = {s, t} | set(short_verts)
    visited = set()
    queue = collections.deque([s])
    visited.add(s)
    while queue:
        u = queue.popleft()
        if u == t:
            return True
        for v in adj.get(u, []):
            if v in allowed and v not in visited:
                visited.add(v)
                queue.append(v)
    return False

@lru_cache(maxsize=None)
def can_destroyer_win(short_mask, unclaimed_mask, cut_turn):
    short_verts = [play_vertices[i] for i in range(n_play) if short_mask & (1 << i)]
    
    if has_path(short_verts):
        return False

    remaining = [play_vertices[i] for i in range(n_play) if unclaimed_mask & (1 << i)]
    if not has_path(short_verts + remaining):
        return True
    
    if unclaimed_mask == 0:
        return True
    

    moves = [i for i in range(n_play) if unclaimed_mask & (1 << i)]
    
    if cut_turn:  
        for i in moves:
            new_unclaimed = unclaimed_mask ^ (1 << i)
            if can_destroyer_win(short_mask, new_unclaimed, False):
                return True
        return False
    else:  
        for i in moves:
            new_short = short_mask | (1 << i)
            new_unclaimed = unclaimed_mask ^ (1 << i)
            if not can_destroyer_win(new_short, new_unclaimed, True):
                return False
        return True

result = can_destroyer_win(0, full_mask, True)
print(result)
