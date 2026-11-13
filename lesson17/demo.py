"""把同一张图的搜索过程打印出来；未补完函数也能运行。"""
import argparse
import sys
from provided import BLOCKED_GRID, GRID, grid_graph, load_implementation, paper_graph, path_moves, room_graph


def show_paper(module):
    for exercise, variants, run in (
        ("L17-H1", ("original", "closed", "reverse_start"), module.dfs_path),
        ("L17-H2", ("original", "reverse_start"), module.bfs_path),
    ):
        for variant in variants:
            trace = []
            path = run(paper_graph(exercise, variant), "S", "T", trace=trace)
            scenario = {"original": "原图", "closed": "关闭D到T", "reverse_start": "S先看B"}[variant]
            print(f"{exercise} {scenario}：{' → '.join(path)}，{len(path) - 1}次")
            if exercise == "L17-H1":
                for key, label in [("discover", "发现"), ("backtrack", "从这些点回退")]:
                    print(label + "：" + (" → ".join(node for event, node, _ in trace if event == key) or "无"))
            else:
                from checks import completed_queues
                parents = {node: prior for event, node, prior in trace if event == "discover"}
                print("每轮队列：" + "；".join(str(list(row)) for row in completed_queues(trace)))
                print("首次来路：" + "，".join(f"{node}←{prior or '无'}" for node, prior in parents.items()))


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="看两种探索顺序")
    parser.add_argument("--reference", action="store_true", help="改用相邻目录中的完整实现")
    parser.add_argument("--module", help="指定Python文件")
    parser.add_argument("--paper", action="store_true", help="手算完成后核对题图")
    args = parser.parse_args()
    try:
        module = load_implementation(args.module, args.reference)
    except (OSError, SyntaxError) as error:
        print("无法读入：" + str(error))
        return 1
    if args.paper:
        try:
            show_paper(module)
        except NotImplementedError:
            print("⏳ 先补完两个函数，再核对题图。")
        return 0
    print("房间地图：S连A、B；A连C；B和C分别连T。每条走廊双向、每次移动1秒。")
    for name in ("dfs_path", "bfs_path"):
        trace = []
        try:
            path = getattr(module, name)(room_graph(), "S", "T", trace=trace)
        except NotImplementedError:
            print("⏳ " + name + "尚未补完，请先打开practice.py。")
            continue
        print(("DFS" if name == "dfs_path" else "BFS") + "路线：" + " → ".join(path) + "；移动" + str(len(path) - 1) + "次")
        print("  发现顺序：" + "，".join(str(node) for event, node, _ in trace if event == "discover"))
        if name == "bfs_path":
            print("  队列快照：" + "；".join(str(list(node)) for event, node, _ in trace if event == "queue"))
    graph, start, goal = grid_graph()
    print("小地图：" + " / ".join(GRID) + "。只能上下左右，每次移动1秒。")
    try:
        path = module.bfs_path(graph, start, goal)
    except NotImplementedError:
        print("⏳ 补完bfs_path后，这里会显示绕墙的路线。")
        return 0
    if not path:
        print("✗ 网格应可到达，你的结果为无路线。")
        return 1
    print("网格路线：" + " → ".join(path_moves(path)))
    print("经过" + str(len(path)) + "个位置，移动" + str(len(path) - 1) + "次，共" + str(len(path) - 1) + "秒。")
    graph[start].reverse()
    alternate = module.bfs_path(graph, start, goal)
    print("只交换起点邻居顺序：" + " → ".join(path_moves(alternate)) + "；移动" + str(len(alternate) - 1) + "次。")
    blocked_graph, start, goal = grid_graph(BLOCKED_GRID)
    blocked = module.bfs_path(blocked_graph, start, goal)
    print("封住(1,2)后：" + ("不可达" if not blocked else str(blocked)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
