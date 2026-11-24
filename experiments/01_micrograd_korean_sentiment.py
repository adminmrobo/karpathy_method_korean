import sys,random,math,time,collections; sys.path.insert(0,'.')
from micrograd.engine import Value
from micrograd.nn import MLP
def load(p):
    r=[l.rstrip('\n').split('\t') for l in open(p,encoding='utf-8')][1:]
    return [(d,int(y)) for _,d,y in r if d.strip()]
tr=load('nsmc/ratings_train.txt'); te=load('nsmc/ratings_test.txt')
random.seed(42); random.shuffle(tr); random.shuffle(te)
vocab_part, train_part = tr[:50000], tr[50000:52000]; test=te[:1000]
pc=collections.Counter(); nc=collections.Counter()
for d,y in vocab_part:
    for ch in set(d): (pc if y else nc)[ch]+=1
P=sum(1 for _,y in vocab_part if y); N=len(vocab_part)-P
lo={ch:math.log((pc[ch]+1)/(P+2))-math.log((nc[ch]+1)/(N+2)) for ch in set(pc)|set(nc) if pc[ch]+nc[ch]>=200}
pos=sorted(lo,key=lambda c:-lo[c])[:30]; neg=sorted(lo,key=lambda c:lo[c])[:30]
print('pos',''.join(pos)); print('neg',''.join(neg))
PS,NS=set(pos),set(neg)
def feat(d):
    n=max(1,len(d)); return [10*sum(c in PS for c in d)/n, 10*sum(c in NS for c in d)/n]
Xtr=[feat(d) for d,_ in train_part]; ytr=[1 if y else -1 for _,y in train_part]
Xte=[feat(d) for d,_ in test]; yte=[1 if y else -1 for _,y in test]
random.seed(1337); model=MLP(2,[8,8,1]); print('params',len(model.parameters()))
def acc(X,Y): return sum((m:=model(list(map(Value,x))).data>0)==(y>0) for x,y in zip(X,Y))/len(Y)
print('step 0 test acc',acc(Xte,yte))
t0=time.time()
for k in range(201):
    idx=random.sample(range(len(Xtr)),64)
    sc=[model(list(map(Value,Xtr[i]))) for i in idx]
    loss=sum((1+-ytr[i]*s).relu() for i,s in zip(idx,sc))*(1/64)+1e-4*sum(p*p for p in model.parameters())
    model.zero_grad(); loss.backward()
    lr=0.5-0.45*k/200
    for p in model.parameters(): p.data-=lr*p.grad
    if k in (50,100,200): print(k,'loss %.3f'%loss.data,'train acc %.3f'%acc(Xtr[:500],ytr[:500]),'test acc %.3f'%acc(Xte,yte),'sec %.0f'%(time.time()-t0),flush=True)
for s in ['정말 최고의 영화','시간 아깝다 최악','그냥 그랬다']:
    f=feat(s); print(s,[round(v,2) for v in f],round(model(list(map(Value,f))).data,2))
