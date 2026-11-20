"""30分钟：只补全bfs_path。5分钟初始化、15分钟循环、3分钟边界、7分钟测试修正。"""
from collections import deque
from support import RunSupport

def bfs_path(graph,start,goal,recorder=None):
    # 开始实现时删除下一行；保留函数名、参数和返回格式。
    run=RunSupport('bfs',recorder,start,goal)
    if not graph.passable(start) or not graph.passable(goal):return run.failure(blocked=True)
    
    frontier = deque([start])

    seen = {start}

    came_from = {}

    while frontier:
        current = frontier.popleft()
        run.expand(current,len(frontier))
        if current == goal:
            return run.success(came_from,start,goal)
        
        for nxt in graph.neighbors(current):
            if nxt in seen:
                continue

            seen.add(nxt)
            came_from[nxt] = current
            frontier.append(nxt)
            run.enqueue(nxt,current,len(frontier))

    return run.failure()



