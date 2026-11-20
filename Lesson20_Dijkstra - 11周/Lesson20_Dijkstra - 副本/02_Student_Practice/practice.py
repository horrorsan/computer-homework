"""30分钟：只补全dijkstra_path。5分钟初始化、15分钟核心、3分钟边界、7分钟测试修正。"""
import heapq
from support import RunSupport

def dijkstra_path(graph,start,goal,recorder=None):
    run=RunSupport('dijkstra',recorder,start,goal)
    if not graph.passable(start) or not graph.passable(goal):return run.failure(blocked=True)
    
    heap=[(0,start[0],start[1],start)]
    best={start:0}
    came_from={}
    closed=set()
    
    while heap:
        g,_r,_c,current=heapq.heappop(heap)

        if current in closed:
            continue
        closed.add(current)
   
        run.expand(current,len(heap),g)

        if current == goal:
            return run.success(came_from, start, goal, g)
    
        for nxt in graph.neighbors(current):
            candidate = g + graph.cost(current, nxt)

            if candidate < best.get(nxt, float('inf')):
                best[nxt] = candidate
                came_from[nxt] = current
                heapq.heappush(heap, (candidate, nxt[0], nxt[1], nxt))
                run.relax(nxt, current, candidate)
 
    return run.failure()
    
