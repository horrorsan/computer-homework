# 第19课：从纸上推演到核心实现

## 先做20分钟手写
使用另发的Worksheet.pdf：A题10分钟、B题10分钟。先预测、填过程与解释，不先运行代码抄答案。

## 开始30分钟代码
在本目录打开终端，运行 `python self_check.py`。初始10项全⏳，通过0/10是正常的。
只改 `practice.py` 的 `bfs_path(graph,start,goal,recorder=None)`。
- 5分钟：开始实现时删除开头提示raise；完成初始化。
- 15分钟：核心循环，对照手写表逐轮动作。
- 3分钟：成功、原地、墙端点、不可达的返回分支。
- 7分钟：保存→自测→读提示→修正；不能改checks来绕过错误。
完整参考应10/10；中途通过多少不作未经验证的承诺。

## 已提供，不要改
provided.py：GridGraph、RoadGraph、PathResult、事件与回溯。support.py：RunSupport日志、计数和结果辅助。
节点坐标(行,列)；网格邻居北东南西；统一取出有效目标才返回。BFS的cost是步数。

## 运行与观察
`python demo.py` 看网格；`python demo.py --case main` 看生活主例；加 `--animate` 可逐帧显示有效取出。
观察：搜索检查的所有格子不等于角色最终路线。

## 自己加一个变式
先预测，再修改tests/test_mine.py，去掉skip并写assert。可选安装pytest：`python -m pip install pytest`，运行 `python -m pytest -q`。
默认自写模板1项跳过，不是已经通过；补完后应不再跳过。自测不需要安装pytest。

## 报错对照
⏳：还留着提示raise；开始实现时删掉。
✗：看预期与实际，对照对应手写行。
No module named pytest：安装pytest或只运行self_check。
找不到practice.py：终端当前目录应是本文件夹。
程序卡住：先停掉，查发现登记、closed或来源形成了环；不能把卡住当通过。

## 提交检查表
- [ ] 两题手写都先预测并解释
- [ ] 只改核心函数，自测10/10
- [ ] 看过demo并能解释路线
- [ ] 保存一条真实失败与修正理由
- [ ] 写一句独立解释，能处理一种新地图

环境：Python3.10+，标准库可完成自测和演示。练习包独立于远端代码库；迁回课程实现的注意事项由老师说明。
