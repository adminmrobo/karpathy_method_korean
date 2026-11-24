# 이미지 명세서 — 카파시의 방법론 (한국어 검증 · 인턴 발표회)

그림체: **16비트 RPG 픽셀아트**(SNES 시대 풍), 낮의 연구실, 흰 바탕 계열. 글자·로고 없음.

## 그림 목록

| 키 | 판 | 상태 | 쓰는 곳 | 만드는 순서 |
|---|---|---|---|---|
| `cover` | 표지 16:9 | 새로 그림 | 페이지 맨 위, 공유 미리보기(og), 목차 썸네일(표지에서 자름) | 1 |
| 캐릭터 표정 그림 | 96px | 캐릭터 팩 재사용 | 말풍선·등장인물 | — |
| 동작 스트립 S1·M16·D1·A1·F1·R1 | 128px | 동작 팩 재사용 | 머리 부분 발표회 무대 캔버스 | — |

## 1. 표지 지시문 (Genspark 등)

```
detailed 16-bit SNES-era pixel art, higher pixel density, about 640x360 native pixel grid, each pixel crisp, no blur, no anti-aliasing.
Wide 16:9 illustration of a bright daytime research-lab seminar room with white walls and soft sunlight.
On a small stage, a large blank presentation screen (no text on it) shows simple pixel icons in a row: a tiny gear, a name tag, two joined letter tiles, a stack of blocks, an empty notebook with a pencil, a computer chip, a chat bubble.
Left of the screen: intern Sia presenting with an open palm — waist-length straight jet-black hair with side-swept bangs, no hair accessory, grey eyes, small silver drop earrings, long-sleeved charcoal-black maid dress with a big grey ribbon and an ankle-length white frilled apron.
Right of the screen: intern Moa in her business suit holding a pointer — ash-beige long hair tied in a low ponytail with a pink scrunchie, amber eyes, black jacket, white shirt.
Audience seated in the foreground, seen from behind and side: the Doctor (thin teal square glasses, black hair with one white streak, short tied tail, white lab coat), Haru (pink long hair with two buns and a navy streak, lab coat over a lavender hoodie), the fruit-fly researcher (black body, red compound eyes, blue helmet with a gold line), Jupanbot (beige box CRT body, dark green screen with a mint pixel face, abacus-bead antenna, tank treads).
At the far back corner, three small dark-navy silhouettes with white dot eyes sit quietly as judges, faces not revealed.
Keep the right third of the image calm for title text. No text, no letters, no logos, no watermark.
```

참고 그림으로 함께 올릴 것: 캐릭터 기본 그림 4장(박사·조수·초파리·주판봇), 시아 E13, 모아 정장 M16 한 장, X1~X3 E13 (`fruitfly-lab-expressions/images`).

## 2. 받은 뒤 반영 (기본 스킬 18-15-2)

1. 원래 픽셀 격자를 찾아(보통 받은 PNG ÷ 4) `NEAREST` 정수배로만 키운 무손실 WebP(예 480×270 → 1920×1080), 300KB 이하.
2. `img/cover.webp`, 공유 미리보기 `img/og.webp`, 썸네일 `img/thumb.webp`는 원래 그림에서 잘라 정수배로.
3. `cover_manifest.json`의 `items`에 `cover`·`og`·`thumb`를 더하고 `status`를 `received` → 반영 후 `ok`.
4. 페이지 `<head>`에 og:image를 넣는다. 그림에 `image-rendering`을 직접 걸지 않는다(px-fix v1이 맡음).
