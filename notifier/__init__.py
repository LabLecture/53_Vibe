"""Deliver messages about crawled items.

Day 3 · 6.11 [실습] 에서 채운다. 계약은 ``tests/test_notifier.py`` 가 고정한다.
테스트는 로컬에 가짜 웹훅 서버를 띄워 검증하므로, 실제 Discord 채널로는
아무것도 나가지 않는다.
"""


def format_message(items: list[dict]) -> str:
    """Render *items* into a single notification body.

    TODO(6.11): 각 item 의 ``title`` 을 한 줄씩 묶어 하나의 본문으로 만든다.
    보낼 게 없으면(빈 리스트) 빈 문자열을 돌려줘 호출 측이 전송을 건너뛸 수
    있게 한다.
    """
    raise NotImplementedError("Day 3 · 6.11 실습: format_message 를 구현하세요")


def send(message: str) -> bool:
    """Deliver *message*. Returns True when accepted by the transport.

    TODO(6.11): Discord 웹훅으로 ``{"content": message}`` 를 POST 한다.
      - URL 은 환경변수 ``DISCORD_WEBHOOK_URL`` 에서 ``os.environ`` 으로 읽는다
        (하드코딩 금지). **이 함수 안에서 .env 를 읽지 말 것** — 테스트가
        환경변수를 지웠다 넣었다 하므로 그러면 계약이 깨진다.
      - URL 이 없으면 예외 대신 경고를 찍고 ``False``
      - 웹훅이 4xx/5xx 로 답해도 예외 대신 ``False``
        (알림 실패가 파이프라인 전체를 죽이면 안 된다)
    """
    raise NotImplementedError("Day 3 · 6.11 실습: send 를 구현하세요")
