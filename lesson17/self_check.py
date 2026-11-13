"""直接运行：python self_check.py。"""
import argparse
import sys
from checks import run_all
from provided import load_implementation


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="检查本课两个函数")
    parser.add_argument("--reference", action="store_true", help="改用相邻目录中的完整实现")
    parser.add_argument("--module", help="指定要检查的Python文件")
    args = parser.parse_args()
    try:
        rows = run_all(load_implementation(args.module, args.reference))
    except (OSError, SyntaxError) as error:
        print("✗ 无法读入练习：" + str(error))
        return 1
    symbols = {"pass": "✓", "pending": "⏳", "fail": "✗"}
    for row in rows:
        print(symbols[row["status"]] + " " + row["name"] + "：" + row["message"])
    counts = {status: sum(row["status"] == status for row in rows) for status in symbols}
    print("合计：通过{pass}，待完成{pending}，未通过{fail}".format(**counts))
    return 1 if counts["fail"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
