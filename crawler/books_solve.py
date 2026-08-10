"""Scrape books from books.toscrape.com.  (정답본 — 먼저 열지 말 것)

books.toscrape.com has no robots.txt (404), so no crawl rules are
declared; we still request a single page per call and sleep between
requests as a courtesy to the server.

원시 수집(scrape_books)과 정제(crawl)를 분리해 둔다 — 정제 규칙이 바뀌어도
수집 쪽을 다시 만지지 않아도 된다.
"""

import re
import time
from urllib.parse import urljoin

import httpx
from bs4 import BeautifulSoup

USER_AGENT = "vibe-crawler/0.1 (+study)"
BASE_URL = "https://books.toscrape.com/"
REQUEST_DELAY_SECONDS = 0.5
SOURCE = "books.toscrape.com"

# <p class="star-rating Three"> — 별점은 텍스트가 아니라 클래스 이름에 있다 (교안 1.4)
RATING_WORDS = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}


def _rating_of(pod) -> int | None:
    tag = pod.select_one("p.star-rating")
    if tag is None:
        return None
    for name in tag.get("class", []):
        if name in RATING_WORDS:
            return RATING_WORDS[name]
    return None


def scrape_books(url: str = BASE_URL) -> list[dict]:
    """Return the books shown on *url* as a list of raw dicts."""
    response = httpx.get(url, headers={"User-Agent": USER_AGENT}, timeout=10)
    response.raise_for_status()
    response.encoding = "utf-8"          # £ 가 깨지지 않게 (교안 1.3)
    time.sleep(REQUEST_DELAY_SECONDS)

    soup = BeautifulSoup(response.text, "html.parser")
    books = []
    for pod in soup.select("article.product_pod"):
        link = pod.select_one("h3 a")
        books.append(
            {
                # 본문 텍스트는 "A Light in the ..." 로 잘려 있다 — title 속성이 온전하다
                "title": link["title"],
                "price": pod.select_one("p.price_color").get_text(strip=True),
                "rating": _rating_of(pod),
                "url": urljoin(url, link["href"]),
            }
        )
    return books


def _page_url(page: int) -> str:
    return BASE_URL if page == 1 else urljoin(BASE_URL, f"catalogue/page-{page}.html")


def crawl(pages: int = 3) -> list[dict]:
    """Collect *pages* pages, clean them up, and map to the Day 2 Item shape."""
    items: list[dict] = []
    seen: set[str] = set()

    for page in range(1, pages + 1):
        for raw in scrape_books(_page_url(page)):
            if raw["url"] in seen:                 # 중복 제거: url 을 자연 키로
                continue
            seen.add(raw["url"])
            price = re.search(r"\d+(?:\.\d+)?", raw["price"])   # 정규화: '£51.77' → 51.77
            items.append(
                {
                    "source": SOURCE,
                    "url": raw["url"],
                    "title": raw["title"],
                    "price": float(price.group()) if price else None,
                    "rating": raw["rating"],
                }
            )
    return items


if __name__ == "__main__":
    import sys

    sys.stdout.reconfigure(encoding="utf-8")   # Windows 콘솔(cp949)에서 £ 출력 대비
    collected = crawl()
    print(f"정제 후 {len(collected)}건 (중복 제거됨)")
    print("샘플 Item:", collected[0])
