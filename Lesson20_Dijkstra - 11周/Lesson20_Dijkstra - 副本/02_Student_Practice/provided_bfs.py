"""已提供：队列维持层次；首次发现登记来源。"""
from collections import deque
from provided import EventRecorder,PathResult,reconstruct_path
SOURCE='m4.bfs'

def bfs_path(graph,start,goal,recorder=None):
    recorder=recorder or EventRecorder()
    if not graph.passable(start) or not graph.passable(goal):
        recorder.emit('no_path',SOURCE,reason='blocked_endpoint')
        return PathResult('bfs',False,(),None,0,0)
    recorder.emit('start',SOURCE,start=list(start),goal=list(goal))
    frontier=deque([start]);seen={start};came_from={}
    expanded=0;generated=1
    while frontier:
        current=frontier.popleft()
        expanded+=1
        recorder.emit('expand',SOURCE,node=list(current),expanded=expanded,frontier_size=len(frontier))
        if current==goal:
            path=reconstruct_path(came_from,start,goal,recorder,SOURCE)
            steps=len(path)-1
            recorder.emit('path_found',SOURCE,cost=steps,length=steps,expanded=expanded)
            return PathResult('bfs',True,tuple(path),steps,expanded,generated)
        for nxt in graph.neighbors(current):
            if nxt in seen:continue
            seen.add(nxt)
            came_from[nxt]=current
            frontier.append(nxt);generated+=1
            recorder.emit('enqueue',SOURCE,node=list(nxt),parent=list(current),frontier_size=len(frontier))
    recorder.emit('no_path',SOURCE,expanded=expanded)
    return PathResult('bfs',False,(),None,expanded,generated)
