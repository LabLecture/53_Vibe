# legacy/ 코드 탐색 노트

## 핵심 흐름 (진입점부터)

1. **`run_weekly.py`** (진입점) — `legacy.weekly.build_weekly_message(papers)` 를 호출해 두 주차 리포트를 출력한다.
2. **`legacy/weekly.py`**
   - `build_weekly_message(papers)` → `render(papers)` 호출 (헤더 없음, 기본 헤더 사용)
   - `build_digest(papers, title)` → `render(papers, header=title)` 호출 (커스텀 헤더)
   - 둘 다 `legacy.report.render` 의 얇은 래퍼.
3. **`legacy/report.py`**
   - `render(items, header=None)`: `fmt(items)` 로 본문을 만들고, 비어 있으면 `"새 논문 없음"`, 아니면 헤더 + 구분선(`-` 반복) + 본문을 합쳐 반환.
   - `fmt(items, w=80)`: 논문 리스트를 번호 매긴 텍스트로 변환하는 핵심 포맷터.
     - 항목 개수 `k = len(items)` 를 캐시 키로 `_CACHE` 조회. 히트 시 `_w("hit ...")` 로그 남기고 캐시값 즉시 반환.
     - 미스 시 각 항목의 `title` 을 `w`(기본 80)자로 자르고(`...` 붙임), `url` 있으면 다음 줄에 들여써서 추가.
     - 결과 문자열을 `_CACHE[k]` 에 저장, `_w("miss ...")` 로그 후 반환.
   - `_w(msg)`: `report.log` 파일에 타임스탬프와 함께 append. `fmt` 호출마다 (히트든 미스든) 매번 실행되는 부작용.
   - `_LOG`: 모듈 임포트 시 `os.path.dirname(__file__)` 기준으로 계산되는 로그 파일 경로.

즉 실행 흐름은 `run_weekly.py → build_weekly_message → render → fmt (+ _w 로깅, _CACHE 조회/저장) → render 가 문자열 합쳐서 출력`.

## 위험 지점 (전역 상태 / 파일 IO / 부작용)

| 위치 | 종류 | 내용 | 위험 |
|---|---|---|---|
| `report.py:4` `_CACHE = {}` | 전역 상태 | 모듈 레벨 dict, 프로세스 생존 기간 내내 유지 | 캐시 키가 `len(items)` 뿐이라 **항목 개수만 같고 내용이 다른 리스트**가 들어오면 잘못된(이전 요청의) 결과를 그대로 반환하는 버그 위험. 테스트 간 상태 격리 안 됨 |
| `report.py:5` `_LOG` | 전역 상태 + 파일 경로 의존 | import 시 1회 계산되는 로그 파일 절대경로 | 모듈을 다른 작업 디렉터리/권한 환경에서 import 시 쓰기 실패 가능성 |
| `report.py:8-10` `_w()` | 파일 IO (부작용) | 매 `fmt` 호출마다 `report.log` 에 append (`open(..., "a")`) | 예외 처리 없음 — 디스크 꽉 참/권한 없음 시 그대로 예외 전파되어 `fmt`/`render` 전체가 실패. 동시 실행(멀티프로세스) 시 로그 인터리빙 가능 |
| `report.py:13-30` `fmt()` | 부작용 + 전역 상태 read/write | `_CACHE` 조회·저장, `_w` 호출 | 순수 함수가 아님 — 같은 입력이라도 캐시 상태에 따라 내부 동작(로그 기록 여부, 실제 계산 여부)이 달라짐 |
| `report.py:33-38` `render()` | 간접 부작용 | 내부에서 `fmt` 호출 | `fmt` 의 캐시/로깅 부작용을 그대로 물려받음 |

## 영향 범위: `fmt()` 를 바꾸면 영향받는 곳

| 구분 | 위치 | 설명 |
|---|---|---|
| 직접 호출부 | `report.py:34` (`render` 내부) | `fmt(items)` 호출 — `w` 기본값(80)에 의존 |
| 간접 호출부 1 | `weekly.py:5` `build_weekly_message` | `render` 경유로 `fmt` 결과에 의존 |
| 간접 호출부 2 | `weekly.py:9` `build_digest` | 동일 |
| 진입점 | `run_weekly.py:1,12,14` | `build_weekly_message` 를 통해 최종 출력 텍스트가 `fmt` 포맷에 그대로 노출됨 (콘솔 출력) |
| 캐시/부작용 | `report.py:4` `_CACHE`, `report.py:8-10` `_w`/`report.log` | `fmt` 의 캐싱 키 전략이나 로깅 형식을 바꾸면 캐시 히트 판정, 로그 포맷(`"hit %s"`/`"miss %s"`) 모두 같이 바뀜 |
| 출력 포맷 계약 | `render()` 의 `"새 논문 없음"` 분기 | `render` 는 `fmt(items)` 가 빈 문자열인지 여부로 분기함 — `fmt` 의 빈 입력 처리(반환값) 를 바꾸면 이 분기 로직이 깨질 수 있음 |
| 테스트 | 없음 | 저장소 내 테스트 파일/디렉터리(`test_*`, `tests/`) 존재하지 않음 — 회귀 검증 수단 없음 |
| 설정 | 없음 | `pyproject.toml`, `setup.cfg`, `.ini`/`.yaml` 등 `fmt` 관련 설정 파일 없음. `report.log` 는 런타임 생성 파일이며 설정 파일이 아님 |

## 비고

- `legacy/__init__.py` 는 빈 파일.
- 테스트·설정 부재 상태이므로, `fmt()` 변경 시 회귀 확인은 `run_weekly.py` 를 직접 실행해 출력 비교하는 수동 검증에 의존해야 함.
