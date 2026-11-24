# nanochat의 rustbpe로 사전 크기별 한국어/영어 토큰당 글자 수를 잰다. (nanochat 저장소 안에서 실행)
import time, sys
from nanochat.tokenizer import RustBPETokenizer
ko = open(sys.argv[1]).read(); en = open(sys.argv[2]).read()   # nsmc_1m.txt, tinyshakespeare input.txt
s = '이 영화 정말 재밌어요 강력 추천합니다'
for V in (512, 1024, 2048, 4096, 8192, 16384):
    for nm, txt in (('KO', ko), ('EN', en)):
        t0 = time.time(); tok = RustBPETokenizer.train_from_iterator(iter(txt.split('\n')), vocab_size=V); dt = time.time() - t0
        n = len(tok.encode(txt)); extra = ''
        if nm == 'KO': ids = tok.encode(s); extra = str(len(ids)) + ' ' + '|'.join(tok.decode([i]) for i in ids)
        print(V, nm, 'chars/tok %.2f' % (len(txt) / n), 'sec %.2f' % dt, extra)
