"""Scrape quotes from quotes.toscrape.com.

quotes.toscrape.com has no robots.txt (404), so no crawl rules are
declared; we still request a single page per call and sleep between
requests as a courtesy to the server.

원시 수집(scrape_quotes)과 정제(crawl)를 분리해 둔다 — 정제 규칙이 바뀌어도
수집 쪽을 다시 만지지 않아도 된다.
"""

import time

import httpx
from bs4 import BeautifulSoup

USER_AGENT = "vibe-crawler/0.1 (+study)"
BASE_URL = "https://quotes.toscrape.com/"
REQUEST_DELAY_SECONDS = 0.5
SOURCE = "quotes.toscrape"


def scrape_quotes(url: str = BASE_URL) -> list[dict]:
    """Return the quotes shown on *url* as a list of text/author/tags dicts."""
    response = httpx.get(url, headers={"User-Agent": USER_AGENT}, timeout=10)
    response.raise_for_status()
    time.sleep(REQUEST_DELAY_SECONDS)

    soup = BeautifulSoup(response.text, "html.parser")
    quotes = []
    for quote in soup.select("div.quote"):
        quotes.append(
            {
                "text": quote.select_one("span.text").get_text(strip=True),
                "author": quote.select_one("small.author").get_text(strip=True),
                "tags": [tag.get_text(strip=True) for tag in quote.select("a.tag")],
            }
        )
    return quotes


def crawl(pages: int = 3) -> list[dict]:
    """Collect *pages* pages, clean them up, and map to the Day 2 Item shape."""
    items: list[dict] = []
    seen: set[str] = set()

    for page in range(1, pages + 1):
        url = BASE_URL if page == 1 else f"{BASE_URL}page/{page}/"
        for raw in scrape_quotes(url):
            content = raw["text"].strip("“”\"")   # 정규화: 앞뒤 따옴표를 벗긴다
            if content in seen:                    # 중복 제거: text 를 자연 키로
                continue
            seen.add(content)
            items.append(
                {
                    "source": SOURCE,
                    "url": url,
                    "title": raw["author"],
                    "content": content,
                    "tags": raw["tags"],
                }
            )
    return items


if __name__ == "__main__":
    collected = crawl()
    print(f"정제 후 {len(collected)}건 (중복 제거됨)")
    print("샘플 Item:", collected[0])
