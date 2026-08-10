"""Scrape books from books.toscrape.com.

Day 3 · 1.6 [실습] 에서 채운다 — 1.3~1.5 의 자유 실습 파일(``scrape_books.py``)을
여기로 옮겨 정착시키는 자리다.

계약(``tests/test_books.py``)은 **미리 주지 않는다** — 1.6 ①에서 에이전트에게
먼저 만들게 하고(RED), 그 다음 통과시킨다(GREEN). Day 2 5교시의 리듬 그대로다.

두 층으로 나눠 둔 이유: **원시 수집(scrape_books)과 정제(crawl)를 분리**해 두면
정제 규칙이 바뀌어도 수집을 다시 안 만져도 된다.

⚠️ 실제 사이트에 요청한다 — 네트워크가 필요하다.
"""

BASE_URL = "https://books.toscrape.com/"


def scrape_books(url: str = BASE_URL) -> list[dict]:
    """Return the books shown on *url* as a list of raw dicts.

    TODO(1.6): 한 페이지의 책을 **원시값 그대로** 긁어 온다.
      - 각 항목은 ``{"title": ..., "price": ..., "rating": ..., "url": ...}``
      - 구조는 1.4 에서 F12 로 확인한 것을 쓴다 (``article.product_pod`` 안의
        ``h3 a`` 의 **title 속성**(본문 텍스트는 ``...`` 로 잘려 있다) ·
        ``p.price_color`` · ``p.star-rating`` 의 **클래스 이름**(One~Five))
      - 상세 URL 은 ``href`` 가 상대 경로이므로 절대 URL 로 만든다
      - 예의: 자신을 밝히는 User-Agent, 타임아웃, 요청 사이 대기(1.2)
      - **정제·매핑은 여기서 하지 않는다** — 그건 crawl 의 몫이다
    """
    raise NotImplementedError("Day 3 · 1.6 실습: scrape_books 를 구현하세요")


def crawl(pages: int = 3) -> list[dict]:
    """Collect *pages* pages, clean them up, and map to the Day 2 Item shape.

    TODO(1.6): scrape_books 를 페이지마다 호출한 뒤 —
      - **정규화**: 가격에서 ``£`` 를 벗겨 float 로
      - **중복 제거**: url 을 자연 키로 (DB ``url UNIQUE`` 전 1차 방어)
      - **Item 매핑**: ``{source, url, title, price, rating}``
      - 요청 사이 0.5초 대기(예의)

    2페이지부터는 ``catalogue/page-2.html`` … ``page-50.html`` 이다
    (``page-51.html`` 은 404 — 총 1,000권).
    """
    raise NotImplementedError("Day 3 · 1.6 실습: crawl 을 구현하세요")
