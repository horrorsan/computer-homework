"""给定的图、地图适配、过程记录与路径还原。"""
from dataclasses import dataclass
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


def emit(trace, event, node, detail=None):
    if trace is not None:
        trace.append((event, node, detail))


def validate_graph(graph, start, goal):
    if start not in graph or goal not in graph:
        raise ValueError("起点和终点都必须在图里")
    if any(neighbor not in graph for neighbors in graph.values() for neighbor in neighbors):
        raise ValueError("邻居也必须是图里的点")


def reconstruct_path(parent, goal):
    result = []
    seen = set()
    node = goal
    while node is not None:
        if node in seen:
            raise ValueError("来路形成了环，检查是否重复发现并覆盖了parent")
        seen.add(node)
        result.append(node)
        node = parent[node]
    result.reverse()
    return result


def load_implementation(path=None, reference=False):
    here = Path(__file__).resolve().parent
    if reference:
        path = here.parent / "04_Teacher" / "reference" / "solution.py"
    elif path is None:
        path = here / "practice.py"
    path = Path(path).resolve()
    if not path.is_file():
        raise FileNotFoundError("没有找到要运行的文件：" + str(path))
    spec = spec_from_file_location("lesson17_selected", path)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


ROOM_GRAPH = {
    "S": ["A", "B"],
    "A": ["S", "C"],
    "B": ["S", "T"],
    "C": ["A", "T"],
    "T": ["B", "C"],
}
GRID = ("S.#T", "....", ".#..")
BLOCKED_GRID = ("S.#T", "..#.", ".#..")


def room_graph():
    """返回一份新图；邻居顺序与课件一致。"""
    return {node: list(neighbors) for node, neighbors in ROOM_GRAPH.items()}


@dataclass(frozen=True)
class GridMap:
    """把字符地图与搜索策略分开，每个能走的位置对应一个点。"""

    rows: tuple[str, ...] = GRID

    def as_graph(self):
        rows = self.rows
        if not rows or not rows[0] or any(len(row) != len(rows[0]) for row in rows):
            raise ValueError("地图应是非空的长方形")
        graph, start, goal = {}, None, None
        height, width = len(rows), len(rows[0])
        for row in range(height):
            for col in range(width):
                if rows[row][col] == "#":
                    continue
                node = (row, col)
                graph[node] = []
                if rows[row][col] == "S":
                    if start is not None:
                        raise ValueError("地图只能有一个S")
                    start = node
                if rows[row][col] == "T":
                    if goal is not None:
                        raise ValueError("地图只能有一个T")
                    goal = node
                for dr, dc in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
                    nr, nc = row + dr, col + dc
                    if 0 <= nr < height and 0 <= nc < width and rows[nr][nc] != "#":
                        graph[node].append((nr, nc))
        if start is None or goal is None:
            raise ValueError("地图需要一个S和一个T")
        return graph, start, goal


def grid_graph(rows=GRID):
    """保留图适配接口，邻居按上、右、下、左排列。"""
    return GridMap(tuple(rows)).as_graph()


def path_moves(path):
    names = {(-1, 0): "上", (0, 1): "右", (1, 0): "下", (0, -1): "左"}
    return [names[(b[0] - a[0], b[1] - a[1])] for a, b in zip(path, path[1:])]

PAPER_H1_GRAPH = {'S': ['A', 'B'],
 'A': ['S', 'C', 'D'],
 'B': ['S', 'T'],
 'C': ['A'],
 'D': ['A', 'T'],
 'T': ['B', 'D']}
PAPER_H2_GRAPH = {'S': ['A', 'B'],
 'A': ['S', 'C'],
 'B': ['S', 'D'],
 'C': ['A', 'T'],
 'D': ['B', 'T'],
 'T': ['C', 'D']}


def paper_graph(exercise, variant="original"):
    """给一份全新的题图，避免把上一次封路带到下一题。"""
    base = {"L17-H1": PAPER_H1_GRAPH, "L17-H2": PAPER_H2_GRAPH}[exercise]
    graph = {node: list(neighbors) for node, neighbors in base.items()}
    if variant == "closed" and exercise == "L17-H1":
        graph["D"].remove("T")
        graph["T"].remove("D")
    elif variant == "reverse_start":
        graph["S"].reverse()
    elif variant != "original":
        raise ValueError("题图没有这种变式")
    return graph
