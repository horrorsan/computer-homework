"""运行 python self_check.py。只用Python自带模块。"""
import argparse
import json
import sys
from checks import CHECKS, EXTRA_CHECKS, run_check
from provided import load_target


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="第18课自测")
    parser.add_argument("--module", help="要检查的Python模块路径")
    parser.add_argument("--reference", action="store_true", help="使用相邻完整示例")
    parser.add_argument("--json", action="store_true", help="输出检查结果JSON")
    args = parser.parse_args()
    try:
        module = load_target(args.module, args.reference)
    except Exception as exc:
        print(f"✗ 应为可加载的练习模块，你的结果为 {type(exc).__name__}: {exc}")
        return 1
    rows = []
    for case in CHECKS + EXTRA_CHECKS:
        status, message = run_check(module, case)
        rows.append({"id": case.code, "label": case.label, "status": status, "message": message})
        if not args.json:
            mark = {"pass": "✓", "pending": "⏳", "fail": "✗"}[status]
            print(f"{mark} {case.code} {case.label}\n  {message}")
    counts = {s: sum(x["status"] == s for x in rows) for s in ["pass", "pending", "fail"]}
    if args.json:
        print(json.dumps({"counts": counts, "checks": rows}, ensure_ascii=False))
    else:
        print(f"\n完成 {counts['pass']} / 待补 {counts['pending']} / 需修改 {counts['fail']}")
    return 1 if counts["fail"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
