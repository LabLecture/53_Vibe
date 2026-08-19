import os
import datetime

_CACHE = {}         # 결과를 저장해둘 캐시 딕셔너리 (키: 아이템 개수, 값: 포맷팅된 문자열). 모듈 레벨 전역 변수
_LOG = os.path.join(os.path.dirname(__file__), "report.log")  
# 현재 파일(__file__)이 있는 폴더에 "report.log" 파일을 만들어서 로그 경로로 설정


def _w(msg):    # 로그를 파일에 기록하는 내부용(프라이빗) 함수. 앞에 _를 붙여서 "내부용"임을 표시
    with open(_LOG, "a", encoding="utf-8") as f:                                            # 로그 파일을 append(추가) 모드로 열고, UTF-8 인코딩 사용. 
        f.write("%s %s\n" % (datetime.datetime.now().isoformat(timespec="seconds"), msg))   # 현재 시간(초 단위까지) + 메시지 + 줄바꿈을 파일에 씀


def fmt(items, w=80):                   # 아이템 리스트를 보기 좋게 포맷팅하는 함수. w는 제목 최대 길이(기본값 80)
    k = len(items)                      # 아이템 개수를 세서 k에 저장 (캐시 키로 사용)
    if k in _CACHE:                     # 이미 같은 개수로 포맷팅한 결과가 캐시에 있으면
        _w("hit %s" % k)                # 캐시 히트(재사용)했다고 로그에 기록
        return _CACHE[k]                # 캐시에 저장된 문자열을 바로 반환 (계산 생략)
    out = []                            # 결과를 담을 빈 리스트 생성
    for i, it in enumerate(items, 1):  
        t = it.get("title", "").strip()  
        if len(t) > w:                  # 제목 길이가 w보다 길면
            t = t[: w - 3] + "..."      # w-3 글자까지만 자르고 뒤에 "..." 붙이기 (너무 길면 줄임)
        out.append("%2d. %s" % (i, t))  # " 1. 제목" 형태로 리스트에 추가 (%2d는 두 자리 숫자로 맞춤)
        u = it.get("url")               # 아이템에서 "url" 키를 가져옴 (없으면 None)
        if u:                           
            out.append("    %s" % u)    # 들여쓰기 4칸 후 url을 리스트에 추가
    s = "\n".join(out)                  # 리스트의 모든 줄을 줄바꿈으로 연결해서 하나의 문자열로 만듦
    _CACHE[k] = s                       # 결과를 캐시에 저장 (다음번에 같은 개수면 바로 재사용)
    _w("miss %s" % k)                   # 캐시 미스(새로 계산)했다고 로그에 기록
    return s  


def render(items, header=None):         # 최종 리포트 문자열을 만드는 함수. header는 제목(없으면 자동 생성)
    body = fmt(items)                   # 위에서 만든 fmt 함수로 본문 포맷팅
    if not body:                        # 본문이 비어있으면 "새 논문 없음" 문자열 반환
        return "새 논문 없음"  
    h = header or ("주간 리포트 (%d건)" % len(items))  # header가 주어졌으면 그걸 쓰고, 없으면 "주간 리포트 (N건)" 자동 생성
    return "%s\n%s\n%s" % (h, "-" * len(h), body)  

### 전체 동작 요약
# 1. **캐시(`_CACHE`)**  
#    아이템 **개수**가 같으면 이전에 만든 포맷 결과를 재사용합니다. (제목 내용이 달라도 개수만 같으면 캐시 히트)

# 2. **로그(`_w`)**  
#    캐시가 맞았는지(miss/hit)와 시간을 `report.log` 파일에 계속 추가 기록합니다.

# 3. **`fmt`**  
#    논문/아이템 리스트를  
#    ```
#     1. 제목...
#        https://...
#     2. 제목...
#        https://...
#    ```
#    형태로 예쁘게 만들어 줍니다. 제목이 너무 길면 `...`으로 자릅니다.

# 4. **`render`**  
#    최종적으로 헤더 + 구분선 + 본문을 합쳐서 리포트 문자열을 만듭니다.  
#    아이템이 없으면 `"새 논문 없음"`을 반환합니다.