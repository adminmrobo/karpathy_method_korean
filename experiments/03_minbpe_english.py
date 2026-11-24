import sys,time; sys.path.insert(0,'.')
from minbpe import BasicTokenizer, RegexTokenizer
text=open('tests/taylorswift.txt',encoding='utf-8').read()
print("chars",len(text),"bytes",len(text.encode()))
for cls in (BasicTokenizer,RegexTokenizer):
    t=cls(); t0=time.time(); t.train(text,512); dt=time.time()-t0
    ids=t.encode(text); ok=t.decode(ids)==text
    print(cls.__name__,"vocab512 tokens",len(ids),"ratio %.2f"%(len(text.encode())/len(ids)),"roundtrip",ok,"sec %.1f"%dt)
# korean sample
t=RegexTokenizer(); t.train(text,512)
k="안녕하세요 연구실입니다"; print("ko bytes",len(k.encode()),"tokens",len(t.encode(k)))
e="hello world"; print("en bytes",len(e.encode()),"tokens",len(t.encode(e)))
print([t.decode([i]) for i in t.encode("hello world")])
