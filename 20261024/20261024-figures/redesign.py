from pathlib import Path
from html import escape
import re
OUT=Path(__file__).parent
C="#147c8c"; N="#12374c"; G="#168264"; P="#6654a4"
def text(x,y,s,size=24,color=N): return f'<text x="{x}" y="{y}" text-anchor="middle" fill="{color}" font-size="{size}" font-family="Microsoft JhengHei,sans-serif">{escape(s)}</text>'
def line(x,y,a,b,color="#9ab3c2",w=3): return f'<path d="M{x},{y} L{a},{b}" stroke="{color}" stroke-width="{w}" fill="none"/>'
def box(x,y,s,w=140,color=C): return f'<rect x="{x-w/2}" y="{y-24}" width="{w}" height="48" rx="10" fill="#ffffff" stroke="{color}" stroke-width="3"/>'+text(x,y+8,s,22,color)
ACTIVE = set()
for source in OUT.parent.glob('*.md'):
 ACTIVE.update(re.findall(r'fig-[\w-]+\.svg', source.read_text(encoding='utf-8')))
def save(name,s):
 if name+'.svg' not in ACTIVE: return
 (OUT/(name+'.svg')).write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 360">'+s+'</svg>',encoding='utf-8')
def graph(name,matched=False,augment=False):
 s=''
 for i,j in [(0,0),(0,1),(1,0)]: s+=line(125,105+i*155,475,105+j*155,G if matched and (i,j) in [(0,1),(1,0)] else '#a9bdca',7 if matched else 3)
 for x,labs,col in [(125,['A','B'],C),(475,['X','Y'],P)]:
  for i,label in enumerate(labs): s+=box(x,105+i*155,label,76,col)
 s+=text(300,335,'A → Y，B → X：匹配數 2' if matched else '每條邊只連左右兩側',23)
 save(name,s)
graph('fig-bipartite');graph('fig-matched',True)
s=box(85,85,'B',70)+box(285,85,'X',70,P)+box(285,245,'A',70)+box(505,245,'Y',70,P)
s+=line(125,85,245,85,G,6)+line(285,110,285,220,P,6)+line(325,245,465,245,G,6)+text(300,335,'B–X–A–Y：交替翻轉，匹配數 +1',24)
save('fig-augment',s)
for name,no in [('fig-attack',False),('fig-noblock',True)]:
 s=box(90,130,'城堡',110)+box(510,130,'城堡',110)+line(150,130,450,130,C,5)
 s+=box(300,130,'無空格' if no else '可放障礙',160,P)+text(300,230,'座標差 = 1：無解' if no else '同一行／列，且中間無棋子',27)+text(300,290,'每一對都必須被阻擋',25)
 save(name,s)
s=line(65,170,535,170,C,8)+line(315,40,315,310,P,8)+box(315,170,'新障礙',120,G)+text(135,110,'橫向攻擊對',24,C)+text(450,270,'縱向攻擊對',24,P)+text(300,350,'一個交叉格 ↔ 一條匹配邊',24)
save('fig-why-h',s)
s=box(100,85,'L₁',90)+box(100,250,'L₂',90)+box(500,85,'R₁',90,P)+box(500,250,'R₂',90,P)
s+=line(150,85,450,85,G,6)+line(150,250,450,250,G,6)+line(150,250,450,85)+text(300,65,'(2,3)',22,G)+text(300,290,'(4,6)',22,G)
save('fig-hgraph',s)
s=''
for r in range(1,7):
 for c in range(1,8):
  x=110+c*48;y=5+r*48
  s+=text(x+24,25,str(c),18) if r==1 else ''; s+=text(140,y+33,str(r),18) if c==1 else ''; s+=f'<rect x="{x}" y="{y}" width="48" height="48" fill="white" stroke="#cbd9e2"/>'
  if (r,c) in [(2,1),(2,6),(4,1),(4,7),(1,3),(6,3),(6,6)]: s+=text(x+24,y+33,'城',22)
  if (r,c) in [(3,1),(3,4),(6,4)]: s+=text(x+24,y+33,'障',22,P)
  if (r,c) in [(2,3),(4,6)]: s+=text(x+24,y+33,'●',26,G)
save('fig-board',s)
for name in ['fig-tree','fig-path','fig-split','fig-sample-tree']:
 s=''; nodes=[(300,45,'[0,4]'),(160,145,'[0,2]'),(450,145,'[3,4]'),(85,255,'[0,1]'),(235,255,'[2]'),(390,255,'[3]'),(530,255,'[4]')]
 for a,b in [(0,1),(0,2),(1,3),(1,4),(2,5),(2,6)]:
  x,y,_=nodes[a];u,v,_=nodes[b];s+=line(x,y+24,u,v-24,G if name=='fig-path' and b in [1,4] else '#9ab3c2',5)
 for x,y,label in nodes:s+=box(x,y,label,125,G if name=='fig-split' and label in ['[2]','[3,4]'] else C)
 s+=text(300,335,{'fig-tree':'父節點計數 = 左孩子 + 右孩子','fig-path':'塗下標 2：只改根到葉子的鏈','fig-split':'[2,4] = [2] ∪ [3,4]','fig-sample-tree':'1 號掛 [2]、[3,4]；4 號掛 [0,2]'}[name],22)
 save(name,s)
s=''
for i in range(5):
 x=80+i*110;s+=f'<circle cx="{x}" cy="125" r="34" fill="'+('#c55362' if i!=2 else C)+'"/>'+text(x,190,str(i),25)
s+=text(300,270,'感測器監視一段閉區間 [l,r]',26)+text(300,320,'區間恰有一顆紅球才啟動',26,G)
save('fig-balls',s)
s=''
for i,(a,b) in enumerate([('0','0'),('1','1'),('2','2'),('4','2')]):
 x=80+i*145;s+=box(x,100,a,90)+text(x,170,'↓',32)+box(x,225,b,90,G)
s+=text(300,40,'真實紅球數 cnt',24)+text(300,305,'封頂貢獻 min(cnt, 2)',26,G)
save('fig-saturate',s)
s=''
for i,label in enumerate(['4','3','2','1','0']):
 x=65+i*118;s+=box(x,125,label,70,G if i>=3 else C)
 if i<4:s+=line(x+37,125,x+80,125,G if i>=2 else '#9ab3c2',5)
s+=text(300,220,'4→3、3→2：不通知',25)+text(300,275,'2→1：啟動候選；1→0：停止',25,G)+text(300,330,'每個節點一生最多通知兩次',24)
save('fig-notify',s)

# Revised teaching diagrams: real board cells and explicit bipartition bands.
s=''
for r in range(4):
 for c in range(7):
  x=70+c*65;y=25+r*65
  s+=f'<rect x="{x}" y="{y}" width="65" height="65" fill="white" stroke="#b7cdd8" stroke-width="2"/>'
  if (r,c) in [(0,0),(0,6),(2,0),(2,6)]:s+=text(x+32,y+42,'城',28,C)
  if (r,c)==(2,3):s+=box(x+32,y+32,'障',55,P)
s+=line(140,57,455,57,C,5)+text(300,145,'上排互攻：可在中間空格放障礙',23)+text(300,335,'下排已有障礙：不再形成攻擊對',23)
save('fig-attack',s)
for name,matched in [('fig-bipartite',False),('fig-matched',True)]:
 s='<rect x="35" y="40" width="150" height="270" rx="16" fill="#e0eff3"/><rect x="415" y="40" width="150" height="270" rx="16" fill="#ece9f7"/>'
 s+=text(110,75,'左點集 L',24,C)+text(490,75,'右點集 R',24,P)
 for i,j in [(0,0),(0,1),(1,0)]:
  on=matched and (i,j) in [(0,1),(1,0)]
  s+=line(150,130+i*120,450,130+j*120,G if on else '#a4b5c3',7 if on else 3)
 for x,labs,col in [(110,['A','B'],C),(490,['X','Y'],P)]:
  for i,label in enumerate(labs):s+=box(x,130+i*120,label,78,col)
 s+=text(300,345,'綠邊 A–Y、B–X：不共用端點' if matched else '只跨集合連邊；同側沒有邊',23)
 save(name,s)

# Same A/B/X example as the preceding board slide.
for name,matched in [('fig-bipartite',False),('fig-matched',True)]:
 s='<rect x="20" y="35" width="165" height="275" rx="16" fill="#e0eff3"/><rect x="415" y="35" width="165" height="275" rx="16" fill="#ece9f7"/>'
 s+=text(102,70,'橫向攻擊對',24,C)+text(498,70,'縱向攻擊對',24,P)
 s+=line(150,125,450,185,G if matched else C,7 if matched else 4)+line(150,255,450,185,'#a4b5c3',4)
 s+=box(102,125,'A',85,C)+box(102,255,'B',85,C)+box(498,185,'X',85,P)
 s+=text(300,125,'(2,3)',23,G if matched else C)+text(300,265,'(4,3)',23)
 s+=text(300,345,'選 A–X；B 單獨阻擋' if matched else '兩條邊共用右點 X',24)
 save(name,s)

# DFS augmentation, with a stable bipartite layout in every frame.
steps=[('起點：處理尚未匹配的 B',0),('DFS(B)：嘗試 X，但 X 已配給 A',1),('DFS(A)：跳過已訪問的 X，找到空著的 Y',2),('回傳成功：先將 Y 配給 A',3),('回到 DFS(B)：將 X 改配給 B',4)]
for k,(caption,state) in enumerate(steps,1):
 s='<rect x="25" y="30" width="145" height="265" rx="14" fill="#e0eff3"/><rect x="430" y="30" width="145" height="265" rx="14" fill="#ece9f7"/>'
 pos={'A':(100,105),'B':(100,245),'X':(500,105),'Y':(500,245)}
 for u,v in [('A','X'),('A','Y'),('B','X')]:
  active=(u,v) in ([('A','X')] if state<3 else [('A','X'),('A','Y')] if state==3 else [('A','Y'),('B','X')])
  x,y=pos[u];a,b=pos[v];s+=line(x+40,y,a-40,b,G if active else '#b5c6d1',7 if active else 3)
 for lab,(x,y) in pos.items():s+=box(x,y,lab,80,C if lab in 'AB' else P)
 if state in [1,2]:s+=text(300,80,'X 已訪問',22,P)
 if state==2:s+=text(300,280,'Y 尚未匹配',23,G)
 if state==3:s+=text(300,280,'遞迴回傳途中',23,G)
 s+=text(300,335,str(k)+' / 5　'+caption,21)
 save('fig-dfs-'+str(k),s)

# Two-by-two example shared by the board, graph, and DFS frames.
s=''
castles={(2,1),(2,7),(4,1),(4,5),(1,3),(6,3),(1,6),(3,6)}
blocks={(1,4),(3,1),(4,3)}
# (4,3) must remain an available intersection; use barriers outside all four target segments.
blocks={(1,4),(3,1)}
for r in range(1,7):
 for c in range(1,8):
  x=65+(c-1)*58;y=10+(r-1)*43
  fill='#e1eff3' if (r==2 and 1<c<7) or (r==4 and 1<c<5) else 'white'
  if (c==3 and 1<r<6) or (c==6 and 1<r<3):fill='#ece9f7'
  s+=f'<rect x="{x}" y="{y}" width="58" height="43" fill="{fill}" stroke="#b8cdd9"/>'
  if (r,c) in castles:s+=text(x+29,y+30,'城',24)
  if (r,c) in blocks:s+=text(x+29,y+30,'●',22,P)
  if (r,c) in [(2,3),(2,6),(4,3)]:s+=f'<circle cx="{x+29}" cy="{y+22}" r="12" fill="none" stroke="{G}" stroke-width="3"/>'
  if c==1:s+=text(45,y+29,str(r),19)
  if r==6:s+=text(x+29,291,str(c),19)
save('fig-concrete',s)
for name,matched in [('fig-bipartite',False),('fig-matched',True)]:
 s='<rect x="25" y="30" width="145" height="265" rx="14" fill="#e0eff3"/><rect x="430" y="30" width="145" height="265" rx="14" fill="#ece9f7"/>'
 pos={'A':(100,105),'B':(100,245),'X':(500,105),'Y':(500,245)}
 for u,v,label in [('A','X','(2,3)'),('A','Y','(2,6)'),('B','X','(4,3)')]:
  on=matched and (u,v) in [('A','Y'),('B','X')]
  x,y=pos[u];a,b=pos[v];s+=line(x+40,y,a-40,b,G if on else '#a7bac8',7 if on else 3)
 for lab,(x,y) in pos.items():s+=box(x,y,lab,80,C if lab in 'AB' else P)
 s+=text(300,335,'最大匹配：A–Y、B–X' if matched else '三條邊：A–X、A–Y、B–X',24)
 save(name,s)

# Labels aligned directly with their corresponding rows and columns.
p=OUT/'fig-concrete.svg'
s=p.read_text(encoding='utf-8')
# Shift the original board down to leave a clean column-label margin.
s=s.replace('viewBox="0 0 600 360"','viewBox="0 0 600 350"')
s=s.replace('>', '><g transform="translate(0,32)">',1).replace('</svg>','</g></svg>')
labels=text(515,115,'A',28,C)+text(515,201,'B',28,C)
labels+=text(210,25,'X',28,P)+text(384,25,'Y',28,P)
p.write_text(s.replace('</svg>',labels+'</svg>'),encoding='utf-8')

# Complete five-leaf trees, consistently shared by all E figures.
for name in ['fig-tree','fig-path','fig-split','fig-sample-tree']:
 nodes=[(300,35,'[0,4]'),(165,110,'[0,2]'),(440,110,'[3,4]'),(90,185,'[0,1]'),(245,185,'[2]'),(390,185,'[3]'),(520,185,'[4]'),(45,260,'[0]'),(135,260,'[1]')]
 links=[(0,1),(0,2),(1,3),(1,4),(2,5),(2,6),(3,7),(3,8)]
 z=''
 for a,b in links:
  x,y,_=nodes[a];u,v,_=nodes[b];on=name=='fig-path' and (a,b) in [(0,1),(1,4)]
  z+=line(x,y+19,u,v-19,G if on else '#b2c4cf',5 if on else 2)
 for i,(x,y,label) in enumerate(nodes):
  on=(name=='fig-path' and i in [0,1,4]) or (name=='fig-split' and i in [2,4])
  z+=f'<rect x="{x-42}" y="{y-18}" width="84" height="36" rx="7" fill="white" stroke="{G if on else C}" stroke-width="{4 if on else 2}"/>'+text(x,y+7,label,20,G if on else N)
 caption={'fig-tree':'五個葉子分別是下標 0、1、2、3、4','fig-path':'更新下標 2：綠色節點計數各減 1','fig-split':'[2,4] = [2] ∪ [3,4]：綠框為分解節點','fig-sample-tree':'1 號：[2]、[3,4]；2 號：[2]、[3]'}[name]
 z+=text(300,320,caption,21)
 if name=='fig-sample-tree':z+=text(300,350,'3 號：[3]；4 號：[0,2]',21)
 save(name,z)
# A stale matchR entry is not a second valid matched edge.
p=OUT/'fig-dfs-4.svg';z=p.read_text(encoding='utf-8')
z=z.replace('d="M140,105 L460,105" stroke="'+G+'" stroke-width="7"','d="M140,105 L460,105" stroke="#a4b5c3" stroke-width="4" stroke-dasharray="9 7"')
p.write_text(z,encoding='utf-8')
