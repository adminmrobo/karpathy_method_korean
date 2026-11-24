# 카파시의 방법론 — 한국어 데이터로 검증하다

안드레이 카파시가 공개한 무료 학습 저장소 7개(micrograd → makemore → minbpe → nanoGPT → build-nanogpt → llm.c → nanochat)를
연구소가 GPU 없는 CPU에서 직접 돌리고, **네이버 영화 리뷰(NSMC) 20만 개**로 한국어에서는 무엇이 달라지는지 검증한 해설 페이지입니다.
인턴 시아·모아가 연구소 식구들(박사·조수 하루·초파리 연구원·주판봇) 앞에서 발표하고, 미공개 평가단이 점수를 매깁니다.

- 페이지: https://adminmrobo.github.io/karpathy_method_korean/
- 대상: AI를 처음 접하는 분 (코드·수식을 몰라도 읽을 수 있습니다)

## 한국어 검증 — 다섯 가지 발견

| 단계 | 한국어로 한 일 | 결과 |
|---|---|---|
| 1 micrograd | 리뷰 긍정·부정 맞히기, 처음 보는 리뷰 1,000개로 채점 | 51.8% → 64.5% |
| 2 makemore | 4~12자 한 줄 평 27,412개로 새 한 줄 평 짓기 | 후보 1,791종 → 약 27개 |
| 3 minbpe | 한국어로 토크나이저 학습, 사전 크기 바꿔 보기 | 같은 21자가 53 / 11 / 6토큰 |
| 4 nanoGPT | 리뷰 111만 자로 GPT 학습 | 후보 2,140종 → 약 31개 |
| 7 nanochat | 리뷰 20만 개로 사전 32,768개 토크나이저 학습 | 5초 · 토큰당 2.45자 |

측정: 연구실 클라우드 작업 환경(CPU 2코어·메모리 8GB, PyTorch CPU 실행), 2026-11-19. 시간은 환경마다 다릅니다.

## 폴더

| 경로 | 내용 |
|---|---|
| `index.html` | 해설 페이지 (단일 파일, 지식 색인·꾸러미 포함) |
| `data/measurements.json` | 페이지의 모든 측정값과 조건 |
| `experiments/` | 측정에 쓴 스크립트 (각 저장소 폴더 안에서 실행) |
| `kg/` | 지식 색인 원본(`kg.json`·`refs.json`·`meta.json`)과 점검 보고 |
| `cover_manifest.json` | 표지 현황판 연결 파일 |
| `image_spec.md` | 표지·장면 그림 명세서 (16비트 RPG 픽셀아트) |

## 다시 돌려 보기

```bash
git clone https://github.com/e9t/nsmc && python3 experiments/00_prepare_nsmc.py nsmc/ratings.txt
# makemore (한국어 한 줄 평)
python makemore.py -i short_reviews.txt -o out_ko --type transformer --max-steps 2001 --device cpu --seed 3407
# nanoGPT (설명서의 CPU 설정, 데이터만 한국어로)
python train.py config/train_shakespeare_char.py --dataset=nsmc_char --device=cpu --compile=False --eval_iters=20 \
  --block_size=64 --batch_size=12 --n_layer=4 --n_head=4 --n_embd=128 --max_iters=2000 --lr_decay_iters=2000 --dropout=0.0
```

## 출처와 라이선스

- 코드: [github.com/karpathy](https://github.com/karpathy) 각 저장소 (MIT)
- 한국어 데이터: 네이버 영화 리뷰 NSMC — [github.com/e9t/nsmc](https://github.com/e9t/nsmc) (CC0 1.0)
- 캐릭터 이름·설정·그림 © 안상선

글 · 안상선 ([소개](https://adminmrobo.github.io/who_am_i/who_am_i.html)) · (주)M-Robo 대표
