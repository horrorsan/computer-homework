from herodungeon.m3_behavior_tree import (
    Action,
    BehaviorStatus,
    Condition,
    Selector,
    Sequence,
    TickContext,
)


def _tree() -> Sequence:
    return Sequence(
        "root",
        [
            Condition("visible", lambda world: bool(world["visible"])),
            Selector(
                "tactic",
                [
                    Sequence(
                        "retreat",
                        [
                            Condition("low_hp", lambda world: world["hp"] < 30),
                            Action("flee"),
                        ],
                    ),
                    Action("attack"),
                ],
            ),
        ],
    )


def test_low_hp_monster_flees() -> None:
    ctx = TickContext(world={"visible": True, "hp": 10})
    status = _tree().tick(ctx)

    assert status is BehaviorStatus.SUCCESS
    assert ctx.world["last_action"] == "flee"
    assert any(
        event.type == "tick" and event.payload["node"] == "flee"
        for event in ctx.recorder.events
    )


def test_healthy_monster_attacks() -> None:
    ctx = TickContext(world={"visible": True, "hp": 80})
    status = _tree().tick(ctx)

    assert status is BehaviorStatus.SUCCESS
    assert ctx.world["last_action"] == "attack"


def test_hidden_hero_fails_at_root_condition() -> None:
    ctx = TickContext(world={"visible": False, "hp": 10})
    status = _tree().tick(ctx)

    assert status is BehaviorStatus.FAILURE
    assert "last_action" not in ctx.world


def test_status_bubbles_through_composites() -> None:
    ctx = TickContext(world={"visible": True, "hp": 10})
    _tree().tick(ctx)

    ticks = [event for event in ctx.recorder.events if event.type == "tick"]
    assert ticks[-1].payload["node"] == "root"
    assert ticks[-1].payload["status"] == "success"


# --- lesson 14 deck: the minimal runnable tree and its three blackboards ---------


def _deck_tree() -> Selector:
    """Slide "最小可跑树": Selector(Seq(IsHpLow, Flee), Seq(CanSeeHero, Attack), Patrol)."""
    return Selector(
        "root",
        [
            Sequence(
                "flee_seq",
                [Condition("is_hp_low", lambda world: world["hp"] < 30), Action("flee")],
            ),
            Sequence(
                "fight_seq",
                [Condition("can_see_hero", lambda world: bool(world["can_see"])), Action("attack")],
            ),
            Action("patrol"),
        ],
    )


def _ticks(ctx: TickContext) -> list[tuple[str, str]]:
    return [
        (event.payload["node"], event.payload["status"])
        for event in ctx.recorder.events
        if event.type == "tick"
    ]


def test_deck_blackboard_low_hp_flees() -> None:
    ctx = TickContext(world={"hp": 20, "can_see": True})

    assert _deck_tree().tick(ctx) is BehaviorStatus.SUCCESS
    assert ctx.world["last_action"] == "flee"


def test_deck_blackboard_healthy_and_seeing_attacks() -> None:
    ctx = TickContext(world={"hp": 80, "can_see": True})

    assert _deck_tree().tick(ctx) is BehaviorStatus.SUCCESS
    assert ctx.world["last_action"] == "attack"


def test_deck_blackboard_nobody_in_sight_patrols() -> None:
    ctx = TickContext(world={"hp": 80, "can_see": False})

    assert _deck_tree().tick(ctx) is BehaviorStatus.SUCCESS
    assert ctx.world["last_action"] == "patrol"


def test_execution_path_is_recorded_leaf_to_root() -> None:
    ctx = TickContext(world={"hp": 80, "can_see": True})
    _deck_tree().tick(ctx)

    assert _ticks(ctx) == [
        ("is_hp_low", "failure"),
        ("flee_seq", "failure"),
        ("can_see_hero", "success"),
        ("attack", "success"),
        ("fight_seq", "success"),
        ("root", "success"),
    ]


def test_enter_events_follow_preorder_of_visited_composites() -> None:
    ctx = TickContext(world={"hp": 80, "can_see": False})
    _deck_tree().tick(ctx)

    enters = [
        (event.payload["node"], event.payload["kind"])
        for event in ctx.recorder.events
        if event.type == "enter"
    ]
    assert enters == [
        ("root", "selector"),
        ("flee_seq", "sequence"),
        ("fight_seq", "sequence"),
    ]


# --- Sequence / Selector semantics --------------------------------------------------


def _counting(name: str, status: BehaviorStatus, calls: list[str]) -> Action:
    def effect(world: dict) -> BehaviorStatus:
        calls.append(name)
        return status

    return Action(name, effect)


def test_sequence_stops_at_first_failure() -> None:
    calls: list[str] = []
    seq = Sequence(
        "seq",
        [
            _counting("a", BehaviorStatus.SUCCESS, calls),
            _counting("b", BehaviorStatus.FAILURE, calls),
            _counting("c", BehaviorStatus.SUCCESS, calls),
        ],
    )

    assert seq.tick(TickContext(world={})) is BehaviorStatus.FAILURE
    assert calls == ["a", "b"]


def test_sequence_succeeds_only_when_all_children_succeed() -> None:
    calls: list[str] = []
    seq = Sequence(
        "seq",
        [_counting("a", BehaviorStatus.SUCCESS, calls), _counting("b", BehaviorStatus.SUCCESS, calls)],
    )

    assert seq.tick(TickContext(world={})) is BehaviorStatus.SUCCESS
    assert calls == ["a", "b"]


def test_selector_stops_at_first_success() -> None:
    calls: list[str] = []
    sel = Selector(
        "sel",
        [
            _counting("a", BehaviorStatus.FAILURE, calls),
            _counting("b", BehaviorStatus.SUCCESS, calls),
            _counting("c", BehaviorStatus.SUCCESS, calls),
        ],
    )

    assert sel.tick(TickContext(world={})) is BehaviorStatus.SUCCESS
    assert calls == ["a", "b"]


def test_selector_fails_only_when_all_children_fail() -> None:
    calls: list[str] = []
    sel = Selector(
        "sel",
        [_counting("a", BehaviorStatus.FAILURE, calls), _counting("b", BehaviorStatus.FAILURE, calls)],
    )

    assert sel.tick(TickContext(world={})) is BehaviorStatus.FAILURE
    assert calls == ["a", "b"]


def test_running_is_passed_up_and_stops_both_composites() -> None:
    calls: list[str] = []
    seq = Sequence(
        "seq",
        [_counting("wind_up", BehaviorStatus.RUNNING, calls), _counting("after", BehaviorStatus.SUCCESS, calls)],
    )
    sel = Selector(
        "sel",
        [_counting("swing", BehaviorStatus.RUNNING, calls), _counting("backup", BehaviorStatus.SUCCESS, calls)],
    )

    assert seq.tick(TickContext(world={})) is BehaviorStatus.RUNNING
    assert sel.tick(TickContext(world={})) is BehaviorStatus.RUNNING
    assert calls == ["wind_up", "swing"]


def test_empty_composites() -> None:
    assert Sequence("empty_seq").tick(TickContext(world={})) is BehaviorStatus.SUCCESS
    assert Selector("empty_sel").tick(TickContext(world={})) is BehaviorStatus.FAILURE


def test_composite_records_its_own_tick_with_kind() -> None:
    ctx = TickContext(world={})
    Selector("sel", [Sequence("seq", [Action("go")])]).tick(ctx)

    kinds = [
        (event.payload["node"], event.payload["kind"])
        for event in ctx.recorder.events
        if event.type == "tick"
    ]
    assert kinds == [("go", "action"), ("seq", "sequence"), ("sel", "selector")]


def test_conditions_only_read_the_blackboard() -> None:
    world = {"hp": 80, "can_see": False}
    ctx = TickContext(world=world)
    Sequence(
        "checks",
        [Condition("alive", lambda w: w["hp"] > 0), Condition("can_see_hero", lambda w: w["can_see"])],
    ).tick(ctx)

    assert world == {"hp": 80, "can_see": False}
