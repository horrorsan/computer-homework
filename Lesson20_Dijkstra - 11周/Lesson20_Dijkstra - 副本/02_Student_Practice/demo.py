"""完成后运行python demo.py；--animate逐帧输出有效取出；--case main/grid切换。"""
import argparse,time
from provided import *
from practice import dijkstra_path

class DungeonDemo:
    def run(self,case,animate):
        graph=road_graph() if case=='main' else dungeon20()
        start,goal=(S,T) if case=='main' else ((0,0),(0,4))
        recorder=EventRecorder();result=dijkstra_path(graph,start,goal,recorder)
        for ev in recorder.events:
            if ev.type in ['expand','enqueue','relax']:
                print(ev.type,ev.payload)
                if animate and ev.type=='expand':time.sleep(.15)
        print('路线:',result.path,'步数:',result.length,'报告代价:',result.cost)
        print('路径实际费用:',path_cost(graph,result.path),'有效取出:',result.expanded)
        if isinstance(graph,GridGraph):
            for r in range(graph.height):
                print(' '.join('#' if (r,c) in graph.blocked else '*' if (r,c) in result.path else str(graph.weight((r,c))) for c in range(graph.width)))

        if case=='grid':
            from provided_bfs import bfs_path
            b=bfs_path(graph,start,goal)
            print('BFS对照:',b.length,'步，',path_cost(graph,b.path),'点')
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--case',choices=['main','grid'],default='grid');p.add_argument('--animate',action='store_true');a=p.parse_args();DungeonDemo().run(a.case,a.animate)
