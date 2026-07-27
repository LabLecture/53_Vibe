"""Fetch pages and extract items from them.

Day 3 · 1.9 [실습] 에서 채운다. 계약은 ``tests/test_crawler.py`` 가 고정한다 —
테스트를 먼저 읽고, 무엇을 돌려줘야 하는지 확인한 뒤 에이전트에게 시킨다.
"""


def fetch(url: str) -> str:
    """Return the raw body of the page at *url*.

    TODO(1.9): 실제 요청을 구현한다.
      - robots.txt 를 확인하고, 불허하면 ``PermissionError`` 를 올린다
      - 자신을 밝히는 User-Agent 를 보낸다
      - 타임아웃을 건다 (무한 대기 금지)
    """
    raise NotImplementedError("Day 3 · 1.9 실습: fetch 를 구현하세요")


def parse(html: str) -> list[dict]:
    """Extract items from a fetched page body.

    TODO(1.9): ``<li>`` 요소의 텍스트를 ``[{"title": ...}, ...]`` 로 돌려준다.
    빈 문서면 빈 리스트를 돌려준다.
    """
    raise NotImplementedError("Day 3 · 1.9 실습: parse 를 구현하세요")
