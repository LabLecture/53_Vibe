"""Scrape quotes from quotes.toscrape.com.

Day 3 · 1.6 [실습] 에서 채운다 — 1.4의 자유 실습 파일(``scrape_quotes.py``)을
여기로 옮겨 정착시키는 자리다.

계약(``tests/test_quotes.py``)은 **미리 주지 않는다** — 1.6 ①에서 에이전트에게
먼저 만들게 하고(RED), 그 다음 통과시킨다(GREEN). Day 2 5교시의 리듬 그대로다.

두 층으로 나눠 둔 이유: **원시 수집(scrape_quotes)과 정제(crawl)를 분리**해 두면
정제 규칙이 바뀌어도 수집을 다시 안 만져도 된다.

⚠️ 실제 사이트에 요청한다 — 네트워크가 필요하다.
"""

BASE_URL = "https://quotes.toscrape.com/"


def scrape_quotes(url: str = BASE_URL) -> list[dict]:
    """Return the quotes shown on *url* as a list of text/author/tags dicts.

    TODO(1.6): 한 페이지의 명언을 **원시값 그대로** 긁어 온다.
      - 각 항목은 ``{"text": ..., "author": ..., "tags": [...]}``
      - 셀렉터는 1.5 에서 확인한 것을 쓴다
        (``div.quote`` 안의 ``span.text`` · ``small.author`` · ``a.tag``)
      - 예의: 자신을 밝히는 User-Agent, 타임아웃, 요청 사이 대기(1.3)
      - **정제·매핑은 여기서 하지 않는다** — 그건 crawl 의 몫이다
    """
    raise NotImplementedError("Day 3 · 1.6 실습: scrape_quotes 를 구현하세요")


def crawl(pages: int = 3) -> list[dict]:
    """Collect *pages* pages, clean them up, and map to the Day 2 Item shape.

    TODO(1.6): scrape_quotes 를 페이지마다 호출한 뒤 —
      - **정규화**: 명언 앞뒤 따옴표(“ ”)를 벗긴다
      - **중복 제거**: text 를 자연 키로 (DB ``url UNIQUE`` 전 1차 방어)
      - **Item 매핑**: ``{source, url, title(=author), content(=text), tags}``
      - 요청 사이 0.5초 대기(예의)
    """
    raise NotImplementedError("Day 3 · 1.6 실습: crawl 을 구현하세요")
