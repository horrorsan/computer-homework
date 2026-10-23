from herodungeon.core.events import EventRecorder
from herodungeon.m3_behavior_tree import (
    TreeNode,
    build_dungeon_rooms,
    build_monster_tree_shape,
    traverse_bfs,
    traverse_inorder,
    traverse_postorder,
    traverse_preorder,
)


def _sample_tree() -> TreeNode:
    root = TreeNode("A")
    b = root.add(TreeNode("B"))
    b.add(TreeNode("D"))
    b.add(TreeNode("E"))
    root.add(TreeNode("C"))
    return root


def _binary_tree() -> TreeNode:
    root = TreeNode("D")
    b = root.add(TreeNode("B"))
    b.add(TreeNode("A"))
    b.add(TreeNode("C"))
    f = root.add(TreeNode("F"))
    f.add(TreeNode("E"))
    f.add(TreeNode("G"))
    return root


def _visits(recorder: EventRecorder) -> list:
    return [event for event in recorder.events if event.type == "visit"]


# --- the four orders on the lesson example --------------------------------


def test_preorder_visits_root_first() -> None:
    assert traverse_preorder(_sample_tree()) == ["A", "B", "D", "E", "C"]


def test_postorder_visits_root_last() -> None:
    assert traverse_postorder(_sample_tree()) == ["D", "E", "B", "C", "A"]


def test_inorder_walks_left_then_root() -> None:
    assert traverse_inorder(_sample_tree()) == ["D", "B", "E", "A", "C"]


def test_bfs_is_level_order() -> None:
    assert traverse_bfs(_sample_tree()) == ["A", "B", "C", "D", "E"]


def test_single_room_is_the_same_in_every_order() -> None:
    for walk in (traverse_preorder, traverse_inorder, traverse_postorder, traverse_bfs):
        assert walk(TreeNode("solo")) == ["solo"]


def test_inorder_on_binary_tree_is_sorted() -> None:
    assert traverse_inorder(_binary_tree()) == ["A", "B", "C", "D", "E", "F", "G"]


def test_walks_do_not_change_the_tree() -> None:
    tree = _sample_tree()
    for walk in (traverse_preorder, traverse_inorder, traverse_postorder, traverse_bfs):
        walk(tree)
    assert traverse_bfs(tree) == ["A", "B", "C", "D", "E"]
    assert [child.name for child in tree.children] == ["B", "C"]


# --- events -----------------------------------------------------------------


def test_visits_are_emitted() -> None:
    recorder = EventRecorder()
    traverse_preorder(_sample_tree(), recorder=recorder)

    visits = _visits(recorder)
    assert [event.payload["node"] for event in visits] == ["A", "B", "D", "E", "C"]


def test_visit_events_carry_order_and_depth() -> None:
    recorder = EventRecorder()
    traverse_postorder(_sample_tree(), recorder=recorder)

    visits = _visits(recorder)
    assert {event.payload["order"] for event in visits} == {"postorder"}
    assert [event.payload["node"] for event in visits] == ["D", "E", "B", "C", "A"]
    assert [event.payload["depth"] for event in visits] == [2, 2, 1, 1, 0]


def test_inorder_emits_one_visit_per_node() -> None:
    recorder = EventRecorder()
    traverse_inorder(_sample_tree(), recorder=recorder)

    visits = _visits(recorder)
    assert [event.payload["node"] for event in visits] == ["D", "B", "E", "A", "C"]
    assert {event.payload["order"] for event in visits} == {"inorder"}


def test_bfs_emits_enqueue_level_then_visit_for_each_node() -> None:
    recorder = EventRecorder()
    traverse_bfs(_sample_tree(), recorder=recorder)

    events = [event for event in recorder.events if event.type in {"enqueue_level", "visit"}]
    assert [event.type for event in events] == ["enqueue_level", "visit"] * 5
    levels = [event for event in events if event.type == "enqueue_level"]
    assert [event.payload["node"] for event in levels] == ["A", "B", "C", "D", "E"]
    assert [event.payload["depth"] for event in levels] == [0, 1, 1, 2, 2]
    assert [event.payload["frontier"] for event in levels] == [0, 1, 2, 1, 0]


# --- HeroDungeon trees (provided) ---------------------------------------------


def test_dungeon_rooms_in_three_orders() -> None:
    rooms = build_dungeon_rooms()

    assert traverse_preorder(rooms) == ["entrance", "hall", "armory", "crypt", "boss", "garden"]
    assert traverse_postorder(rooms) == ["armory", "boss", "crypt", "hall", "garden", "entrance"]
    assert traverse_bfs(rooms) == ["entrance", "hall", "garden", "armory", "crypt", "boss"]


def test_monster_tree_preorder_is_top_down_left_to_right() -> None:
    assert traverse_preorder(build_monster_tree_shape()) == [
        "root",
        "flee_seq",
        "is_hp_low",
        "flee",
        "fight_seq",
        "can_see_hero",
        "attack",
        "patrol",
        "wander",
        "wait",
    ]


def test_monster_tree_postorder_puts_every_parent_after_its_children() -> None:
    order = traverse_postorder(build_monster_tree_shape())

    assert order[-1] == "root"
    for parent, children in {
        "flee_seq": ("is_hp_low", "flee"),
        "fight_seq": ("can_see_hero", "attack"),
        "patrol": ("wander", "wait"),
    }.items():
        assert all(order.index(child) < order.index(parent) for child in children)


def test_monster_tree_levels_are_root_composites_leaves() -> None:
    recorder = EventRecorder()
    traverse_bfs(build_monster_tree_shape(), recorder=recorder)

    by_depth: dict[int, list[str]] = {}
    for event in _visits(recorder):
        by_depth.setdefault(event.payload["depth"], []).append(event.payload["node"])
    assert by_depth == {
        0: ["root"],
        1: ["flee_seq", "fight_seq", "patrol"],
        2: ["is_hp_low", "flee", "can_see_hero", "attack", "wander", "wait"],
    }
