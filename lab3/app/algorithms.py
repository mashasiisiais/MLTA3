import math

# ДЕЙКСТРА
def dijkstra(vertices, edges, start):
    dist = {v: math.inf for v in vertices}
    prev = {v: None for v in vertices}
    dist[start] = 0

    visited = set()
    protocol = []
    step = 1

    outgoing = {v: [] for v in vertices}
    for u, v, w in edges:
        outgoing[u].append((v, w))
    
    for u in outgoing:
        outgoing[u].sort(key=lambda x: x[0])

    while len(visited) < len(vertices):
        u = None
        best = math.inf
        for v in vertices:
            if v not in visited and dist[v] < best:
                best = dist[v]
                u = v

        if u is None:
            protocol.append("Зупинка: залишились недосяжні вершини.")
            break

        visited.add(u)
        protocol.append(f"[Крок {step}] Обрано: {u}, dist[{u}]={dist[u]}, Visited={sorted(list(visited))}")
        step += 1

        for (to, w) in outgoing[u]:
            if dist[to] > dist[u] + w:
                old = dist[to]
                dist[to] = dist[u] + w
                prev[to] = u
                protocol.append(f"  Релаксація: {u}→{to} (w={w}): {old} → {dist[to]}")

    return dist, prev, protocol


def reconstruct_path_dijkstra(prev, start, end):
    if start == end:
        return [start]
    if prev[end] is None:
        return None
    path = []
    cur = end
    while cur is not None:
        path.append(cur)
        cur = prev[cur]
    path.reverse()
    if path and path[0] == start:
        return path
    return None


# ФЛОЙД-УОРШЕЛ
def floyd_warshall(vertices, edges):
    n = len(vertices)
    idx = {v: i for i, v in enumerate(vertices)}
    D = [[math.inf] * n for _ in range(n)]
    NXT = [[None] * n for _ in range(n)]

    for v in vertices:
        D[idx[v]][idx[v]] = 0
        NXT[idx[v]][idx[v]] = v

    for u, v, w in edges:
        D[idx[u]][idx[v]] = min(D[idx[u]][idx[v]], w)
        NXT[idx[u]][idx[v]] = v

    protocol = []

    for k in range(n):
        protocol.append(f"\n=== Проміжна вершина k = {vertices[k]} ===")
        for i in range(n):
            for j in range(n):
                if D[i][k] == math.inf or D[k][j] == math.inf:
                    continue
                new_val = D[i][k] + D[k][j]
                if new_val < D[i][j]:
                    old = D[i][j]
                    D[i][j] = new_val
                    NXT[i][j] = NXT[i][k]
                    protocol.append(f"  Оновлення: {vertices[i]}->{vertices[j]}: {old} → {new_val}")

    return D, NXT, protocol


def reconstruct_path_floyd(nxt_matrix, vertices, start, end):
    idx = {v: i for i, v in enumerate(vertices)}
    i = idx[start]
    j = idx[end]
    
    if nxt_matrix[i][j] is None:
        return None
        
    path = [start]
    curr = start
    while curr != end:
        curr = nxt_matrix[idx[curr]][idx[end]]
        if curr is None:
            return None
        path.append(curr)
    return path