"""运行方式：python demo.py

看三个场景里，同一棵树怎样做出不同选择。需要先完成三个函数。
"""
from __future__ import annotations

from monster_ai import build_monster_tree, simulate


class SceneDemo:
    """把一个场景放进树里检查一次，并打印走过的节点。"""

    def __init__(self, title: str, **changes: object) -> None:
        self.title = title
        self.world = {
            "hero_pos": (0, 0), "monster_pos": (3, 2), "monster_hp": 20,
            "monster_max_hp": 20, "hero_hp": 100, "sight_range": 5,
            "attack_cooldown": 0, "hp_threshold": 0.3, "damage": 5,
            "cooldown": 2, "grid": (10, 10), "trace": [],
        }
        self.world.update(changes)

    def run(self) -> None:
        before_pos = self.world["monster_pos"]
        status = build_monster_tree().tick(self.world)
        print(f"\n{self.title}")
        print("  走过的节点：", " → ".join(self.world["trace"]))
        print("  选择的行动：", self.world["last_action"], f"（整棵树返回 {status.value}）")
        print("  怪物位置：", before_pos, "→", self.world["monster_pos"])
        print("  勇者血量：", self.world["hero_hp"])


def main() -> None:
    scenes = [
        SceneDemo("场景一：怪物只剩5点血，勇者就在旁边", monster_hp=5),
        SceneDemo("场景二：怪物满血，勇者距离5，范围也是5"),
        SceneDemo("场景三：怪物满血，勇者很远", monster_pos=(9, 9)),
    ]
    try:
        for scene in scenes:
            scene.run()
        print("\n20步模拟：", simulate(steps=20))
    except NotImplementedError as error:
        print(f"还有函数没写完：{error}")


if __name__ == "__main__":
    main()
