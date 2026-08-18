from crawler import Paper


def send_papers(papers: list[Paper]) -> bool:
    """전송 대상 논문 목록을 Discord 채널로 발송한다. 빈 리스트면 발송을 생략한다."""
    raise NotImplementedError
