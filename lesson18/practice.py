"""只修改标有TODO的 priority 和 relax；其余搜索骨架已经提供。"""
from provided import search


def priority(g, h):

    return g + h

def relax(g, parent, u, v, edge_cost):
    

    new_cost = g[u] + edge_cost
    if v not in g or new_cost < g[v]:
        g[v] = new_cost
        parent[v] = u
        return True
    return False


def dijkstra(graph, start, goal):
    """完整搜索入口：不使用目标估计。"""
    return search(graph, start, goal, {}, priority, relax)


def astar(graph, start, goal, heuristic):
    """完整搜索入口：优先处理 f=g+h 小的候选。"""
    return search(graph, start, goal, heuristic, priority, relax)
