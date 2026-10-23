import pytest

from herodungeon.core.events import EventRecorder
from herodungeon.m2_equip_search import (
    EQUIPMENT_FIELDS,
    FIELD_RANGES,
    VECTOR_FIELDS,
    Equipment,
    generate_equipment,
    load_equipment,
)

SWORD = {
    "item_id": "EQ-1",
    "name": "骑士长剑",
    "power": 260,
    "speed": 40,
    "weight": 6,
    "durability": 70,
    "rarity": 3,
}


def _record(**changes):
    record = dict(SWORD)
    record.update(changes)
    return record


# --- provided scaffolding: the unified field set -------------------------------


def test_unified_field_set_and_ranges() -> None:
    assert EQUIPMENT_FIELDS == (
        "item_id",
        "name",
        "power",
        "speed",
        "weight",
        "durability",
        "rarity",
    )
    assert VECTOR_FIELDS == ("power", "speed", "weight", "durability", "rarity")
    assert FIELD_RANGES["power"] == (1, 1000)
    assert FIELD_RANGES["rarity"] == (1, 5)
    assert set(FIELD_RANGES) == set(VECTOR_FIELDS)


def test_to_vector_order() -> None:
    sword = Equipment(**SWORD)

    assert sword.to_vector() == (260, 40, 6, 70, 3)
    assert sword.to_record() == SWORD


@pytest.mark.parametrize(
    "changes",
    [{"power": 0}, {"power": 1001}, {"rarity": 6}, {"speed": True}, {"weight": 2.5}, {"item_id": ""}],
)
def test_equipment_rejects_bad_values(changes) -> None:
    with pytest.raises(ValueError):
        Equipment(**_record(**changes))


def test_generate_equipment_is_reproducible_and_in_range() -> None:
    first = generate_equipment(50)
    second = generate_equipment(50, seed=42)

    assert first == second
    assert first != generate_equipment(50, seed=7)
    assert [item.item_id for item in first[:3]] == ["EQ-000000", "EQ-000001", "EQ-000002"]
    assert len({item.item_id for item in first}) == 50
    for item in first:
        for field_name, (low, high) in FIELD_RANGES.items():
            assert low <= getattr(item, field_name) <= high
    assert generate_equipment(0) == []
    with pytest.raises(ValueError):
        generate_equipment(-1)


# --- lesson 9: load_equipment (入库) -------------------------------------------


def test_load_round_trips_records_in_order() -> None:
    catalogue = generate_equipment(20)
    records = [item.to_record() for item in catalogue]

    loaded = load_equipment(records)

    assert loaded == catalogue
    assert all(isinstance(item, Equipment) for item in loaded)


def test_load_accepts_any_iterable_and_does_not_mutate_input() -> None:
    records = [_record(item_id="a"), _record(item_id="b")]
    snapshot = [dict(record) for record in records]

    loaded = load_equipment(record for record in records)

    assert [item.item_id for item in loaded] == ["a", "b"]
    assert records == snapshot


def test_load_emits_one_ingest_event_per_record() -> None:
    recorder = EventRecorder()

    load_equipment([_record(item_id="a"), _record(item_id="b"), _record(item_id="c")], recorder=recorder)

    ingests = [event for event in recorder.events if event.type == "ingest"]
    assert [event.payload["item_id"] for event in ingests] == ["a", "b", "c"]
    assert recorder.events[-1].type == "ingest_done"
    assert recorder.events[-1].payload["count"] == 3


def test_load_rejects_missing_field() -> None:
    record = _record()
    del record["durability"]

    with pytest.raises(ValueError):
        load_equipment([record])


def test_load_rejects_unknown_field() -> None:
    with pytest.raises(ValueError):
        load_equipment([_record(attack=12)])


def test_load_rejects_duplicate_item_id() -> None:
    with pytest.raises(ValueError):
        load_equipment([_record(item_id="dup"), _record(item_id="dup", name="另一把")])


def test_load_rejects_out_of_range_value() -> None:
    with pytest.raises(ValueError):
        load_equipment([_record(rarity=9)])


def test_load_empty_batch() -> None:
    recorder = EventRecorder()

    assert load_equipment([], recorder=recorder) == []
    assert recorder.events[-1].type == "ingest_done"
    assert recorder.events[-1].payload["count"] == 0
