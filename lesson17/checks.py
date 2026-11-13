"""唯一的检查清单；self_check.py与pytest都调用这里。"""
from collections import Counter
from copy import deepcopy
from provided import BLOCKED_GRID, grid_graph, paper_graph, path_moves, reconstruct_path, room_graph


def small_graph(kind):
    if kind == "rooms":
        return room_graph(), "S", "T"
    if kind == "reverse":
        graph = room_graph()
        graph["S"] = ["B", "A"]
        return graph, "S", "T"
    if kind == "blocked":
        graph = room_graph()
        graph["C"].remove("T")
        graph["T"].remove("C")
        return graph, "S", "T"
    if kind == "cycle":
        return {"S": ["A"], "A": ["S", "B"], "B": ["A", "S"], "T": []}, "S", "T"
    if kind == "same":
        return room_graph(), "S", "S"
    if kind == "disconnected":
        return {"S": ["A"], "A": ["S"], "T": []}, "S", "T"
    if kind == "diamond":
        return {"S": ["A", "B"], "A": ["S", "C"], "B": ["S", "C"], "C": ["A", "B"], "T": []}, "S", "T"
    if kind == "cross":
        return {"S": ["A", "B"], "A": ["B", "C"], "B": ["T"], "C": [], "T": []}, "S", "T"
    if kind == "grid":
        return grid_graph()
    if kind == "grid_down_first":
        graph, start, goal = grid_graph()
        graph[start].reverse()
        return graph, start, goal
    if kind == "grid_blocked":
        return grid_graph(BLOCKED_GRID)
    if kind.startswith("paper_"):
        _, exercise, variant = kind.split("_", 2)
        return paper_graph("L17-" + exercise, variant), "S", "T"
    if kind == "invalid":
        return {"S": []}, "S", "T"
    raise ValueError("没有这个小图：" + kind)


# name、函数、小图、观察哪项、应为什么、对应课件页码
CASES = [
    ("DFS按邻居顺序走深", "dfs_path", "rooms", "path", ["S", "A", "C", "T"], 11),
    ("DFS交换起点邻居顺序", "dfs_path", "reverse", "path", ["S", "B", "T"], 11),
    ("DFS交叉边仍保持逐层走深", "dfs_path", "cross", "path", ["S", "A", "B", "T"], 11),
    ("DFS封路后退回分支", "dfs_path", "blocked", "backtrack", ["C", "A"], 12),
    ("DFS封路后仍能找到T", "dfs_path", "blocked", "path", ["S", "B", "T"], 12),
    ("DFS遇到环不重复发现", "dfs_path", "cycle", "unique_discover", True, 14),
    ("DFS没有路返回空列表", "dfs_path", "disconnected", "path", [], 14),
    ("DFS起点就是终点", "dfs_path", "same", "path", ["S"], 23),
    ("DFS点不存在时明确报错", "dfs_path", "invalid", "value_error", True, 2),
    ("BFS找到两次移动的路线", "bfs_path", "rooms", "path", ["S", "B", "T"], 22),
    ("BFS先检查队头", "bfs_path", "rooms", "expand", ["S", "A", "B"], 22),
    ("BFS队列快照与纸上表相同", "bfs_path", "rooms", "queues_after_expand", [("A", "B"), ("B", "C"), ("C", "T")], 22),
    ("BFS首次发现写来路", "bfs_path", "rooms", "goal_parent", "B", 23),
    ("BFS起点就是终点", "bfs_path", "same", "path", ["S"], 23),
    ("BFS没有路返回空列表", "bfs_path", "disconnected", "path", [], 14),
    ("BFS环中不重复发现", "bfs_path", "diamond", "unique_discover", True, 14),
    ("BFS点不存在时明确报错", "bfs_path", "invalid", "value_error", True, 2),
    ("网格按上右下左找到五步路线", "bfs_path", "grid", "moves", ["右", "下", "右", "右", "上"], 27),
    ("调换起点邻居顺序得到另一条同长路线", "bfs_path", "grid_down_first", "moves", ["下", "右", "右", "右", "上"], 27),
    ("封住(1,2)后网格不可达", "bfs_path", "grid_blocked", "path", [], 38),
    ("BFS不修改原图", "bfs_path", "rooms", "unchanged", True, 3),
]
CASES += [
    ("L17-H1 原图发现与回退", "dfs_path", "paper_H1_original", "dfs_paper_state",
     (["S", "A", "D", "T"], ["S", "A", "C", "D", "T"], ["C"]), 16),
    ("L17-H1 关D到T后回退", "dfs_path", "paper_H1_closed", "dfs_paper_state",
     (["S", "B", "T"], ["S", "A", "C", "D", "B", "T"], ["C", "D", "A"]), 16),
    ("L17-H1 原图先看B", "dfs_path", "paper_H1_reverse_start", "dfs_paper_state",
     (["S", "B", "T"], ["S", "B", "T"], []), 16),
    ("L17-H2 每轮队列、层数和来路", "bfs_path", "paper_H2_original", "bfs_paper_state",
     (["S", "A", "C", "T"], [("A", "B"), ("B", "C"), ("C", "D"), ("D", "T")],
      {"S": 0, "A": 1, "B": 1, "C": 2, "D": 2, "T": 3},
      {"S": None, "A": "S", "B": "S", "C": "A", "D": "B", "T": "C"}), 28),
    ("L17-H2 换序只换同长路线", "bfs_path", "paper_H2_reverse_start", "path", ["S", "B", "D", "T"], 28),
]
# 可在这里加自己画的小图和期望，self_check与pytest会一起使用。
EXTRA_CASES = []


class EventLog(list):
    """发现重复过多时中止，避免错误程序在环中一直运行。"""
    def append(self, event):
        if len(self) >= 120:
            raise AssertionError("过程事件超过120条，检查是否遗漏发现标记")
        super().append(event)


def completed_queues(trace):
    result, last, started = [], None, False
    for event, node, _ in trace:
        if event == "expand":
            if started and last is not None:
                result.append(last)
            started = True
            last = None
        elif event == "queue" and started:
            last = node
    if last is not None:
        result.append(last)
    return result


def evaluate(module, case):
    name, function, kind, observe, expected, page = case
    graph, start, goal = small_graph(kind)
    original = deepcopy(graph)
    trace = EventLog()
    try:
        path = getattr(module, function)(graph, start, goal, trace=trace)
    except ValueError:
        if observe == "value_error":
            return True
        raise
    if observe == "value_error":
        return False
    if observe == "path":
        return path
    if observe == "backtrack":
        return [node for event, node, _ in trace if event == "backtrack"]
    if observe == "expand":
        return [node for event, node, _ in trace if event == "expand"]
    if observe == "unique_discover":
        nodes = [node for event, node, _ in trace if event == "discover"]
        counts = Counter(nodes)
        return bool(nodes) and all(count == 1 for count in counts.values()) and len(nodes) <= len(graph)
    if observe == "goal_parent":
        parents = [parent for event, node, parent in trace if event == "discover" and node == goal]
        return parents[0] if len(parents) == 1 else parents
    if observe == "queues_after_expand":
        return completed_queues(trace)
    if observe == "dfs_paper_state":
        return (path, [node for event, node, _ in trace if event == "discover"],
                [node for event, node, _ in trace if event == "backtrack"])
    if observe == "bfs_paper_state":
        parents = {node: prior for event, node, prior in trace if event == "discover"}
        levels = {node: len(reconstruct_path(parents, node)) - 1 for node in parents}
        return path, completed_queues(trace), levels, parents
    if observe == "moves":
        return path_moves(path)
    if observe == "unchanged":
        return graph == original
    raise AssertionError("没有实现这个观察项：" + observe)


def run_case(module, case):
    try:
        actual = evaluate(module, case)
        passed = actual == case[4]
        return {"name": case[0], "status": "pass" if passed else "fail", "page": case[5],
                "message": "应为" + repr(case[4]) + "，你的结果为" + repr(actual)}
    except NotImplementedError as error:
        return {"name": case[0], "status": "pending", "page": case[5], "message": str(error)}
    except Exception as error:
        return {"name": case[0], "status": "fail", "page": case[5],
                "message": "应为" + repr(case[4]) + "，你的结果为" + type(error).__name__ + ": " + str(error)}


def run_all(module):
    return [run_case(module, case) for case in CASES + EXTRA_CASES]
