第 7 次课 · 教室现场课
哈希表与精确查找

用自己的电脑。先交纸笔，再写四个函数。编码不单独计分，算进第 11 次课小项目 2 的验收。代码写不完，纸上过程仍要交。

纸笔：

1. 15 分钟。写出 sword、shield、bow、dagger、staff、helmet 的字符编码相加过程，再 % 8。只写柜号不算完。字符编码用 ord()，a=97，后面每个字母 +1。
2. 20 分钟。按这个顺序放进 8 个柜子（0 到 7）。画出 sword 和 helmet 都进 7 号柜的那条链。走一遍 get("helmet") 比了几次、先碰到谁。再写一个不存在的 ID 会怎样。
3. 10 分钟。算 n=6、M=8 的负载因子。再写一个坏哈希：不管什么 ID 都进 0 号柜，说明这时为什么又变回一个一个找。

当场编码（约 35 分钟），只改 src/herodungeon/m2_equip_search/live_hash.py：

- bucket_index(item_id, bucket_count)：字符编码之和再取余
- put(buckets, item_id)：接到那条链的末尾
- get(buckets, item_id)：沿链找到就返回这个 ID，没有就返回 None，不要抛异常
- load_factor(n, bucket_count)：n / 柜子数

检查：sword 和 helmet 都在 7 号柜，链是 ["sword", "helmet"]；get("helmet") 得到 "helmet"；不存在的 ID 得到 None；load_factor(6, 8) 是 0.75。

pytest tests/test_live_hash-第7课.py

不要写插入排序、归并排序，也不要写第 10 课的 EquipmentIndex。仓库里没有答案。阅读 docs/lesson-07.md。
