"""Generate the Hungarian/DFS overview and density comparison (standard library only)."""
from pathlib import Path
OUT=Path(__file__).parent
TEAL='#147c8c'; PURPLE='#6654a4'; GREEN='#168264'; ORANGE='#b76a16'
def text(x,y,value,size=22,color='#12374c'):
 return f'<text x="{x}" y="{y}" text-anchor="middle" fill="{color}" font-size="{size}" font-family="Microsoft JhengHei,sans-serif">{value}</text>'
def line(x,y,a,b,color='#a6bbc9',width=3,extra=''):
 return f'<path d="M{x},{y} L{a},{b}" stroke="{color}" stroke-width="{width}" fill="none" {extra}/>'
def node(x,y,label,color):
 return f'<circle cx="{x}" cy="{y}" r="26" fill="white" stroke="{color}" stroke-width="3"/>'+text(x,y+8,label,24,color)
def save(name,body):
 (OUT/name).write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 340">'+body+'</svg>',encoding='utf-8')
for dense in [False,True]:
 z=text(100,28,'左點集',22,TEAL)+text(500,28,'右點集',22,PURPLE)
 edges=[(i,j) for i in range(4) for j in range(4)] if dense else [(0,0),(0,1),(1,1),(2,2),(3,3)]
 for i,j in edges:z+=line(128,75+i*70,472,75+j*70)
 for i in range(4):z+=node(100,75+i*70,'ABCD'[i],TEAL)+node(500,75+i*70,'XYZW'[i],PURPLE)
 z+=text(300,335,'16 條實際邊' if dense else '5 條實際邊',22)
 save('fig-matching-dense.svg' if dense else 'fig-matching-sparse.svg',z)
z='<defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8" fill="none" stroke="'+ORANGE+'" stroke-width="1.6"/></marker></defs>'
z+=text(100,32,'左點集',22,TEAL)+text(500,32,'右點集',22,PURPLE)
z+=line(130,105,470,105,GREEN,8)+line(130,105,470,245)+line(130,245,470,105)
# Alternating path directions: nonmatched L→R, matched R→L.
z+=line(460,88,140,88,ORANGE,3,'marker-end="url(#arrow)"')
z+=line(130,230,458,112,ORANGE,3,'marker-end="url(#arrow)"')
z+=line(130,120,458,238,ORANGE,3,'marker-end="url(#arrow)"')
for x,y,l,c in [(100,105,'A',TEAL),(100,245,'B',TEAL),(500,105,'X',PURPLE),(500,245,'Y',PURPLE)]:z+=node(x,y,l,c)
z+=text(300,305,'A–X  →  A–Y、B–X',24,GREEN)+text(300,335,'匹配數 1 → 2',23)
save('fig-hungarian-intro.svg',z)
