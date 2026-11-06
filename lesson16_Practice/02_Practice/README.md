# 第16课练习：从填好的表里，找出带走了哪几个包

读完这份说明，你就知道每一步要做什么、看到什么算对。

## 先回顾：动态规划在做什么（四句话）
1. 拆小问题：只用前几个包、最多背几公斤，最多能带走几枚金币？
2. 存进表里：每个小问题的答案存在表里的一格。
3. 比较选择：每格比较“不拿”和“拿”，留下金币更多的。
4. 旧答案反复用：算过的格子不重算，后面的格子直接读。

今天新学的是：表填好以后，怎样倒着找出带走了哪几个包。这叫“回溯”。

## 文件夹里有什么
| 文件 | 作用 | 要不要改 |
|---|---|---|
| `lesson16_practice.py` | 你写代码的地方 | 要，只改 `reconstruct_items` |
| `lesson_data.py` | 包和已经填好的表 | 不改，要看一看 |
| `self_check.py` | 检查你写得对不对 | 不改，运行它 |
| `demo.py` | 看不同限重下带走哪些包 | 不改，运行它 |
| `models.py`、`events.py` | 包和事件记录的定义 | 不改 |
| `checks.py`、`tests/`、`pytest.ini` | 检查内容 | 不改 |
| `README.md` | 本说明 | 不改 |

## 准备工作
1. 在本文件夹打开终端。Windows可在地址栏输入 `cmd`；macOS用终端 `cd` 进入本文件夹。
2. 运行 `python --version`，需要Python 3.10或更高。若找不到`python`，试`python3`或`py`。
3. 运行`dir`（Windows）或`ls`（macOS），确认能看到`lesson16_practice.py`。

## 第0步：看懂表，再预测（在纸上写，不要运行代码）

包A重2公斤、含3枚金币；包B重3公斤、含4枚；包C重4公斤、含5枚。每包只能拿一次，不能拆开。

| 能用的包 / 限重 | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---:|---:|---:|---:|---:|---:|
| 没有包 | 0 | 0 | 0 | 0 | 0 | 0 |
| 只用A | 0 | 0 | 3 | 3 | 3 | 3 |
| 用A、B | 0 | 0 | 3 | 4 | 4 | 7 |
| 用A、B、C | 0 | 0 | 3 | 4 | 5 | 7 |

- 行：现在能用哪些包。第i行对应第i个包（第1行是包A）。
- 列：最多能背几公斤。
- 格：这种条件下最多能带走几枚金币。
- 一格是一个完整问题，要一起看“能用哪些包”和“限重多少”。只用A、限重2和只用A、限重5是不同问题，但答案碰巧都为3；用A、B、限重5是另一个问题，答案是7。

**回溯：从最后一行、限重那一列开始。每一步看、比、动：**
1. 看：现在能用哪些包？还能背几公斤？
2. 比：当前格和上一行同一列。
3. 动：相同→不拿，限重不变；不同→拿，限重减去包的重量。**限重变了，下一步要换到新的那一列。**然后都去上一行。

为什么？上一行表示“不用这个包”。两格相同，说明不用它也能得到同样金币，不拿；两格不同，说明用了它结果更好，拿。

### 限重5公斤例子（课件有箭头）
| 看哪个包 | 当前格 | 上一行同列 | 结果 | 决定 | 之后限重 |
|---|---:|---:|---|---|---|
| C | 7 | 7 | 相同 | 不拿 | 5（不变） |
| B | 7 | 3 | 不同 | 拿 | 5−3=2，换到“2”列 |
| A | 3 | 0 | 不同 | 拿 | 2−2=0，结束 |

### 请预测
1. 限重4：第一步看C，当前格和上一行同列各是多少？拿不拿？为什么？
2. 限重4：最后带走哪个包？几枚金币？
3. 限重3：最后带走哪个包？几枚金币？

## 第1步：先运行一次
```bash
python self_check.py
```
10项都会显示`⏳`，最后“通过 0 / 10 项”，因为函数还没写。

| 符号 | 意思 |
|---|---|
| ✓ | 通过，继续 |
| ⏳ | 函数还没写 |
| ✗ | 结果不对；看“应该是……，你的结果是……” |

## 第2步：在纸上回溯一次（限重5，约3分钟）
| 包 | 当前格 | 上一行同列 | 相同/不同 | 拿/不拿 | 还剩几公斤 |
|---|---:|---:|---|---|---:|
| C（第3行） | ? | ? | ? | ? | ? |
| B（第2行） | ? | ? | ? | ? | ? |
| A（第1行） | ? | ? | ? | ? | ? |

注意：拿了B后，剩余限重从5变成2。**下一步看“只用A”这一行、限重2这一列**，不是继续看限重5列。核对时再对照上面的限重5示例。

## 第3步：写 `reconstruct_items`（约12分钟）
1. 打开`lesson16_practice.py`，找到`def reconstruct_items`。
2. 写完后，删除该函数里的`raise NotImplementedError`。
3. 参考骨架填空：
```python
def reconstruct_items(items, table, capacity, recorder=None):
    if recorder is None:
        recorder = EventRecorder()
    chosen = []
    weight = ____                       # 当前还剩几公斤？
    for i in range(____, 0, -1):        # 从最后一行往上
        item = items[____]              # 第i行对应 items[i - 1]
        if table[i][weight] ____ table[i - 1][weight]:
            chosen.append(____)
            recorder.emit("choose", SOURCE, item_id=____, remaining=____)
            weight = ____               # 拿了以后，下一步要换到新的限重列
        else:
            recorder.emit("skip_item", SOURCE, item_id=____, remaining=weight)
    recorder.emit("chosen", SOURCE, item_ids=____)
    return ____
```
只读`table`；一行对应一个包；不拿时限重不变，拿了才扣重量。`remaining`记录拿包之后剩余的限重。

## 第4步：逐项检查
```bash
python self_check.py
```
最后应为`通过 10 / 10 项`。先看“带走哪些包”，再看“规则和记录”。如果不通过，回到纸上过程找出第一次走错的格子。

## 第5步：看演示（约2分钟）
```bash
python demo.py
```
限重5：跳过C、拿B（剩2公斤）、拿A（剩0公斤），带走A、B，共5公斤、7枚金币。
限重4：带走C，共4公斤、5枚金币。
限重3：带走B，共3公斤、4枚金币。

## 第6步：自己加一个测试（约8分钟）
新建`my_test.py`，不要原样照抄；换一个你自己的输入：
```python
from copy import deepcopy
from lesson16_practice import reconstruct_items
from lesson_data import ITEMS, TABLE

# 例：只用A和B，限重2，想想应该带走什么
chosen = reconstruct_items(ITEMS[:2], deepcopy(TABLE[:3]), 2)
ids = [item.item_id for item in chosen]
assert ids == ["a"], "限重2公斤放不下B，只能带A"
print("我的测试通过", ids)
```
运行`python my_test.py`。写清输入、预测和理由，以及它检查了哪种容易错的情况。

## 第7步：保存，并写一句话（约3分钟）
最后运行一次`python self_check.py`，再写：
> 我写代码时哪里错过？为什么会错？后来怎样改对？

没有犯错也没关系，写一条容易错的地方和避免办法。

## 遇到问题怎么办
| 看到什么 | 怎么处理 |
|---|---|
| `⏳ 请先完成 reconstruct_items` | 函数还没写；完成后删掉TODO抛出的`raise NotImplementedError` |
| 当前格和结果不对 | 对照纸上的逐步回溯，找到第一步不一致处 |
| 回溯后表变了 | 删除对`table[...]`的写入，表只读 |
| `IndexError` | 检查`items[i - 1]`以及重量扣减后的新列 |
| `EventRecorder`未定义 | 不要删除文件开头的导入 |
| `ModuleNotFoundError` | 终端切回包含`lesson16_practice.py`的文件夹 |
| 找不到`python` | 试`python3`或`py` |

## 做完以后的检查表
- [ ] 运行前写了预测和理由。
- [ ] 纸上走完限重5的三步，并在拿B后换到限重2列。
- [ ] `python self_check.py`显示10/10。
- [ ] 能解释为什么拿B后限重从5变成2。
- [ ] 函数没有修改表。
- [ ] 写了自己的测试和一句修正说明。

## 接下来还要做（不在这30分钟里）
1. 在课程仓`dp.py`完成`knapsack_01`和格子事件。
2. 在`visualizer.py`完成`print_tree`和`to_mermaid`。
3. 整理报告。

## 复制函数时注意
`dp.py`里的`reconstruct_items`函数名、参数、返回值相同。复制时只复制函数体，并使用文件顶部已经导入的`Item`和`EventRecorder`。本练习包的`self_check.py`、`checks.py`不要复制进去。
