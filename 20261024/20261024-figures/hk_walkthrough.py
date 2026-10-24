"""Simple two-channel Hopcroft–Karp walkthrough, SVG only."""
from pathlib import Path
OUT=Path(__file__).parent
GREEN='#168264'; INK='#12374c'; ORANGE='#b76a16'; PURPLE='#6654a4'
def text(x,y,s,size=22,color=INK):return f'<text x="{x}" y="{y}" text-anchor="middle" fill="{color}" font-size="{size}" font-family="Microsoft JhengHei,sans-serif">{s}</text>'
def circle(x,y,s,fill='white',stroke='#147c8c'):
 return f'<circle cx="{x}" cy="{y}" r="28" fill="{fill}" stroke="{stroke}" stroke-width="3"/>'+text(x,y+9,s,27,stroke)
def save(name,s):
 (OUT/name).write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 360">'+s+'</svg>',encoding='utf-8')
# Initial conventional left/right layout.
pos={'A':(115,55),'B':(115,135),'C':(115,225),'D':(115,305),'X':(505,55),'Y':(505,135),'Z':(505,225),'W':(505,305)}
z=text(115,20,'左點',19)+text(505,20,'右點',19)
for u,v in [('A','X'),('A','Y'),('B','X'),('C','Z'),('C','W'),('D','Z')]:
 x,y=pos[u];a,b=pos[v];matched=(u,v) in [('A','X'),('C','Z')]
 z+=f'<path d="M{x+28},{y} L{a-28},{b}" stroke="{GREEN if matched else "#b5c4ce"}" stroke-width="{7 if matched else 3}"/>'
for label,(x,y) in pos.items():z+=circle(x,y,label,stroke='#147c8c' if label in 'ABCD' else PURPLE)
z+=text(310,352,'原配對 A–X、C–Z',22,GREEN)
save('fig-hk-start.svg',z)
for name,stage,path in [('fig-hk-clear-bfs-0.svg',0,0),('fig-hk-clear-bfs-2.svg',2,0),('fig-hk-clear-bfs-3.svg',3,0),('fig-hk-clear-dfs-1.svg',3,1),('fig-hk-clear-dfs-2.svg',3,2)]:
 z='<defs><marker id="arrow" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0,0 L6,3.5 L0,7" fill="#859daa"/></marker></defs>'
 for row,labels in enumerate([['B','X','A','Y'],['D','Z','C','W']]):
  y=100+row*155
  for i in range(3):
   x=70+165*i;col=ORANGE if path==1 and row==0 else PURPLE if path==2 and row==1 else GREEN if i==1 else '#9fb4c1'
   if not path and i>=stage:col='#d1dce3'
   if path==2 and row==0:col='#d1dce3'
   z+=f'<path d="M{x+30},{y} L{x+132},{y}" stroke="{col}" stroke-width="{6 if path and row==path-1 else 4}" marker-end="url(#arrow)"/>'
  for i,label in enumerate(labels):
   x=70+165*i;known=i<=stage
   col=ORANGE if path==1 and row==0 else PURPLE if path==2 and row==1 else '#147c8c' if known else '#b8c6cf'
   z+=circle(x,y,label,'#fff3e1' if path and row==path-1 else 'white',col)
   z+=text(x,y-47,'dist='+str(i) if known else 'dist=∞',20,col)
   z+=text(x,y+52,'左點' if i%2==0 else '右點',19)
 if path:z+=text(320,22,'固定本輪 BFS 層次；上列已用完' if path==2 else '固定本輪 BFS 層次',19)
 caption='配對不變：A–X、C–Z' if not path else '本次路徑 B–X–A–Y；翻轉後匹配數 3' if path==1 else '本次路徑 D–Z–C–W；翻轉後匹配數 4'
 z+=text(320,350,caption,22,GREEN)
 save(name,z)

for chosen in [False,True]:
 z='<defs><marker id="ov" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0,0 L6,3.5 L0,7" fill="#859daa"/></marker></defs>'
 positions={'B':(70,100),'X':(235,100),'A':(400,100),'Y':(565,100),'D':(70,255),'Z':(235,255),'C':(400,255),'W':(565,255)}
 for u,v in [('B','X'),('X','A'),('A','Y'),('D','Z'),('Z','C'),('C','W'),('B','Z')]:
  x,y=positions[u];a,b=positions[v];color=GREEN if (u,v) in [('X','A'),('Z','C')] else '#9fb4c1'
  if chosen:color=PURPLE if u in ['D','Z','C'] else ORANGE if (u,v)!=('B','Z') else '#c5d0d7'
  if not chosen and (u,v)==('B','Z'):color=ORANGE
  dx=a-x;dy=b-y;l=(dx*dx+dy*dy)**.5
  z+=f'<path d="M{x+dx/l*30},{y+dy/l*30} L{a-dx/l*34},{b-dy/l*34}" stroke="{color}" stroke-width="4" marker-end="url(#ov)" fill="none"/>'
 for label,(x,y) in positions.items():z+=circle(x,y,label)
 z+=text(320,32,'固定 BFS 層次：0 → 1 → 2 → 3',22)
 z+=text(320,350,'先選下列 Q，再由 B 改走上列 R' if chosen else '新增 B→Z：P 與 Q 共用 Z、C、W',22)
 save('fig-hk-overlap-reroute.svg' if chosen else 'fig-hk-overlap-candidates.svg',z)
