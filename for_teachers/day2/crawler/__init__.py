from dataclasses import dataclass
from datetime import datetime


@dataclass
class Paper:
    arxiv_id: str
    title: str
    authors: list[str]
    url: str
    published_at: datetime


class CrawlerFetchError(Exception):
    pass


def fetch_recent_papers(category: str = "cs.AI", days: int = 7) -> list[Paper]:
    """arXiv 지정 카테고리에서 최근 N일 이내 신규 논문을 조회한다."""
    raise NotImplementedError
