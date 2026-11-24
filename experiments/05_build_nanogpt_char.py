import sys,time,torch
src=open('train_gpt2.py').read().split('\n')
code='\n'.join([l for l in src[:203] if 'hellaswag' not in l])
ns={'master_process':False}; exec(code,ns); GPT,GPTConfig=ns['GPT'],ns['GPTConfig']
txt=open('input.txt').read(); ch=sorted(set(txt)); stoi={c:i for i,c in enumerate(ch)}
data=torch.tensor([stoi[c] for c in txt]); n=int(.9*len(data)); tr,va=data[:n],data[n:]
torch.manual_seed(1337)
cfg=GPTConfig(block_size=64,vocab_size=len(ch),n_layer=4,n_head=4,n_embd=128)
m=GPT(cfg); print("params",sum(p.numel() for p in m.parameters()))
opt=m.configure_optimizers(weight_decay=0.1,learning_rate=1e-3,device_type='cpu')
def batch(d,B=12,T=64):
    ix=torch.randint(len(d)-T-1,(B,)); return torch.stack([d[i:i+T] for i in ix]),torch.stack([d[i+1:i+T+1] for i in ix])
@torch.no_grad()
def ev():
    m.eval(); l=sum(m(*batch(va))[1].item() for _ in range(20))/20; m.train(); return l
t0=time.time()
for s in range(2001):
    if s%500==0: print(s,"val %.4f"%ev())
    x,y=batch(tr); _,loss=m(x,y); opt.zero_grad(); loss.backward(); torch.nn.utils.clip_grad_norm_(m.parameters(),1.0); opt.step()
print("sec",round(time.time()-t0))
