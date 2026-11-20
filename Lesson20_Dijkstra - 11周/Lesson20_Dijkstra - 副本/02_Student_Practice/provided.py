"""已提供：图、结果、事件、路径回溯。坐标(行,列)，网格邻居北东南西。Python3.10+。"""
from dataclasses import dataclass,field

@dataclass(frozen=True)
class AlgorithmEvent:
    type:str
    step:int
    source:str
    payload:dict

class EventRecorder:
    def __init__(self):self._events=[]
    @property
    def events(self):return tuple(self._events)
    def emit(self,event_type,source,**payload):
        e=AlgorithmEvent(event_type,len(self._events),source,payload)
        self._events.append(e)
        return e

@dataclass
class GridGraph:
    width:int
    height:int
    blocked:set=field(default_factory=set)
    weights:dict=field(default_factory=dict)
    default_weight:int=1
    def __post_init__(self):
        if self.width<=0 or self.height<=0:raise ValueError('尺寸必须为正')
        if self.default_weight<=0 or any(x<=0 for x in self.weights.values()):raise ValueError('地形费用必须为正')
    def in_bounds(self,node):
        r,c=node
        return 0<=r<self.height and 0<=c<self.width
    def passable(self,node):return self.in_bounds(node) and node not in self.blocked
    def weight(self,node):return self.weights.get(node,self.default_weight)
    def cost(self,current,nxt):return self.weight(nxt)
    def neighbors(self,node):
        r,c=node
        for dr,dc in [(-1,0),(0,1),(1,0),(0,-1)]:
            nxt=(r+dr,c+dc)
            if self.passable(nxt):yield nxt
    def cells(self):
        for r in range(self.height):
            for c in range(self.width):yield r,c

class RoadGraph:
    """道路按边收费，方向由directed决定。节点仍为二元组以兼容寻路接口。"""
    def __init__(self,edges,directed=False):
        self.adj={}
        for a,b,c in edges:
            if c<0:raise ValueError('本例不接受负费用')
            self.adj.setdefault(a,[]).append((b,c));self.adj.setdefault(b,[])
            if not directed:self.adj[b].append((a,c))
    def passable(self,node):return node in self.adj
    def neighbors(self,node):return (n for n,c in self.adj[node])
    def cost(self,current,nxt):return next(c for n,c in self.adj[current] if n==nxt)

@dataclass(frozen=True)
class PathResult:
    algorithm:str
    found:bool
    path:tuple
    cost:int|None
    expanded:int
    generated:int
    @property
    def length(self):return max(0,len(self.path)-1) if self.path else 0

def reconstruct_path(came_from,start,goal,recorder,source):
    """已提供：沿来源倒着回起点，再反转。"""
    if goal!=start and goal not in came_from:return []
    path=[goal];current=goal
    while current!=start:
        current=came_from[current];path.append(current)
        recorder.emit('reconstruct',source,node=list(current))
    path.reverse()
    return path

def path_cost(graph,path):return sum(graph.cost(a,b) for a,b in zip(path,path[1:]))
S=(0,0);A=(0,1);B=(1,0);C=(0,2);T=(0,3)
NAMES={S:'S',A:'A',B:'B',C:'C',T:'T'}
def room_graph():return RoadGraph([(S,A,1),(S,B,1),(A,C,1),(B,T,1),(C,T,1)])
def road_graph():return RoadGraph([(S,A,4),(S,B,1),(B,A,2),(B,T,7),(A,T,1)],directed=True)
def dungeon19():return GridGraph(3,3,blocked={(1,1)})
def dungeon20():return GridGraph(5,3,weights={(0,1):8,(0,2):8,(0,3):8})
