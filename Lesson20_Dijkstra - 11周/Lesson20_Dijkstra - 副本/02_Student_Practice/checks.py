from practice import dijkstra_path
from provided_bfs import bfs_path
from provided import *
TITLE='第20课 Dijkstra'
def launch(graph,start,goal):
    rec=EventRecorder();result=dijkstra_path(graph,start,goal,rec);return result,rec

def a():
    r,_=launch(road_graph(),S,T)
    assert r.cost==4 and r.path==(S,B,A,T),f'应S→B→A→T，4点，你的是{r}'
def b():
    _,rec=launch(road_graph(),S,T)
    aa=[e.payload['g'] for e in rec.events if e.type=='relax' and tuple(e.payload['node'])==A]
    tt=[e.payload['g'] for e in rec.events if e.type=='relax' and tuple(e.payload['node'])==T]
    assert aa==[4,3] and tt==[8,4],f'应A:4→3，T:8→4，你的是{aa}, {tt}'
def c():
    r,rec=launch(road_graph(),S,T)
    ex=[NAMES[tuple(e.payload['node'])] for e in rec.events if e.type=='expand']
    assert ex==['S','B','A','T'],f'应有效取出S,B,A,T，你的是{ex}'
    assert (r.expanded,r.generated)==(4,6),f'应扩展4、生成6，你的是{r.expanded},{r.generated}'
def d():
    graph=dungeon20();r,_=launch(graph,(0,0),(0,4));bb=bfs_path(graph,(0,0),(0,4))
    assert r.cost==6 and r.length==6 and path_cost(graph,r.path)==6,f'应6步/6点，你的是{r}'
    assert path_cost(graph,bb.path)==25,'BFS对照应25点'
def e():
    r,_=launch(GridGraph(3,3),(1,1),(1,1))
    assert r.found and r.path==((1,1),) and r.cost==0,f'应原地0点，你的是{r}'
def f():
    r,rec=launch(GridGraph(3,3,blocked={(0,1),(1,1),(2,1)}),(0,0),(2,2))
    assert not r.found and r.path==() and r.cost is None,f'应无路，你的是{r}'
    assert rec.events[-1].type=='no_path','末事件应no_path'
def g():
    r,_=launch(GridGraph(3,3,blocked={(0,0)}),(0,0),(2,2))
    assert not r.found and r.expanded==0,f'墙起点应失败，你的是{r}'
def h():
    graph=RoadGraph([(S,A,5),(S,B,1),(B,A,1),(A,T,6)],directed=True)
    r,rec=launch(graph,S,T)
    ns=[tuple(e.payload['node']) for e in rec.events if e.type=='expand']
    assert r.cost==8 and len(ns)==len(set(ns)),f'旧A应跳过，总代价8，你的是{r}, {ns}'
def i():
    graph=RoadGraph([(S,A,0),(A,T,1),(S,T,3)],directed=True)
    r,_=launch(graph,S,T)
    assert r.cost==1,f'零权边应1点，你的是{r.cost}'
def j():
    graph=road_graph();r,rec=launch(graph,S,T)
    assert path_cost(graph,r.path)==r.cost,f'路径重算与报告不符：{r}'
    assert rec.events[-1].type=='path_found','末事件应path_found'
CHECKS=[('A路线4点',a),('两次松弛',b),('有效取出计数',c),('B地形对比',d),('原地0点',e),('不可达',f),('墙端点',g),('跳过旧记录',h),('零权边',i),('路径费用一致',j)]
