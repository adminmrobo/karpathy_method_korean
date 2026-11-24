import sys, random, time; sys.path.insert(0,'.')
from micrograd.engine import Value
from micrograd.nn import MLP
# README example check
a=Value(-4.0); b=Value(2.0); c=a+b; d=a*b+b**3; c+=c+1; c+=1+c+(-a); d+=d*2+(b+a).relu(); d+=3*d+(b-a).relu()
e=c-d; f=e**2; g=f/2.0; g+=10.0/f; g.backward()
print("README g=%.4f a.grad=%.4f b.grad=%.4f"%(g.data,a.grad,b.grad))
# moons-like toy: 2 classes ring-ish, seed fixed
random.seed(1337)
import math
X=[];y=[]
for i in range(100):
    t=random.uniform(0,math.pi); cls=i%2
    if cls==0: X.append([math.cos(t)+random.gauss(0,.1), math.sin(t)+random.gauss(0,.1)]); y.append(-1)
    else: X.append([1-math.cos(t)+random.gauss(0,.1), 0.5-math.sin(t)+random.gauss(0,.1)]); y.append(1)
model=MLP(2,[16,16,1]); print("params",len(model.parameters()))
t0=time.time()
for k in range(100):
    scores=[model(list(map(Value,x))) for x in X]
    losses=[(1+-yi*s).relu() for yi,s in zip(y,scores)]
    reg=1e-4*sum(p*p for p in model.parameters())
    loss=sum(losses)*(1.0/len(losses))+reg
    acc=sum((yi>0)==(s.data>0) for yi,s in zip(y,scores))/len(y)
    model.zero_grad(); loss.backward()
    lr=1.0-0.9*k/100
    for p in model.parameters(): p.data-=lr*p.grad
    if k in (0,9,49,99): print(k, round(loss.data,4), acc)
print("sec",round(time.time()-t0,1))
