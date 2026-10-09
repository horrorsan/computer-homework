"""第 7 次课当场检查。空函数应当失败。不要改这个文件。"""

from herodungeon.m2_equip_search.live_hash import (
    bucket_index,
    get,
    load_factor,
    put,
)

# 课件上的 6 个 ID，柜子数 8。柜号 = 字符编码之和 % 8。
DECK_IDS = ("sword", "shield", "bow", "dagger", "staff", "helmet")
DECK_BUCKETS = {
    "sword": 7,    # 559 % 8
    "shield": 1,   # 633 % 8
    "bow": 0,      # 328 % 8
    "dagger": 2,   # 618 % 8
    "staff": 4,    # 532 % 8
    "helmet": 7,   # 639 % 8
}


def test_bucket_index_matches_the_six_ids() -> None:
    for item_id, bucket in DECK_BUCKETS.items():
        assert bucket_index(item_id, 8) == bucket


def test_put_chains_sword_then_helmet_in_bucket_7() -> None:
    buckets: list[list[str]] = [[] for _ in range(8)]
    for item_id in DECK_IDS:
        put(buckets, item_id)

    assert buckets[7] == ["sword", "helmet"]
    assert buckets[0] == ["bow"]
    assert buckets[1] == ["shield"]
    assert buckets[2] == ["dagger"]
    assert buckets[4] == ["staff"]
    assert buckets[3] == []
    assert buckets[5] == []
    assert buckets[6] == []


def test_get_finds_helmet_and_missing_id_returns_none() -> None:
    buckets: list[list[str]] = [[] for _ in range(8)]
    for item_id in DECK_IDS:
        put(buckets, item_id)

    assert get(buckets, "helmet") == "helmet"
    assert get(buckets, "potion") is None


def test_load_factor_six_over_eight() -> None:
    assert load_factor(6, 8) == 0.75
