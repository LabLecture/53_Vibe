from crawler import Paper


class StoreQueryError(Exception):
    pass


class StoreWriteError(Exception):
    pass


def get_unsent_papers(papers: list[Paper]) -> list[Paper]:
    """신규 수집 논문 목록을 전송 이력과 대조해 미전송 논문만 선별한다."""
    raise NotImplementedError


def save_sent_papers(papers: list[Paper]) -> int:
    """전송 완료된 논문을 전송 이력에 저장한다."""
    raise NotImplementedError
