import numpy as np, struct, os
txt=open('input.txt').read()
chars=sorted(set(txt)); V=len(chars); stoi={c:i for i,c in enumerate(chars)}
ids=np.array([stoi[c] for c in txt],dtype=np.uint16); n=int(len(ids)*0.9)
os.makedirs('dev/data/tinyshakespeare',exist_ok=True)
def wtok(path,a):
    h=np.zeros(256,dtype=np.int32); h[0]=20240520;h[1]=1;h[2]=len(a)
    with open(path,'wb') as f: f.write(h.tobytes()); f.write(a.tobytes())
wtok('dev/data/tinyshakespeare/tiny_shakespeare_train.bin',ids[:n]); wtok('dev/data/tinyshakespeare/tiny_shakespeare_val.bin',ids[n:])
h=np.zeros(256,dtype=np.uint32); h[0]=20240328;h[1]=2;h[2]=V;h[3]=stoi['\n']
with open('gpt2_tokenizer.bin','wb') as f:
    f.write(h.tobytes())
    for c in chars: b=c.encode(); f.write(bytes([len(b)])); f.write(b)
maxT,L,NH,C,Vp=64,4,4,128,128
rng=np.random.default_rng(1337)
sizes=[Vp*C,maxT*C,L*C,L*C,L*3*C*C,L*3*C,L*C*C,L*C,L*C,L*C,L*4*C*C,L*4*C,L*C*4*C,L*C,C,C]
ones={2,8,14}; zeros={3,5,7,9,11,13,15}
ps=[]
for i,s in enumerate(sizes):
    if i in ones: ps.append(np.ones(s,np.float32))
    elif i in zeros: ps.append(np.zeros(s,np.float32))
    else:
        std=0.02/np.sqrt(2*L) if i in (6,12) else 0.02
        ps.append((rng.standard_normal(s)*std).astype(np.float32))
h=np.zeros(256,dtype=np.int32); h[0]=20240326;h[1]=3;h[2:8]=[maxT,V,L,NH,C,Vp]
with open('gpt2_124M.bin','wb') as f:
    f.write(h.tobytes()); [f.write(p.tobytes()) for p in ps]
print("V",V,"params",sum(sizes))
