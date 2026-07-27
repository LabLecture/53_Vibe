"""Scrape quotes from quotes.toscrape.com.

Day 3 · 1.5~1.6 [실습] 에서 채운다. 계약은 ``tests/test_quotes.py`` 가 고정한다.
1.5 에서 셀렉터를 직접 확인한 뒤, 1.6 에서 에이전트에게 구현을 맡긴다.

⚠️ 이 테스트는 실제 사이트에 요청한다 — 네트워크가 필요하다.
"""

BASE_URL = "https://quotes.toscrape.com/"


def scrape_quotes(url: str = BASE_URL) -> list[dict]:
    """Return the quotes shown on *url* as a list of text/author/tags dicts.

    TODO(1.6): 한 페이지의 명언을 긁어 온다.
      - 각 항목은 ``{"text": ..., "author": ..., "tags": [...]}``
      - 셀렉터는 1.5 에서 확인한 것을 쓴다
        (``div.quote`` 안의 ``span.text`` · ``small.author`` · ``a.tag``)
      - 예의: 자신을 밝히는 User-Agent, 타임아웃, 요청 사이 대기(1.3)
    """
    raise NotImplementedError("Day 3 · 1.6 실습: scrape_quotes 를 구현하세요")
