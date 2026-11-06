"""本课用到的包和已经填好的表。已提供，不要修改。

表的含义：TABLE[i][w] = 只用前 i 个包、最多背 w 公斤时，最多能带走的金币数。
第 i 行对应第 i 个包（第 0 行表示“没有包”）。
"""
from __future__ import annotations

from models import Item

# 三个战利品包：A 重2公斤含3枚金币，B 重3公斤含4枚，C 重4公斤含5枚
ITEMS = (Item("a", "A", 2, 3), Item("b", "B", 3, 4), Item("c", "C", 4, 5))

#            限重： 0  1  2  3  4  5
TABLE = [
    [0, 0, 0, 0, 0, 0],   # 没有包
    [0, 0, 3, 3, 3, 3],   # 只用 A
    [0, 0, 3, 4, 4, 7],   # 用 A、B
    [0, 0, 3, 4, 5, 7],   # 用 A、B、C
]

# 课程仓库测试里用的四个包：再加上 D（重5公斤，含8枚金币）
ITEMS_WITH_D = ITEMS + (Item("d", "D", 5, 8),)
TABLE_WITH_D = [row[:] for row in TABLE] + [[0, 0, 3, 4, 5, 8]]
