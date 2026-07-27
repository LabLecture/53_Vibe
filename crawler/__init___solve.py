"""Fetch pages and extract items from them."""

import urllib.request
import urllib.robotparser
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse

USER_AGENT = "vibe-crawler/0.1"
TIMEOUT = 10


def _can_fetch(url: str) -> bool:
    """Check *url* against its site's robots.txt for USER_AGENT."""
    parsed = urlparse(url)
    robots_url = urljoin(f"{parsed.scheme}://{parsed.netloc}", "/robots.txt")
    parser = urllib.robotparser.RobotFileParser()
    parser.set_url(robots_url)
    try:
        parser.read()
    except OSError:
        return True  # robots.txt unreachable: assume allowed
    return parser.can_fetch(USER_AGENT, url)


def fetch(url: str) -> str:
    """Return the raw body of the page at *url*.

    Honors robots.txt (raises PermissionError if disallowed), sends an
    identifying User-Agent, and bounds the request with TIMEOUT.
    """
    if not _can_fetch(url):
        raise PermissionError(f"robots.txt disallows fetching {url}")
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
        charset = response.headers.get_content_charset() or "utf-8"
        return response.read().decode(charset, errors="replace")


class _ItemParser(HTMLParser):
    """Collect the text of every <li> element, including nested markup."""

    def __init__(self) -> None:
        super().__init__()
        self.items: list[dict] = []
        self._depth = 0
        self._parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list) -> None:
        if tag == "li":
            self._depth += 1

    def handle_endtag(self, tag: str) -> None:
        if tag != "li" or self._depth == 0:
            return
        self._depth -= 1
        if self._depth == 0:
            self.items.append({"title": "".join(self._parts).strip()})
            self._parts = []

    def handle_data(self, data: str) -> None:
        if self._depth:
            self._parts.append(data)


def parse(html: str) -> list[dict]:
    """Extract items from a fetched page body."""
    parser = _ItemParser()
    parser.feed(html)
    parser.close()
    return parser.items
