"""迷你行为树引擎：第15课练习用。

这个文件已经写好，不需要修改。它只做一件事：
把“判断”和“行动”按树的规则一个个检查。

两条规则：
  顺序 Sequence ：前一步成功，才做下一步；遇到“失败”或“运行中”就停下并向上报告。
  选择 Selector ：先试左边的方案；遇到“成功”或“运行中”就停下并向上报告，
                  只有“失败”才继续试下一个方案。
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Callable

World = dict[str, Any]


class BehaviorStatus(str, Enum):
    """一个节点执行后的三种结果。"""

    SUCCESS = "success"   # 成功 / 成立
    FAILURE = "failure"   # 失败 / 不成立
    RUNNING = "running"   # 运行中：事情还没做完


class Node(ABC):
    """树上的一个节点。"""

    def __init__(self, name: str) -> None:
        self.name = name

    @abstractmethod
    def tick(self, world: World) -> BehaviorStatus:
        """让这个节点检查（或执行）一次，并返回结果。"""

    def _report(self, world: World, status: BehaviorStatus) -> BehaviorStatus:
        """记录“走过哪个节点、结果是什么”，方便你对照树上的路径。"""
        world.setdefault("trace", []).append(f"{self.name}:{status.value}")
        return status


class Condition(Node):
    """判断节点：只回答“是”或“不是”，不改变游戏。"""

    def __init__(self, name: str, predicate: Callable[[World], bool]) -> None:
        super().__init__(name)
        self.predicate = predicate

    def tick(self, world: World) -> BehaviorStatus:
        status = BehaviorStatus.SUCCESS if self.predicate(world) else BehaviorStatus.FAILURE
        return self._report(world, status)


class Action(Node):
    """行动节点：真正去做一件事，可能改变游戏。"""

    def __init__(
        self,
        name: str,
        effect: Callable[[World], BehaviorStatus] | None = None,
    ) -> None:
        super().__init__(name)
        self.effect = effect

    def tick(self, world: World) -> BehaviorStatus:
        status = BehaviorStatus.SUCCESS if self.effect is None else self.effect(world)
        world["last_action"] = self.name
        return self._report(world, status)


class Composite(Node):
    """有孩子的节点（分支）。"""

    def __init__(self, name: str, children: list[Node]) -> None:
        super().__init__(name)
        self.children = children


class Sequence(Composite):
    """顺序：一个接一个做，前面不成功就停。"""

    def tick(self, world: World) -> BehaviorStatus:
        for child in self.children:
            status = child.tick(world)
            if status is not BehaviorStatus.SUCCESS:
                return self._report(world, status)
        return self._report(world, BehaviorStatus.SUCCESS)


class Selector(Composite):
    """选择：按顺序试方案，找到可用的就停。"""

    def tick(self, world: World) -> BehaviorStatus:
        for child in self.children:
            status = child.tick(world)
            if status is not BehaviorStatus.FAILURE:
                return self._report(world, status)
        return self._report(world, BehaviorStatus.FAILURE)
