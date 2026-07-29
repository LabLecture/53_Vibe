"""Persist collected items.

Day 3 · 8.2+ [실습] 에서 채운다. 계약은 ``tests/test_store.py`` 가 고정한다.
테스트는 **SQLite 임시 파일**로만 돌아가므로 PostgreSQL 도 네트워크도 필요 없다.
"""


def connect(dsn: str | None = None):
    """Open a database connection.

    TODO(8.2+): *dsn* → 없으면 환경변수 ``DATABASE_URL`` → 그것도 없으면
    로컬 SQLite 파일(``vibe.db``) 순으로 정한다.
      - ``postgres`` 로 시작하면 PostgreSQL (psycopg 는 그때만 import)
      - 그 외에는 SQLite 파일 경로로 취급
    설정을 코드 밖에 두면 DB가 준비되기 전에도 파이프라인을 돌려 볼 수 있다.
    """
    raise NotImplementedError("Day 3 · 8.2+ 실습: connect 를 구현하세요")


def init_schema(conn) -> None:
    """Create the items table if it is not there yet.

    TODO(8.2+): Day 2 ERD 그대로 — ``source`` / ``title`` / ``url UNIQUE`` /
    ``collected_at``(기본 now()). PostgreSQL 이면 ``vibe`` 스키마 안에,
    SQLite 면 스키마 없이 ``items`` 로 만든다.
    """
    raise NotImplementedError("Day 3 · 8.2+ 실습: init_schema 를 구현하세요")


def save_items(conn, items: list[dict]) -> int:
    """Insert *items*, skipping any whose url is already stored.

    TODO(8.2+): 실제로 들어간 행 수를 돌려준다.
      - 같은 항목을 다시 저장하면 **예외가 아니라 0** 이어야 한다
        (``INSERT ... ON CONFLICT (url) DO NOTHING``) — 매일 도는 파이프라인이
        중복으로 죽으면 안 된다
      - ``url`` 이나 ``title`` 이 비어 있는 항목은 저장하지 않는다
      - sqlite3 는 ``?``, psycopg 는 ``%s`` 로 파라미터 자리표시자가 다르다
    """
    raise NotImplementedError("Day 3 · 8.2+ 실습: save_items 를 구현하세요")


def count_items(conn) -> int:
    """Return how many items are stored.

    TODO(8.2+): 저장된 행 수를 센다 — 재실행 후에도 늘지 않는지 확인하는 데 쓴다.
    """
    raise NotImplementedError("Day 3 · 8.2+ 실습: count_items 를 구현하세요")
