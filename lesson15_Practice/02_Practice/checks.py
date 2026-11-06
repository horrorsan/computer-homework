"""第15课自测：每一项都对应课件里的一个预测或一张表。

不需要修改这个文件。运行 python self_check.py 查看结果。
"""
from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from typing import Any, Callable

import monster_ai as ai
from tree_engine import BehaviorStatus

S = BehaviorStatus.SUCCESS
R = BehaviorStatus.RUNNING


@dataclass(frozen=True)
class Check:
    group: str
    name: str
    run: Callable[[], None]


def make_world(**changes: Any) -> dict[str, Any]:
    data: dict[str, Any] = {
        "hero_pos": (0, 0),
        "monster_pos": (3, 2),
        "monster_hp": 20,
        "monster_max_hp": 20,
        "hero_hp": 100,
        "sight_range": 5,
        "attack_cooldown": 0,
        "hp_threshold": 0.3,
        "damage": 5,
        "cooldown": 2,
        "grid": (10, 10),
        "trace": [],
    }
    data.update(changes)
    return data


def expect(actual: Any, expected: Any, hint: str) -> None:
    if actual != expected:
        raise AssertionError(f"{hint}：应该是 {expected!r}，你的结果是 {actual!r}")


def visited(world: dict[str, Any]) -> list[str]:
    return [item.split(":")[0] for item in world["trace"]]


class CheckSuite:
    """把所有自测集中在一起，终端脚本和 pytest 共用同一份。"""

    def checks(self) -> list[Check]:
        return [
            Check("判断：血量", "按比例判断低血", self.hp_ratio),
            Check("判断：血量", "判断函数只读", self.hp_read_only),
            Check("判断：血量", "满血为0不报错", self.hp_zero_max),
            Check("判断：距离", "横向 + 纵向距离", self.sight_distance),
            Check("判断：距离", "判断函数只读", self.sight_read_only),
            Check("行动：攻击", "四次攻击与冷却表", self.cooldown_table),
            Check("行动：攻击", "冷却剩2时的预测", self.cooldown_prediction),
            Check("行动：攻击", "改变伤害与冷却", self.cooldown_custom),
            Check("整棵树", "场景一：血量低 → 逃跑", self.scene_low_hp),
            Check("整棵树", "场景二：玩家在范围 → 攻击", self.scene_in_sight),
            Check("整棵树", "场景三：玩家太远 → 巡逻", self.scene_far),
            Check("整棵树", "模拟中三种行动都出现", self.simulation),
        ]

    # ---- 判断：血量 ----
    def hp_ratio(self) -> None:
        for hp, max_hp, expected in [(5, 20, True), (6, 20, False), (20, 20, False),
                                      (11, 40, True), (12, 40, False)]:
            world = make_world(monster_hp=hp, monster_max_hp=max_hp)
            expect(ai.is_hp_low(world), expected, f"{hp}/{max_hp} 是否算低血")

    def hp_read_only(self) -> None:
        world = make_world(monster_hp=5)
        before = deepcopy(world)
        ai.is_hp_low(world)
        expect(world, before, "判断函数不应该修改 world")

    def hp_zero_max(self) -> None:
        expect(ai.is_hp_low(make_world(monster_hp=0, monster_max_hp=0)), True, "满血为0时")

    # ---- 判断：距离 ----
    def sight_distance(self) -> None:
        cases = [((0, 0), (3, 2), 5, True), ((0, 0), (3, 2), 4, False),
                 ((0, 0), (9, 9), 5, False), ((4, 4), (4, 4), 0, True)]
        for hero, monster, sight, expected in cases:
            world = make_world(hero_pos=hero, monster_pos=monster, sight_range=sight)
            expect(ai.is_hero_in_sight(world), expected,
                   f"勇者{hero}、怪物{monster}、范围{sight}")

    def sight_read_only(self) -> None:
        world = make_world()
        before = deepcopy(world)
        ai.is_hero_in_sight(world)
        expect(world, before, "判断函数不应该修改 world")

    # ---- 行动：攻击 ----
    def _run_attacks(self, world: dict[str, Any], expected: list[tuple[BehaviorStatus, int, int]]) -> None:
        for number, (status, hero_hp, cooldown) in enumerate(expected, start=1):
            result = ai.attack(world)
            expect(result, status, f"第{number}次攻击的返回结果")
            expect(world["hero_hp"], hero_hp, f"第{number}次攻击后的勇者血量")
            expect(world["attack_cooldown"], cooldown, f"第{number}次攻击后的剩余冷却")

    def cooldown_table(self) -> None:
        self._run_attacks(make_world(), [(S, 95, 2), (R, 95, 1), (R, 95, 0), (S, 90, 2)])

    def cooldown_prediction(self) -> None:
        self._run_attacks(make_world(hero_hp=80, attack_cooldown=2), [(R, 80, 1)])

    def cooldown_custom(self) -> None:
        self._run_attacks(make_world(damage=3, cooldown=1), [(S, 97, 1), (R, 97, 0), (S, 94, 1)])

    # ---- 整棵树 ----
    def scene_low_hp(self) -> None:
        world = make_world(monster_hp=5, hero_pos=(0, 0), monster_pos=(3, 2))
        before = world["monster_pos"]
        status = ai.build_monster_tree().tick(world)
        expect(status, S, "整棵树的返回结果")
        expect(world["last_action"], "flee", "这次选择的行动")
        expect(world["monster_pos"] != before, True, "逃跑后怪物位置应该改变")
        expect("is_hero_in_sight" in visited(world), False, "保命分支成功后，不应该再检查是否看见勇者")

    def scene_in_sight(self) -> None:
        world = make_world()
        status = ai.build_monster_tree().tick(world)
        expect(status, S, "整棵树的返回结果")
        expect(world["last_action"], "attack", "这次选择的行动")
        expect(world["hero_hp"], 95, "勇者血量")
        expect("patrol" in visited(world), False, "攻击成功后，不应该再去巡逻")

    def scene_far(self) -> None:
        world = make_world(monster_pos=(9, 9))
        before = world["monster_pos"]
        status = ai.build_monster_tree().tick(world)
        expect(status, S, "整棵树的返回结果")
        expect(world["last_action"], "patrol", "这次选择的行动")
        expect(world["monster_pos"] != before, True, "巡逻后怪物位置应该改变")
        expect("attack" in visited(world), False, "看不见勇者时，不应该攻击")

    def simulation(self) -> None:
        actions = ai.simulate(steps=20)
        expect(len(actions), 20, "模拟返回的步数")
        expect(set(actions) <= {"patrol", "attack", "flee"}, True, "每一步的行动名称")
        expect({"patrol", "attack", "flee"} <= set(actions), True,
               f"20步里应该出现巡逻、攻击、逃跑；你的结果是 {actions}")
