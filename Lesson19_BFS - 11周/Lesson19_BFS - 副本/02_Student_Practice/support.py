"""事件与结果构建已经提供，不要修改。把30分钟留给算法判断。"""
from provided import EventRecorder,PathResult,reconstruct_path

class RunSupport:
    def __init__(self,algorithm,recorder,start,goal):
        self.algorithm=algorithm;self.source='m4.'+algorithm
        self.recorder=recorder or EventRecorder();self.expanded=0;self.generated=1
        self.recorder.emit('start',self.source,start=list(start),goal=list(goal))
    def expand(self,node,frontier_size,g=None):
        self.expanded+=1
        payload=dict(node=list(node),expanded=self.expanded,frontier_size=frontier_size)
        if g is not None:payload['g']=g
        self.recorder.emit('expand',self.source,**payload)
    def enqueue(self,node,parent,size):
        self.generated+=1
        self.recorder.emit('enqueue',self.source,node=list(node),parent=list(parent),frontier_size=size)
    def relax(self,node,parent,g):
        self.generated+=1
        self.recorder.emit('relax',self.source,node=list(node),parent=list(parent),g=g)
    def success(self,came_from,start,goal,cost=None):
        path=reconstruct_path(came_from,start,goal,self.recorder,self.source)
        cost=len(path)-1 if cost is None else cost
        self.recorder.emit('path_found',self.source,cost=cost,length=len(path)-1,expanded=self.expanded)
        return PathResult(self.algorithm,True,tuple(path),cost,self.expanded,self.generated)
    def failure(self,blocked=False):
        self.recorder.emit('no_path',self.source,expanded=self.expanded)
        return PathResult(self.algorithm,False,(),None,self.expanded,0 if blocked else self.generated)
