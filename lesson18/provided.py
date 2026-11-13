"""给定的带权图、估计值、搜索骨架与结果对象。"""
from dataclasses import dataclass
import heapq
import math

import importlib.util
import os
from pathlib import Path
import sys


@dataclass
class SearchResult:
    path: list
    cost: float
    expanded: list
    updates: list
    stale_skipped: int


def restore_path(parent, start, goal):
    """沿来路从目标回到起点，再反转。"""
    path = [goal]
    while path[-1] != start:
        path.append(parent[path[-1]])
    return path[::-1]


def validate_graph(graph, start, goal):
    if start not in graph or goal not in graph:
        raise ValueError("起点和终点必须都在图中")
    for node, edges in graph.items():
        if not isinstance(node, str):
            raise ValueError("位置名请使用字符串，便于按字母顺序处理并列候选")
        for neighbor, cost in edges:
            if neighbor not in graph:
                raise ValueError("每个邻居都应在图中有一行，即使它没有出边")
            if isinstance(cost, bool) or not isinstance(cost, (int, float)) or not math.isfinite(cost):
                raise ValueError("通道花费必须是有限数值")
            if cost < 0:
                raise ValueError("本课算法只接受不小于0的通道花费")


def search(graph, start, goal, heuristic, priority, relax):
    """h全为0就是Dijkstra；A星在同一骨架中使用给定的h。

    不把“首次发现”当成定案，改善g时重新入堆。
    h须由调用者保证不高估。课堂使用一致的h且h(goal)=0。
    骨架允许重新展开，因此不会用一个永久closed集合拦住更好来路。
    """
    validate_graph(graph, start, goal)
    h = {node: heuristic.get(node, 0) for node in graph}
    if any(isinstance(x, bool) or not isinstance(x, (int, float)) or not math.isfinite(x) or x < 0 for x in h.values()):
        raise ValueError("剩余估计请使用不小于0的有限数值")
    if h[goal] != 0:
        raise ValueError("目标处的剩余估计必须是0")
    g = {node: math.inf for node in graph}
    g[start] = 0
    parent = {}
    # 元组先比f，再比位置名，落实课件的“同值时按字母顺序”。
    frontier = [(priority(0, h[start]), start, 0)]
    expanded, updates = [], []
    stale_skipped = 0
    while frontier:
        _, node, queued_g = heapq.heappop(frontier)
        if queued_g != g[node]:
            stale_skipped += 1
            continue
        expanded.append(node)
        # 取出当前有效的最小候选后，才判断是否到达目标。
        if node == goal:
            return SearchResult(restore_path(parent, start, goal), g[goal], expanded, updates, stale_skipped)
        for neighbor, edge_cost in graph[node]:
            old_g = g[neighbor]
            if relax(g, parent, node, neighbor, edge_cost):
                updates.append((node, neighbor, old_g, g[neighbor]))
                heapq.heappush(frontier, (priority(g[neighbor], h[neighbor]), neighbor, g[neighbor]))
    return SearchResult([], math.inf, expanded, updates, stale_skipped)


def load_target(module_path=None, reference=False):
    own = Path(__file__).resolve().parent
    if str(own) not in sys.path:
        sys.path.insert(0, str(own))
    if module_path is None:
        module_path = os.environ.get("LESSON18_MODULE")
    if module_path is None:
        module_path = own.parent / "04_Teacher" / "reference" / "solution.py" if reference else own / "practice.py"
    module_path = Path(module_path).resolve()
    if not module_path.is_file():
        raise FileNotFoundError("没有找到指定模块，请保留材料目录层级或检查 --module 路径")
    spec = importlib.util.spec_from_file_location("lesson18_target", module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


MAIN_GRAPH = {
    "S": [("A", 4), ("B", 1)],
    "B": [("A", 2), ("T", 7)],
    "A": [("T", 1)],
    "T": [],
}
GOOD_H = {"S": 3, "B": 2, "A": 1, "T": 0}
# 故意高估的反例，只用于观察为什么不能随便夸大估计。
BAD_H = {"S": 0, "B": 10, "A": 0, "T": 0}


def changed_graph():
    """只把 B 到 A 的花费由 2 点改为 5 点，其他通道不变。"""
    return {node: [(v, 5 if node == "B" and v == "A" else w)
                   for v, w in edges] for node, edges in MAIN_GRAPH.items()}


# 这张图保持4点最优路线，另加一条看似便宜的支路。
BRANCH_GRAPH = {
    "S": [("B", 1), ("C", 1)],
    "B": [("A", 2)],
    "A": [("T", 1)],
    "C": [("D", 1)],
    "D": [("E", 1)],
    "E": [("T", 3)],
    "T": [],
}
BRANCH_H = {"S": 3, "B": 2, "A": 1, "T": 0, "C": 4, "D": 3, "E": 2}


PAPER_H1_GRAPH = {'S': [('A', 6), ('B', 2)],
 'B': [('A', 1), ('C', 4)],
 'A': [('C', 2), ('D', 5)],
 'C': [('D', 1), ('T', 7)],
 'D': [('T', 2)],
 'T': []}
PAPER_H2_GRAPH = {'S': [('A', 4), ('B', 2)],
 'A': [('T', 3)],
 'B': [('A', 1), ('C', 2)],
 'C': [('T', 2)],
 'T': []}
PAPER_H2_H = {'S': 4, 'A': 3, 'B': 3, 'C': 2, 'T': 0}


def paper_graph(exercise, changed=False):
    """每次从完整题面取一份新图。H1变式只改C到T。"""
    base = {"L18-H1": PAPER_H1_GRAPH, "L18-H2": PAPER_H2_GRAPH}[exercise]
    if changed and exercise != "L18-H1":
        raise ValueError("改边的变式属于H1")
    return {u: [(v, 1 if changed and (u, v) == ("C", "T") else cost)
                for v, cost in edges] for u, edges in base.items()}
