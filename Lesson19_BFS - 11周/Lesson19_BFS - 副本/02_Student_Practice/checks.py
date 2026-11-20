from practice import bfs_path
from provided import *
TITLE='第19课 BFS'
def launch(graph,start,goal):
    rec=EventRecorder();result=bfs_path(graph,start,goal,rec);return result,rec

def a():
    r,_=launch(room_graph(),S,T)
    assert r.cost==2 and r.path==(S,B,T),f'应S→B→T，2步，你的是{r.path}, {r.cost}'
def b():
    _,rec=launch(room_graph(),S,T)
    got=[NAMES[tuple(e.payload['node'])] for e in rec.events if e.type=='expand']
    assert got==['S','A','B','C','T'],f'应取出S,A,B,C,T，你的是{got}'
def c():
    r,_=launch(dungeon19(),(0,0),(2,2))
    want=((0,0),(0,1),(0,2),(1,2),(2,2))
    assert r.path==want and r.cost==4,f'北东南西应走{want}，4步，你的是{r}'
def d():
    r,rec=launch(dungeon19(),(0,0),(2,2))
    nodes=[tuple(e.payload['node']) for e in rec.events if e.type=='enqueue']
    assert len(nodes)==7 and len(nodes)==len(set(nodes)),f'应7次新邻居入队且不重复，你的是{nodes}'
    assert (r.expanded,r.generated)==(8,8),f'应取出8、生成8，你的是{r.expanded},{r.generated}'
def e():
    r,_=launch(GridGraph(3,3),(1,1),(1,1))
    assert r.found and r.cost==0 and r.path==((1,1),),f'应原地0步，你的是{r}'
def f():
    r,rec=launch(GridGraph(3,3,blocked={(0,1),(1,1),(2,1)}),(0,0),(2,2))
    assert not r.found and r.path==() and r.cost is None,f'应无路，你的是{r}'
    assert rec.events[-1].type=='no_path','末事件应no_path'
def g():
    r,_=launch(GridGraph(3,3,blocked={(0,0)}),(0,0),(2,2))
    assert not r.found and r.expanded==0,f'起点为墙应直接失败，你的是{r}'
def h():
    r,_=launch(GridGraph(5,4),(0,0),(3,4))
    assert r.cost==7,f'应7步，你的是{r.cost}'
def i():
    graph=dungeon20();r,_=launch(graph,(0,0),(0,4))
    assert r.cost==4 and path_cost(graph,r.path)==25,f'BFS应4步/25点，你的是{r}'
def j():
    _,rec=launch(room_graph(),S,T)
    assert rec.events[-1].type=='path_found','末事件应path_found'
    assert any(e.type=='reconstruct' for e in rec.events),'应记录回溯'
CHECKS=[('A路线',a),('A取出顺序',b),('B路径',c),('不重复与计数',d),('原地0步',e),('不可达',f),('墙端点',g),('开阔7步',h),('忽略权重',i),('事件回溯',j)]
