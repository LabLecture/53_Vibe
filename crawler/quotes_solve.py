"""Scrape quotes from quotes.toscrape.com.

quotes.toscrape.com has no robots.txt (404), so no crawl rules are
declared; we still request a single page per call and sleep between
requests as a courtesy to the server.
"""

import time

import httpx
from bs4 import BeautifulSoup

USER_AGENT = "vibe-crawler/0.1 (+study)"
BASE_URL = "https://quotes.toscrape.com/"
REQUEST_DELAY_SECONDS = 0.5


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
