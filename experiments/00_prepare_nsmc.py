# 네이버 영화 리뷰(NSMC, CC0)에서 이 페이지가 쓴 두 데이터를 만든다.
# 사용: git clone https://github.com/e9t/nsmc && python3 00_prepare_nsmc.py nsmc/ratings.txt
import random, sys
rows = [l.rstrip('\n').split('\t') for l in open(sys.argv[1], encoding='utf-8')][1:]
rows = [(d.strip(), int(y)) for _, d, y in rows if d.strip()]
short = [d for d, _ in rows if 4 <= len(d) <= 12 and '\t' not in d]
random.seed(0); random.shuffle(short)
open('short_reviews.txt', 'w').write('\n'.join(short))          # makemore용 27,412줄
random.seed(1); r2 = rows[:]; random.shuffle(r2)
out, n = [], 0
for d, _ in r2:
    out.append(d); n += len(d) + 1
    if n >= 1_115_000: break
open('nsmc_1m.txt', 'w').write('\n'.join(out))                  # 토크나이저·nanoGPT용 111만 자
print(len(short), len(''.join(out)))
