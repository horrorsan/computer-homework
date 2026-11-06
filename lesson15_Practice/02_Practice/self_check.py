"""运行方式：python self_check.py

每一行会告诉你：通过 / 还没写 / 需要修改。
"""
from __future__ import annotations

import sys

from checks import CheckSuite


class SelfCheckRunner:
    """逐项运行自测，并用中文打印结果。"""

    def __init__(self) -> None:
        self.checks = CheckSuite().checks()

    def run(self) -> int:
        passed = 0
        current_group = ""
        for check in self.checks:
            if check.group != current_group:
                current_group = check.group
                print(f"\n【{current_group}】")
            try:
                check.run()
            except NotImplementedError as error:
                print(f"  ⏳ {check.name}：{error}")
            except AssertionError as error:
                print(f"  ✗  {check.name}\n       {error}")
            except Exception as error:  # noqa: BLE001 - 给初学者看清报错类型
                print(f"  ✗  {check.name}\n       程序出错：{type(error).__name__}: {error}")
            else:
                passed += 1
                print(f"  ✓  {check.name}")
        total = len(self.checks)
        print(f"\n通过 {passed} / {total} 项")
        return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(SelfCheckRunner().run())
