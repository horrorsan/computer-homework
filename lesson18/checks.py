"""唯一的检查与期望来源：self_check和pytest都调用这里。"""
from dataclasses import dataclass
import math
from provided import BAD_H, BRANCH_GRAPH, BRANCH_H, GOOD_H, MAIN_GRAPH, PAPER_H2_H, changed_graph, paper_graph


def equal(actual, expected):
    if actual != expected:
        raise AssertionError(f"应为 {expected!r}，你的结果为 {actual!r}")


def summary(result):
    return result.path, result.cost, result.expanded


def check_priority_1(m):
    equal(m.priority(3, 1), 4)


def check_priority_2(m):
    equal((m.priority(2, 5), m.priority(7, 0)), (7, 7))


def check_better(m):
    g, parent = {"S": 0, "B": 1, "A": 4}, {"B": "S", "A": "S"}
    changed = m.relax(g, parent, "B", "A", 2)
    equal((changed, g["A"], parent["A"], g["B"]), (True, 3, "B", 1))


def check_worse(m):
    g, parent = {"B": 1, "A": 2}, {"A": "S"}
    changed = m.relax(g, parent, "B", "A", 2)
    equal((changed, g["A"], parent["A"]), (False, 2, "S"))


def check_equal(m):
    g, parent = {"B": 1, "A": 3}, {"A": "S"}
    changed = m.relax(g, parent, "B", "A", 2)
    equal((changed, g["A"], parent["A"]), (False, 3, "S"))


def check_first_reach(m):
    g, parent = {"B": 1, "T": math.inf}, {}
    changed = m.relax(g, parent, "B", "T", 7)
    equal((changed, g["T"], parent["T"]), (True, 8, "B"))


def check_dijkstra(m):
    r = m.dijkstra(MAIN_GRAPH, "S", "T")
    equal(summary(r), (["S", "B", "A", "T"], 4, ["S", "B", "A", "T"]))
    equal([(u, v, new) for u, v, old, new in r.updates],
          [("S", "A", 4), ("S", "B", 1), ("B", "A", 3), ("B", "T", 8), ("A", "T", 4)])


def check_astar(m):
    equal(summary(m.astar(MAIN_GRAPH, "S", "T", GOOD_H)),
          (["S", "B", "A", "T"], 4, ["S", "B", "A", "T"]))


def check_h_zero(m):
    r1, r2 = m.dijkstra(MAIN_GRAPH, "S", "T"), m.astar(MAIN_GRAPH, "S", "T", {})
    equal(summary(r2), summary(r1))


def check_changed_edge(m):
    equal(summary(m.dijkstra(changed_graph(), "S", "T")),
          (["S", "A", "T"], 5, ["S", "B", "A", "T"]))
    r = m.astar(changed_graph(), "S", "T", GOOD_H)
    equal((r.path, r.cost), (["S", "A", "T"], 5))


def check_same_point(m):
    for r in [m.dijkstra(MAIN_GRAPH, "S", "S"), m.astar(MAIN_GRAPH, "S", "S", {})]:
        equal(summary(r), (["S"], 0, ["S"]))


def check_unreachable(m):
    graph = {"S": [("A", 2)], "A": [], "T": []}
    for r in [m.dijkstra(graph, "S", "T"), m.astar(graph, "S", "T", {})]:
        equal(summary(r), ([], math.inf, ["S", "A"]))


def check_zero_edge(m):
    g, parent = {"u": 2, "v": 5}, {"v": "S"}
    changed = m.relax(g, parent, "u", "v", 0)
    equal((changed, g["v"], parent["v"]), (True, 2, "u"))
    graph = {"S": [("A", 0)], "A": [("T", 0)], "T": []}
    equal(summary(m.dijkstra(graph, "S", "T")), (["S", "A", "T"], 0, ["S", "A", "T"]))


def expect_value_error(call):
    try:
        result = call()
    except ValueError:
        return
    raise AssertionError(f"应为 ValueError 拒绝负花费，你的结果为 {result!r}")


def check_negative_edge(m):
    graph = {"S": [("T", 1)], "T": [], "X": [("Y", -1)], "Y": []}
    expect_value_error(lambda: m.dijkstra(graph, "S", "T"))
    expect_value_error(lambda: m.astar(graph, "S", "T", {}))


def check_stale(m):
    graph = {"S": [("A", 10), ("B", 1)], "B": [("A", 1)], "A": [("C", 1)], "C": [("T", 100)], "T": []}
    r = m.dijkstra(graph, "S", "T")
    equal((r.path, r.cost, r.expanded, r.stale_skipped),
          (["S", "B", "A", "C", "T"], 103, ["S", "B", "A", "C", "T"], 1))


def check_tie_order(m):
    graph = {"S": [("B", 1), ("A", 1)], "B": [("T", 1)], "A": [("T", 1)], "T": []}
    equal(summary(m.dijkstra(graph, "S", "T")), (["S", "A", "T"], 2, ["S", "A", "B", "T"]))


def check_bad_h_counterexample(m):
    # 这里只确认“故意高估会出错”的现象，并不把这个h当成正确用法。
    r = m.astar(MAIN_GRAPH, "S", "T", BAD_H)
    equal(summary(r), (["S", "A", "T"], 5, ["S", "A", "T"]))


def check_zero_cycle(m):
    graph = {"S": [("A", 0)], "A": [("S", 0), ("T", 1)], "T": []}
    equal(summary(m.dijkstra(graph, "S", "T")), (["S", "A", "T"], 1, ["S", "A", "T"]))


def check_direction(m):
    graph = {"S": [("A", 1), ("B", 2)], "A": [("X", 1)], "B": [("T", 1)], "X": [], "T": []}
    h = {"S": 3, "A": 4, "X": 4, "B": 1, "T": 0}
    r = m.astar(graph, "S", "T", h)
    equal(summary(r), (["S", "B", "T"], 3, ["S", "B", "T"]))


def check_branch_saves_pops(m):
    dijkstra = m.dijkstra(BRANCH_GRAPH, "S", "T")
    astar = m.astar(BRANCH_GRAPH, "S", "T", BRANCH_H)
    equal(summary(dijkstra), (["S", "B", "A", "T"], 4, ["S", "B", "C", "D", "A", "E", "T"]))
    equal(summary(astar), (["S", "B", "A", "T"], 4, ["S", "B", "A", "T"]))


def check_paper_h1(m):
    graph = paper_graph("L18-H1")
    result = m.dijkstra(graph, "S", "T")
    equal(summary(result), (["S", "B", "A", "C", "D", "T"], 8, ["S", "B", "A", "C", "D", "T"]))
    g = {node: math.inf for node in graph}
    g["S"] = 0
    parent, rows = {}, []
    for node in result.expanded:
        for u, v, _, new in result.updates:
            if node == u:
                g[v], parent[v] = new, u
        rows.append(tuple(g[k] for k in ("S", "B", "A", "C", "D", "T")))
    inf = math.inf
    equal(rows, [(0, 2, 6, inf, inf, inf), (0, 2, 3, 6, inf, inf), (0, 2, 3, 5, 8, inf),
                 (0, 2, 3, 5, 6, 12), (0, 2, 3, 5, 6, 8), (0, 2, 3, 5, 6, 8)])
    equal(parent, {"B": "S", "A": "B", "C": "A", "D": "C", "T": "D"})
    changed = m.dijkstra(paper_graph("L18-H1", changed=True), "S", "T")
    equal((changed.path, changed.cost), (["S", "B", "A", "C", "T"], 6))


def check_paper_h2(m):
    graph = paper_graph("L18-H2")
    result = m.astar(graph, "S", "T", PAPER_H2_H)
    equal(summary(result), (["S", "B", "A", "T"], 6, ["S", "B", "A", "C", "T"]))
    equal([(u, v, new) for u, v, _, new in result.updates],
          [("S", "A", 4), ("S", "B", 2), ("B", "A", 3), ("B", "C", 4), ("A", "T", 6)])
    bad_h = {**PAPER_H2_H, "B": 8}
    equal(summary(m.astar(graph, "S", "T", bad_h)), (["S", "A", "T"], 7, ["S", "A", "T"]))
    equal(summary(m.astar(graph, "S", "T", {})), summary(m.dijkstra(graph, "S", "T")))


@dataclass(frozen=True)
class Check:
    code: str
    label: str
    requires: tuple
    run: object


CHECKS = [
    Check("P01", "排队数字：累计与估计相加", ("priority",), check_priority_1),
    Check("P02", "排队数字：h=0仍保留累计花费", ("priority",), check_priority_2),
    Check("R01", "主图：A由4改3，来路同步改B", ("relax",), check_better),
    Check("R02", "更贵的新路不改记录", ("relax",), check_worse),
    Check("R03", "代码边界：同价不覆盖原来路", ("relax",), check_equal),
    Check("R04", "主图：第一次发现T，先记8", ("relax",), check_first_reach),
    Check("D01", "主图：T先8后4，取出后再停", ("priority", "relax"), check_dijkstra),
    Check("A01", "主图：一致的h得到4点路线", ("priority", "relax"), check_astar),
    Check("A02", "h全0与Dijkstra相同", ("priority", "relax"), check_h_zero),
    Check("D02", "通道变式：B到A改5后最省路线花5点", ("priority", "relax"), check_changed_edge),
    Check("B01", "初始化：已经在终点，花费0", ("priority", "relax"), check_same_point),
    Check("B02", "边界：不可达保留无路线与无穷大", ("priority", "relax"), check_unreachable),
    Check("B03", "代码边界：0点通道可以更新", ("priority", "relax"), check_zero_edge),
    Check("B04", "适用条件：负花费要拒绝", ("priority", "relax"), check_negative_edge),
    Check("B05", "跳过堆中的旧记录", ("priority", "relax"), check_stale),
    Check("B06", "同值按字母取点", ("priority", "relax"), check_tie_order),
    Check("A03", "高估反例：返回5，错过4", ("priority", "relax"), check_bad_h_counterexample),
    Check("B07", "代码边界：零花费环不会反复入队", ("priority", "relax"), check_zero_cycle),
    Check("A04", "延伸：h真正参与候选顺序", ("priority", "relax"), check_direction),
    Check("A05", "支路对照：同为4点，A星少取出3个位置", ("priority", "relax"), check_branch_saves_pops),
    Check("H01", "L18-H1 六点取出顺序、g表、来路及改边", ("priority", "relax"), check_paper_h1),
    Check("H02", "L18-H2 同值顺序、来路及坏估计反例", ("priority", "relax"), check_paper_h2),
]


# 可添加自己的Check，让两条自测入口一起运行。
EXTRA_CHECKS = []


def run_check(module, case):
    """预探针只辨别TODO是否完成，不替代实际检查。"""
    try:
        if "priority" in case.requires:
            module.priority(0, 0)
        if "relax" in case.requires:
            module.relax({"u": 0, "v": math.inf}, {}, "u", "v", 1)
        case.run(module)
    except NotImplementedError as exc:
        return "pending", str(exc)
    except AssertionError as exc:
        return "fail", str(exc)
    except Exception as exc:
        return "fail", f"应为正常完成这一项，你的结果为 {type(exc).__name__}: {exc}"
    return "pass", "应该与题图和规则一致，你的结果已符合"
