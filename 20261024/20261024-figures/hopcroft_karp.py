"""BFS layers and vertex-disjoint shortest augmenting paths."""
from pathlib import Path
OUT=Path(__file__).parent
P={'B':(55,90),'D':(55,235),'X':(215,90),'Z':(215,235),'A':(375,90),'C':(375,235),'Y':(535,90),'W':(535,235)}
EDGES=[('B','X'),('B','Z'),('D','Z'),('X','A'),('Z','C'),('A','Y'),('C','W')]
def text(x,y,s,size=22,color='#12374c'):
 return f'<text x="{x}" y="{y}" text-anchor="middle" font-family="Microsoft JhengHei,sans-serif" font-size="{size}" fill="{color}">{s}</text>'
for paths in [False,True]:
 z='<defs><marker id="arr" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L7,4 L0,8" fill="#738d9c"/></marker></defs>'
 for i,x in enumerate([55,215,375,535]):
  z+=f'<rect x="{x-36}" y="45" width="72" height="238" rx="12" fill="#e7eff5"/>'+text(x,28,'層 '+str(i),22)
 for u,v in EDGES:
  x,y=P[u];a,b=P[v];color='#168264' if (u,v) in [('X','A'),('Z','C')] else '#9bb0bd'
  if paths and (u,v)!=('B','Z'):color='#b76a16' if u in ['B','X','A'] else '#6654a4'
  # All edges run to the next BFS layer; the diagonal is a competing path.
  dx=a-x;dy=b-y;length=(dx*dx+dy*dy)**.5
  sx=x+dx/length*24;sy=y+dy/length*24;ex=a-dx/length*29;ey=b-dy/length*29
  z+=f'<path d="M{sx},{sy} L{ex},{ey}" stroke="{color}" stroke-width="{5 if paths and (u,v)!=("B","Z") else 3}" marker-end="url(#arr)" fill="none"/>'
 for label,(x,y) in P.items():
  color='#147c8c' if label in ['A','B','C','D'] else '#6654a4'
  z+=f'<circle cx="{x}" cy="{y}" r="23" fill="white" stroke="{color}" stroke-width="3"/>'+text(x,y+8,label,25,color)
 z+=text(300,325,'B–X–A–Y 與 D–Z–C–W' if paths else '未匹配左點 → 右點 → 已匹配左點 → 空右點',21)
 name='fig-hk-paths.svg' if paths else 'fig-hk-layers.svg'
 (OUT/name).write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 340">'+z+'</svg>',encoding='utf-8')

# Queue-trace frames: stable positions, newly discovered layer highlighted.
for stage in [1,2,3]:
 z='<defs><marker id="bfsarr" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L7,4 L0,8" fill="#738d9c"/></marker></defs>'
 layer={'B':0,'D':0,'X':1,'Z':1,'A':2,'C':2,'Y':3,'W':3}
 for i,x in enumerate([55,215,375,535]):z+=text(x,28,'dist = '+str(i) if i<=stage else 'dist = ∞',21)
 for u,v in EDGES:
  x,y=P[u];a,b=P[v];visible=layer[v]<=stage
  color=('#168264' if (u,v) in [('X','A'),('Z','C')] else '#738d9c') if visible else '#dce4e9'
  dx=a-x;dy=b-y;length=(dx*dx+dy*dy)**.5
  sx=x+dx/length*24;sy=y+dy/length*24;ex=a-dx/length*29;ey=b-dy/length*29
  z+=f'<path d="M{sx},{sy} L{ex},{ey}" stroke="{color}" stroke-width="3" marker-end="url(#bfsarr)" fill="none"/>'
 for label,(x,y) in P.items():
  discovered=layer[label]<=stage;new=layer[label]==stage
  fill='#fff0d9' if new else '#e5f2f0' if discovered else '#f1f3f5'
  color='#b76a16' if new else '#147c8c' if discovered else '#b8c4cd'
  z+=f'<circle cx="{x}" cy="{y}" r="23" fill="{fill}" stroke="{color}" stroke-width="3"/>'+text(x,y+8,label,25,color)
 z+=text(300,325,['發現 X、Z：佇列剩下 [X,Z]','發現 A、C：佇列剩下 [A,C]','發現 Y、W：最短路長度為 3'][stage-1],21)
 (OUT/('fig-hk-bfs-'+str(stage)+'.svg')).write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 340">'+z+'</svg>',encoding='utf-8')
