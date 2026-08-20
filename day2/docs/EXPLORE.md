# legacy/ 탐색 기록

## 진입점부터 흐름

`run_weekly.py` 가 진입점.

```
run_weekly.py
  → legacy/weekly.py : build_weekly_message(papers)
      → legacy/report.py : render(items, header=None)
          → fmt(items, w=80)   # 캐시 조회/적재 + 로그 파일 쓰기
```

- `render()` : `fmt()` 로 본문 만들고, 비어있으면 "새 논문 없음", 아니면 헤더 + 구분선(`-`×len(h)) + 본문.
- `fmt()` : 논문 개수 `k = len(items)` 를 키로 `_CACHE` 조회 → 있으면 그대로 반환("hit" 로그), 없으면 번호 매기고 제목을 `w`(기본 80자)로 자르고 URL 붙여서 조립 후 `_CACHE[k]` 에 저장("miss" 로그).
- 로그는 매 호출마다 `report.log` 에 append (`_w()`).

## 위험지점 표 — 전역 상태 / 파일 IO / 부작용

| 함수 | 종류 | 내용 | 위험 |
|---|---|---|---|
| `_CACHE`(모듈 전역 dict) | 전역 상태 | `fmt()` 이 읽고 쓴다 | **키가 `len(items)` 뿐이라 내용이 다른데 개수만 같은 리스트가 오면 잘못된 캐시를 반환**(캐시 오염). 프로세스가 살아있는 한 절대 안 비워짐(무한 성장 겸 stale 결과). |
| `_w()` | 파일 IO + 부작용 | 호출마다 `report.log` 에 append-open | 매 `fmt()` 호출마다 디스크 I/O. 로그 파일 삭제/권한 없으면 예외로 `fmt()` 자체가 죽음. 동시 실행(멀티프로세스) 시 인터리브 가능성(락 없음). |
| `fmt()` | 전역 상태 읽기/쓰기 + `_w()` 호출 | 캐시 히트/미스 로그 남김 | 순수 함수처럼 보이지만 아님 — 같은 입력이라도 첫 호출과 이후 호출의 부작용(로그, 캐시 채움)이 다름. 테스트에서 `_CACHE` 초기화 안 하면 테스트 간 오염. |
| `render()` | 없음(자체) | `fmt()` 을 통해 간접적으로 전역 상태/IO에 연루 | 직접 부작용은 없지만 `fmt()` 의 부작용을 그대로 상속. |
| `_LOG` 경로 | 모듈 로드시 고정 | `os.path.dirname(__file__)` 기준 | 모듈 위치가 바뀌면(패키징 등) 로그 경로도 따라 바뀜 — 배포 환경에 따라 쓰기 권한 문제. |

## 영향 범위 표 — `fmt()` 을 바꾸면 영향받는 곳

| 위치 | 관계 | 비고 |
|---|---|---|
| `legacy/report.py: render()` | 직접 호출부 | `fmt(items)` — `w` 기본값(80) 그대로 사용, 커스텀 폭 넘기는 곳 없음 |
| `legacy/weekly.py: build_weekly_message()` | 간접(render 경유) | `render(papers)` |
| `legacy/weekly.py: build_digest()` | 간접(render 경유) | `render(papers, header=title)` |
| `run_weekly.py` | 최종 소비자 | `build_weekly_message(week1)`, `build_weekly_message(week2)` 출력을 그대로 print |
| 테스트 | **없음** | `tests/` 디렉터리에 report/weekly/fmt 관련 테스트 파일이 현재 존재하지 않음(`test_report_characterization.py` 는 다른 repo(`2608_vibe_coding/for_teachers`)에 있던 것으로, 이 저장소엔 없음) |
| 설정 | **없음** | `w`(폭), 캐시, 로그 경로를 외부에서 주입하는 설정 파일 없음 — 전부 하드코딩 |

### 시사점
- `fmt()` 을 고치기 전에 **캐릭터라이제이션 테스트가 먼저 있어야** 한다 — 지금은 회귀를 잡아줄 테스트가 0개.
- 특히 `_CACHE` 키를 `len(items)` 대신 내용 기반으로 바꾸는 리팩터링을 할 경우, "미스/히트" 로그 문자열에 의존하는 코드가 없는지도 같이 확인 필요(현재는 없음, `_w` 출력을 아무도 파싱하지 않음).
