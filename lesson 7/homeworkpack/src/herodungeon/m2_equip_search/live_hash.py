"""第 7 次课当场写的哈希表：柜号、放入、查找、负载因子。

四个函数都还是空的，会抛 NotImplementedError。请只改这个文件。
本课用的哈希函数是「各字符编码之和再取余」，不是第 10 课的多项式哈希。
"""

from __future__ import annotations


def bucket_index(item_id: str, bucket_count: int) -> int:
    """柜号 = 各字符编码之和 % bucket_count。

    字符编码用 ord()。例如 "sword" 是 115+119+111+114+100 = 559，
    bucket_count 为 8 时柜号是 7。
    """
    
    for ch in item_id:
        total += ord(ch)
    return total % bucket_count


def put(buckets: list[list[str]], item_id: str) -> None:
    """把 item_id 挂到对应柜子那条链的末尾。

    buckets 的长度就是柜子数。同号的 ID 按放入顺序排在同一条链上。
    """
    idx = bucket_index(item_id, len(buckets))
    buckets[idx].append(item_id)


def get(buckets: list[list[str]], item_id: str) -> str | None:
    """沿链逐个比较。找到就返回这个 ID，没有就返回 None。不要抛异常。"""
    idx = bucket_index(item_id, len(buckets))
    for stored_id in buckets[idx]:
        if stored_id == item_id:
            return item_id
    return None


def load_factor(n: int, bucket_count: int) -> float:
    """负载因子 = 装备件数 / 柜子数。用普通除法，不要整除。"""
    return n / bucket_count
