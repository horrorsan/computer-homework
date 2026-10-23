"""M3 lesson 12: traverse the same dungeon tree in four orders.

Provided: TreeNode, _emit_visit, build_dungeon_rooms() and
build_monster_tree_shape() (only the *shape* of the deck's monster tree --
no tick, no statuses; the behavior tree runtime is lesson 14).

Implement the four traverse_* functions and emit a visit for every node.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field
from typing import Any, Iterator

from herodungeon.core.events import EventRecorder

SOURCE = "m3.tree"


@dataclass(slots=True)
class TreeNode:
    name: str
    payload: dict[str, Any] = field(default_factory=dict)
    children: list[TreeNode] = field(default_factory=list)

    def add(self, child: TreeNode) -> TreeNode:
        self.children.append(child)
        return child

    def __iter__(self) -> Iterator[TreeNode]:
        return iter(self.children)


def build_dungeon_rooms() -> TreeNode:
    """The dungeon room tree used by the engine and the M3 demo.

    entrance
    ├── hall
    │   ├── armory
    │   └── crypt
    │       └── boss
    └── garden
    """
    entrance = TreeNode("entrance")
    hall = entrance.add(TreeNode("hall"))
    hall.add(TreeNode("armory"))
    crypt = hall.add(TreeNode("crypt"))
    crypt.add(TreeNode("boss"))
    entrance.add(TreeNode("garden"))
    return entrance


def build_monster_tree_shape() -> TreeNode:
    """Shape of the lesson-12 deck's monster tree (slide "完整怪物树").

    Only plain ``TreeNode``s: ``payload["kind"]`` says what the node *will* be
    in lesson 14 (selector / sequence / condition / action) and
    ``payload["label"]`` is the label on the slide.

    root (Selector)
    ├── flee_seq (Seq 逃跑)    -> is_hp_low?, flee
    ├── fight_seq (Seq 战斗)   -> can_see_hero?, attack
    └── patrol (Patrol)        -> wander, wait
    """

    def node(name: str, kind: str, label: str) -> TreeNode:
        return TreeNode(name, payload={"kind": kind, "label": label})

    root = node("root", "selector", "Selector 根")
    flee_seq = root.add(node("flee_seq", "sequence", "Seq 逃跑"))
    flee_seq.add(node("is_hp_low", "condition", "IsHpLow"))
    flee_seq.add(node("flee", "action", "Flee"))
    fight_seq = root.add(node("fight_seq", "sequence", "Seq 战斗"))
    fight_seq.add(node("can_see_hero", "condition", "CanSeeHero"))
    fight_seq.add(node("attack", "action", "Attack"))
    patrol = root.add(node("patrol", "sequence", "Patrol"))
    patrol.add(node("wander", "action", "Wander"))
    patrol.add(node("wait", "action", "Wait"))
    return root


def _emit_visit(recorder: EventRecorder, order: str, node: TreeNode, depth: int) -> None:
    recorder.emit(
        "visit",
        SOURCE,
        order=order,
        node=node.name,
        depth=depth,
        child_count=len(node.children),
    )


def traverse_preorder(
    root: TreeNode, recorder: EventRecorder | None = None, depth: int = 0
) -> list[str]:
    """Root, then each subtree left-to-right."""
    recorder = recorder or EventRecorder()
    # TODO: emit visit，然后先根、再从左到右递归子树（depth + 1）
    raise NotImplementedError("implement traverse_preorder")


def traverse_inorder(
    root: TreeNode, recorder: EventRecorder | None = None, depth: int = 0
) -> list[str]:
    """First child's subtree, root, then the remaining children.

    On a binary tree this is the usual left-root-right walk (sorted order for a
    BST). Inorder has no standard meaning for 3+ children; this is our convention.
    """
    recorder = recorder or EventRecorder()
    # TODO: 先递归第一个孩子，再 visit 自己，再递归其余孩子
    raise NotImplementedError("implement traverse_inorder")


def traverse_postorder(
    root: TreeNode, recorder: EventRecorder | None = None, depth: int = 0
) -> list[str]:
    """Children first, then the parent -- useful for "clear the dungeon from the leaves"."""
    recorder = recorder or EventRecorder()
    # TODO: 先递归全部孩子，最后 visit 自己
    raise NotImplementedError("implement traverse_postorder")


def traverse_bfs(root: TreeNode, recorder: EventRecorder | None = None) -> list[str]:
    """Level-order walk: all rooms at distance d before any room at distance d+1.

    For each dequeued node emit ``enqueue_level`` (``frontier`` = queue length
    right after the pop, before its children are queued), then ``visit``.
    """
    recorder = recorder or EventRecorder()
    # TODO: 用队列做层序遍历，队列里放 (节点, 深度)
    # TODO: 出队后先 emit enqueue_level(node, depth, frontier)，再 emit visit
    raise NotImplementedError("implement traverse_bfs")

