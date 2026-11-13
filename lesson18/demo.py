"""运行演示。未补完时会给出提示，不会打印伪造结果。"""
import argparse
import sys
from provided import BAD_H, BRANCH_GRAPH, BRANCH_H, GOOD_H, MAIN_GRAPH, PAPER_H2_H, changed_graph, load_target, paper_graph


def show(label, result, trace=False):
    print(f"\n{label}")
    print("路线：" + (" -> ".join(result.path) if result.path else "不可达"))
    print(f"累计：{result.cost} 点体力")
    print("有效取出：" + " -> ".join(result.expanded))
    print(f"取出数量：{len(result.expanded)}；跳过旧记录：{result.stale_skipped}")
    if trace:
        print("改写记录：")
        for u, v, old, new in result.updates:
            print(f"  经 {u} 到 {v}：{old} 改成 {new}")


def show_paper(module):
    show("L18-H1 原图", module.dijkstra(paper_graph("L18-H1"), "S", "T"), True)
    show("L18-H1 C到T改为1点", module.dijkstra(paper_graph("L18-H1", changed=True), "S", "T"))
    show("L18-H2 给定h", module.astar(paper_graph("L18-H2"), "S", "T", PAPER_H2_H), True)
    show("L18-H2 故意把B的h改为8", module.astar(paper_graph("L18-H2"), "S", "T", {**PAPER_H2_H, "B": 8}))
    show("L18-H2 h全为0", module.astar(paper_graph("L18-H2"), "S", "T", {}))


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="第18课路线侦探")
    parser.add_argument("--reference", action="store_true", help="使用相邻完整示例")
    parser.add_argument("--module", help="指定自己的实现文件")
    parser.add_argument("--paper", action="store_true", help="手算完成后核对题图")
    args = parser.parse_args()
    try:
        module = load_target(args.module, args.reference)
        if args.paper:
            show_paper(module)
            return 0
        print("箭头是单向通道，边上的数字表示体力点。")
        for u, edges in MAIN_GRAPH.items():
            for v, cost in edges:
                print(f"  {u} -> {v}：{cost} 点")
        show("Dijkstra：按累计g排队", module.dijkstra(MAIN_GRAPH, "S", "T"), True)
        show("A*：使用给定的不高估且一致的h", module.astar(MAIN_GRAPH, "S", "T", GOOD_H), True)
        show("只把B到A改为5点后", module.dijkstra(changed_graph(), "S", "T"))
        show("故意坏估计：B的h改成10（反例，不能照此使用）", module.astar(MAIN_GRAPH, "S", "T", BAD_H))
        print("\n比较上面的真实运行结果：坏估计可能错过更省的路线。")
        print("\n支路对照：S到C花1，C到D花1，D到E花1，E到T花3。")
        show("支路图 Dijkstra", module.dijkstra(BRANCH_GRAPH, "S", "T"))
        show("支路图 A*", module.astar(BRANCH_GRAPH, "S", "T", BRANCH_H))
    except NotImplementedError as exc:
        print(f"\n⏳ 还没有补完：{exc}")
        print("先补 practice.py 的两个TODO，再运行 python self_check.py。")
    except Exception as exc:
        print(f"\n✗ 应为可运行的路线推演，你的结果为 {type(exc).__name__}: {exc}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
