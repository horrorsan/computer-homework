"""第15课练习：让怪物做出选择。

你的任务（30分钟）：只完成下面标着 TODO 的三个函数
    1. is_hp_low          血量是不是很低？          （判断，只读）
    2. is_hero_in_sight   勇者是不是在范围内？      （判断，只读）
    3. attack             攻击一次，并进入冷却      （行动，会改血量和冷却）

flee、patrol、build_monster_tree、simulate 已经写好，不用改。
三个函数写完后，运行  python demo.py  就能看到怪物做出选择。

world 就是一个字典，保存游戏里的各种数据，例如：
    monster_hp / monster_max_hp   怪物当前血量 / 满血
    hero_pos / monster_pos        勇者和怪物的位置 (x, y)
    sight_range                   范围
    hero_hp                       勇者血量
    attack_cooldown               还要再等几次才能再次造成伤害
    damage / cooldown             一次伤害 / 攻击后的冷却次数
"""
from __future__ import annotations

from tree_engine import Action, BehaviorStatus, Condition, Selector, Sequence, World


# ---------------------------------------------------------------------------
# 你要完成的三个函数
# ---------------------------------------------------------------------------
def is_hp_low(world: World) -> bool:
    """怪物血量比例是否低于阈值？只读，不要修改 world。

    比例 = monster_hp / monster_max_hp
    阈值 = world.get("hp_threshold", 0.3)
    注意：刚好等于阈值，不算“低于”。满血为 0 时无法相除，直接当作低血。
    """
    max_hp = world.get("monster_max_hp",0)

    if max_hp <= 0:
        return True
    
    hp = world.get("monster_hp",0)
    threshold = world.get("hp_threshold",0.3)

    ratio = hp / max_hp
    return ratio < threshold

def is_hero_in_sight(world: World) -> bool:
    """勇者是否在范围内？只读，不要修改 world。

    距离 = |怪物x - 勇者x| + |怪物y - 勇者y|
    距离 <= sight_range 就算在范围内（默认范围 5）。
    """
    hero_x , hero_y = world["hero_pos"]
    monster_x , monster_y = world["monster_pos"]
    distance = abs(monster_x - hero_x) + abs(monster_y - hero_y)
    sight_range = world.get("sight_range" , 5)
    return distance <= sight_range


def attack(world: World) -> BehaviorStatus:
    """攻击一次。

    如果 attack_cooldown 大于 0：
        还在冷却，把它减 1，不造成伤害，返回“运行中”。
    否则：
        勇者血量 hero_hp 减去 damage（默认 5），
        把 attack_cooldown 设为 cooldown（默认 2），返回“成功”。
    """
    cooldown_left = world.get("attack_cooldown",0)

    if cooldown_left > 0:
        world["attack_cooldown"] = cooldown_left - 1
        return BehaviorStatus.RUNNING
    damage = world.get("damage" , 5)

    world["hero_hp"] = world.get("hero_hp" , 0) - damage

    world["attack_cooldown"] = world.get("cooldown" , 2)
    
    return BehaviorStatus.SUCCESS
    


# ---------------------------------------------------------------------------
# 下面是已经写好的部分
# ---------------------------------------------------------------------------
def _clamp(value: int, low: int, high: int) -> int:
    """把数字限制在 low 到 high 之间。"""
    return max(low, min(high, value))


def flee(world: World) -> BehaviorStatus:
    """（已提供）向远离勇者的方向走一步，不走出地图。"""
    hx, hy = (int(v) for v in world["hero_pos"])
    mx, my = (int(v) for v in world["monster_pos"])
    width, height = (int(v) for v in world.get("grid", (10, 10)))
    dx, dy = mx - hx, my - hy
    step_x = (dx > 0) - (dx < 0)
    step_y = (dy > 0) - (dy < 0)
    if step_x == 0 and step_y == 0:
        nx = mx + 1 if mx + 1 < width else mx - 1
        ny = my
    elif abs(dx) >= abs(dy):
        nx, ny = mx + step_x, my
    else:
        nx, ny = mx, my + step_y
    world["monster_pos"] = (_clamp(nx, 0, width - 1), _clamp(ny, 0, height - 1))
    return BehaviorStatus.SUCCESS


def patrol(world: World) -> BehaviorStatus:
    """（已提供）按 右、下、左、上 的顺序，走到第一个不出地图的相邻格子。"""
    mx, my = (int(v) for v in world["monster_pos"])
    width, height = (int(v) for v in world.get("grid", (10, 10)))
    for nx, ny in ((mx + 1, my), (mx, my + 1), (mx - 1, my), (mx, my - 1)):
        if 0 <= nx < width and 0 <= ny < height:
            world["monster_pos"] = (nx, ny)
            break
    return BehaviorStatus.SUCCESS


def build_monster_tree() -> Selector:
    """（已提供）搭出怪物的树：先保命，再战斗，最后巡逻。"""
    return Selector(
        "root",
        [
            Sequence("flee_seq", [Condition("is_hp_low", is_hp_low), Action("flee", flee)]),
            Sequence(
                "fight_seq",
                [Condition("is_hero_in_sight", is_hero_in_sight), Action("attack", attack)],
            ),
            Action("patrol", patrol),
        ],
    )


HERO_STEPS_PER_TICK = 2   # 勇者每一步向怪物靠近两格


def simulate(steps: int = 20, seed: int = 42) -> list[str]:
    """（已提供）勇者每步靠近怪物，让怪物的树检查一次，返回每步做的事。"""
    _ = seed
    world: World = {
        "hero_pos": (0, 0),
        "monster_pos": (9, 0),
        "monster_hp": 20,
        "monster_max_hp": 20,
        "hero_hp": 100,
        "sight_range": 5,
        "attack_cooldown": 0,
        "hp_threshold": 0.3,
        "damage": 5,
        "cooldown": 2,
        "grid": (10, 10),
    }
    tree = build_monster_tree()
    actions: list[str] = []
    for step in range(steps):
        for _ in range(HERO_STEPS_PER_TICK):
            hx, hy = world["hero_pos"]
            mx, my = world["monster_pos"]
            if hx != mx:
                hx += 1 if mx > hx else -1
            elif hy != my:
                hy += 1 if my > hy else -1
            world["hero_pos"] = (hx, hy)
        if step == max(1, steps // 2):
            world["monster_hp"] = 2          # 战斗中途，怪物受了重伤
        world["trace"] = []
        tree.tick(world)
        actions.append(str(world["last_action"]))
    return actions
