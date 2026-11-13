import json,os,urllib.request
E=os.environ["MAKEFUN_ENV_URL"]
def h(u,b):
 try:return json.load(urllib.request.urlopen(urllib.request.Request(E+u,data=json.dumps(b).encode(),headers={"content-type":"application/json"})))
 except:quit(u)
KN,BI,RO,QU,KI,PA=range(6)
D=[[],[-15,-17,15,17],[-15,-17,15,17,-1,1,-16,16],[-15,-17,15,17,-1,1,-16,16],[-1,-15,-17,-16,1,15,17,16],[-16,16]]
V=[0,330,500,900,0,100]
B=[0]*128;S=0;Ep=-1;Cr=0
def ld(f):
 global B,S,Ep,Cr
 B=[0]*128
 p=f.split();r=7;q=r*16
 for z in p[0]:
  if z=="/":r-=1;q=r*16
  elif z.isdigit():q+=int(z)
  else:
   B[q]={"n":KN,"b":BI,"r":RO,"q":QU,"k":KI,"p":PA}[z.lower()]|(8 if z.isupper() else 0);q+=1
 S=8 if p[1]=="w" else 0
 Ep=-1 if len(p)<4 or p[3]=="-" else ord(p[3][0])-97+(int(p[3][1])-1)*16
 Cr=sum({"K":1,"Q":2,"k":4,"q":8}.get(z,0)for z in p[2])
def fg(sq,sd_):
 for i in range(128):
  x=B[i]
  if not x or (x&8)!=(sd_&8):continue
  p=x&7
  if p==PA:
   for d in (15,17) if sd_&8 else (-17,-15):
    if i+d==sq:return 1
  elif p==KN:
   for d in (-33,-31,-18,-14,14,18,31,33):
    if i+d==sq:return 1
  elif p==KI:
   for d in (-1,-15,-17,-16,1,15,17,16):
    if i+d==sq:return 1
  else:
   for d in D[p]:
    t=i+d
    while not t&0x88:
     if t==sq:return 1
     if B[t]:break
     t+=d
 return 0
def fk(sd_):
 for i in range(128):
  if B[i]==(KI|sd_):return i
 return 0
def mg(ml):
 for i in range(128):
  x=B[i]
  if not x or (x&8)!=(S&8):continue
  p=x&7
  if p==PA:
   w=16 if S&8 else -16
   t=i+w
   if not t&0x88 and not B[t]:
    if (t&240)==0 or (t&240)==112:
     for p in (QU,RO,BI,KN):ml.append((i,t,p))
    else:ml.append((i,t,0))
   t=i+w*2
   sr=1 if S&8 else 6
   if (i&240)==sr*16 and not B[i+w] and not B[t]:ml.append((i,t,0))
   for d in (15,17) if S&8 else (-17,-15):
    t=i+d
    if not t&0x88 and B[t] and (B[t]&8)!=(S&8):ml.append((i,t,0))
   if Ep>=0:
    for d in (15,17) if S&8 else (-17,-15):
     if i+d==Ep:ml.append((i,Ep,0))
  elif p==KN:
   for d in (-33,-31,-18,-14,14,18,31,33):
    t=i+d
    if not t&0x88 and (not B[t] or (B[t]&8)!=(S&8)):ml.append((i,t,0))
  elif p==KI:
   for d in (-1,-15,-17,-16,1,15,17,16):
    t=i+d
    if not t&0x88 and (not B[t] or (B[t]&8)!=(S&8)):ml.append((i,t,0))
  else:
   for d in D[p]:
    t=i+d
    while not t&0x88:
     x=B[t]
     if x:
      if (x&8)!=(S&8):ml.append((i,t,0))
      break
     ml.append((i,t,0))
     t+=d
def mv(mm):
 global B,S,Ep,Cr
 i,t,p=mm
 x=B[i];B[i]=0;B[t]=x
 if x&7==PA:
  if abs(t-i)==32:Ep=(i+t)//2
  else:Ep=-1
  if (t&240)==0 or (t&240)==112:B[t]=(x&8)|p
 elif x&7==KI:
  Ep=-1
  if t-i==2:B[i+3]=0;B[t-1]=RO|(S&8)
  if t-i==-2:B[i-4]=0;B[t+1]=RO|(S&8)
  if i==4:Cr&=~3
  if i==112:Cr&=~12
 elif x&7==RO:
  Ep=-1
  if i==4:Cr&=~3
  if i==112:Cr&=~12
  if i==0:Cr&=~1
  if i==7:Cr&=~2
  if i==116:Cr&=~4
  if i==119:Cr&=~8
 if B[t]&7:Cr=0
 S^=8
def um(mm):
 global B,S,Cr
 i,t,p=mm
 x=B[t]
 if x&7==KI:
  if t-i==2:B[t-1]=0;B[i+3]=RO|(S^8&8)
  if t-i==-2:B[t+1]=0;B[i-4]=RO|(S^8&8)
 if x&7==PA and (t&240) in (0,112):x=(x&8)|PA
 B[t]=0;B[i]=x
 S^=8
def ev():
 sc=0
 for i in range(128):
  x=B[i]
  if not x:continue
  sc+=V[x&7]*(1 if x&8 else -1)
 return sc*(1 if S==8 else -1)
T={}
def ab(d,al,be):
 key=(tuple(B),S,Ep,Cr,d)
 if key in T:return T[key]
 if d==0:return ev()
 ml=[]
 mg(ml)
 if not ml:return -20000 if fg(fk(S),S^8) else 0
 bs=-99999
 for mm in ml:
  sv=S
  mv(mm)
  if fg(fk(sv),S):um(mm);continue
  v=-ab(d-1,-be,-al)
  um(mm)
  if v>bs:bs=v
  if v>al:al=v
  if al>=be:break
 T[key]=bs;return bs
def bm():
 ml=[]
 mg(ml)
 if not ml:return None
 bv=-99999;bm=None
 for d in (1,2,3,4):
  for mm in ml:
   sv=S
   mv(mm)
   if fg(fk(sv),S):um(mm);continue
   v=-ab(d-1,-99999,99999)
   um(mm)
   if v>bv:bv=v;bm=mm
 return bm
def uci(mm):
 i,t,p=mm
 return "abcdefgh"[i&7]+str(i//16+1)+"abcdefgh"[t&7]+str(t//16+1)+("qrbn"[p:p+1] if p else "")
g=h("/game",{})
while g.get("status")!="done":
 if g.get("status")=="your_move":
  ld(g["fen"])
  m=bm()
  if not m:h("/resign",{"game":g["game"]})
  else:
   u=uci(m)
   g=h("/move",{"game":g["game"],"move":u})
 else:
  g=h("/game",{})


