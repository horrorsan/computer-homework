# 第 9 次课幻灯纲要（20 页）

1. 标题：装备类 + 入库 + 快速排序
2. 回顾第 8 次课：排序 + 二分 + 选型；冒泡/选择只作对照
3. 场景：一批原始装备记录要先入库，再按战力排行
4. 统一字段：item_id / name / power / speed / weight / durability / rarity
5. 取值范围：power 1–1000，rarity 1–5，其余见 lesson-09.md
6. to_vector：五维向量，为第 10 次课相似度 Top-K 铺路
7. generate_equipment(n, seed=42)：同一 seed 同一目录
8. 入库三类错误：缺字段 / 未知字段 / 重复 item_id
9. 事件 ingest / ingest_done
10. 冒泡、选择对照：O(n²) 比较次数（老师代码，不计分）
11. 快排思想：选枢轴 → 划分 → 递归两段
12. 枢轴规则：三数取中，已排序输入不退化
13. 划分过程：compare / swap / place_pivot
14. 降序：只把比较方向反过来
15. 快排不稳定；大量相同键时的代价
16. 只改 equipment.py 的 load_equipment 和 quicksort.py
17. 禁止 sorted() / list.sort()
18. 两组测试：test_equipment / test_quicksort
19. 今晚不写二分、哈希、Top-K
20. 提交
