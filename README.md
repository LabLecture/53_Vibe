# 53_Vibe — Vibe Coding 실습 저장소

Vibe Coding 3일 과정의 실습 저장소. **보조 노트북**(원리를 직접 겪는 용도)과
**관통 프로젝트 스캐폴딩**(교안 [실습]에서 채우는 뼈대)이 함께 들어 있다.

## 구성

```
53_Vibe/
├── day2/                    # Day 2 보조 노트북
├── day3/                    # Day 3 보조 노트북
│   ├── 01_crawler.ipynb         # 1교시 — 요청→파싱→정제→Item
│   ├── 02_injection_demo.ipynb  # 2교시 — 인젝션 재현→방어
│   ├── 03_ml_pipeline.ipynb     # 3교시 — 전처리→학습→평가
│   └── 05_agent_sdk.ipynb       # 5교시 — Agent SDK 최소 예제
│
├── crawler/                 # 관통 프로젝트 ① 수집  ← 1.9 에서 채운다
├── store/                   # 관통 프로젝트 ② 저장  ← 8.2+ 에서 채운다
├── notifier/                # 관통 프로젝트 ④ 알림  ← 6.11 에서 채운다
├── tests/                   # 계약(contract) — 이 테스트가 정답을 고정한다
├── conftest.py              # tests/ 에서 프로젝트 루트를 import 가능하게
└── .env.example             # .env 로 복사해 쓴다
```

## 시작하기

```powershell
pip install pytest httpx beautifulsoup4 python-dotenv
```
```powershell
python -m pytest -q
```

**처음에는 빨간불이 정상이다.** `crawler/`·`notifier/` 는 아직 **스텁**이라
`NotImplementedError` 를 낸다 — 그걸 채우는 게 실습이다.

## 실습 방식 — 테스트가 정답을 고정한다

`tests/` 는 **미리 주어지는 계약**이다. 손대지 말고, **먼저 읽는다.**
무엇을 돌려줘야 하는지 테스트가 이미 말하고 있으니, 그걸 근거로 에이전트에게
지시하고 결과를 검증한다.

| 실습 | 채울 곳 | 계약 |
|---|---|---|
| Day 3 · 1.6 | `crawler/quotes.py` | `tests/test_quotes.py` |
| ↳ | 1.4에서 자유 실습으로 만든 `scrape_quotes.py` 를 여기로 옮겨 정착시키고, 정제·매핑을 하는 `crawl` 을 얹는다 | |
| Day 3 · 1.9 | `crawler/__init__.py` | `tests/test_crawler.py` |
| Day 3 · 6.11 | `notifier/__init__.py` | `tests/test_notifier.py` |
| Day 3 · 8.2+ | `store/__init__.py` | `tests/test_store.py` |

한 파일씩 검증하려면:
```powershell
python -m pytest tests/test_notifier.py -q
```

## `_solve` 파일 — 먼저 보지 말 것

`*_solve.py` / `*_solve.ts` 는 **정답본**이다. 막혔을 때 참고하거나, 내가 만든
것과 대조해 보는 용도다. 먼저 열어 보면 실습의 의미가 없다.

| 정답본 | 대응 실습 |
|---|---|
| `crawler/__init___solve.py` | 1.9 |
| `crawler/quotes_solve.py` | 1.6 |
| `notifier/__init___solve.py` | 6.11 |
| `store/__init___solve.py` | 8.2+ |
| `notify_solve.ts` | 6.5 (bun 웹훅 알림) |

## 시크릿

`.env.example` 을 `.env` 로 복사해 본인 값을 채운다. **`.env` 는 커밋되지
않는다**(`.gitignore`). 토큰·웹훅 URL 을 코드나 문서에 붙여넣지 않는다 —
한 번이라도 적었다면 발급처에서 **재발급**한다.

> ⚠️ **Python 은 `.env` 를 자동으로 읽지 않는다.** bun 은 알아서 읽어 주지만
> Python 은 진입점에서 `load_dotenv()` 를 한 번 불러 줘야 `os.environ` 에
> 올라온다(교안 6.11).

## 네트워크가 필요한 테스트

`tests/test_quotes.py` 와 `test_crawler.py::test_fetch_returns_page_body` 는
**실제 사이트에 요청한다**. 오프라인이면 이 둘은 실패한다 — 나머지는 로컬에
가짜 서버를 띄워 검증하므로 네트워크 없이도 돈다.

`tests/test_notifier.py` 도 **로컬 가짜 웹훅 서버**를 쓴다. 테스트를 돌려도
실제 Discord 채널로는 아무것도 나가지 않는다.
