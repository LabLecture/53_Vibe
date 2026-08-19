# for_teachers — 강사용 정답본

수강생이 실습으로 **직접 만들 산출물**의 완성본이다. 실습 폴더(`day2/`·`day3/`)와 분리해 둔 이유는
하나다 — 옆에 답이 놓여 있으면 실습이 성립하지 않는다.

- `day2/` — Day 2 · 3교시(5대 설계문서 + 스캐폴딩) 산출물
  - `docs/` PRD · 유스케이스 · 컴포넌트설계서 · 인터페이스정의서 · 시퀀스 · ERD
  - `crawler/` `store/` `notifier/` `main.py` — 문서에서 나온 스캐폴딩(스텁만, 구현 없음)

이 산출물은 교안의 📊 실측값과 같은 세션에서 나온 것이다(Sonnet, `docs/` 가 빈 상태에서 순서대로 실행).
수강생 화면은 다를 수 있다 — **정답이 아니라 한 번 돌려 본 결과**로 다룬다.

- `day2/legacy_solve/` — Day 2 · 4교시(Explore→Plan→Code→Commit) 정답본
  - `report_init.py` **실습 시작 상태**(= `legacy/report.py` 원본). 캐시 키가 `len(items)` 뿐이라
    항목 수만 같으면 지난 결과를 그대로 돌려주는 버그가 살아 있다
  - `EXPLORE.md` Explore 단계 산출물(흐름·위험지점·영향 범위)
  - `test_report_characterization.py` 특성화 테스트 15개 (원본 코드에서 전부 GREEN)
  - `report_fixed.py` 최소 범위 수정본. `report_init.py` 와 **3줄만** 다르다 —
    `diff report_init.py report_fixed.py` 로 4교시의 결론(−3/+3)을 그대로 보여줄 수 있다

### 실습을 처음부터 다시 하려면
```powershell
cd 53_Vibe
git checkout legacy/            # 커밋된 원본으로 되돌린다 (가장 간단)
git clean -fd docs tests        # Explore 산출물·특성화 테스트도 지운다(만들었다면)
```
`git` 을 쓰기 어려운 상황이면 `for_teachers/day2/legacy_solve/report_init.py` 를
`legacy/report.py` 로 덮어써도 된다.
