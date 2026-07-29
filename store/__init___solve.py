"""Persist collected items.

DATABASE_URL 이 있으면 PostgreSQL, 없으면 로컬 SQLite 파일로 폴백한다 —
설정을 코드 밖으로 빼 두면 DB가 준비되기 전에도 파이프라인을 끝까지 돌려 볼 수
있다(교안 8.2+).
"""

import os
import sqlite3

DEFAULT_SQLITE_PATH = "vibe.db"

SCHEMA_SQLITE = """
CREATE TABLE IF NOT EXISTS items (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    source       TEXT NOT NULL,
    title        TEXT NOT NULL,
    url          TEXT UNIQUE NOT NULL,
    collected_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
)
"""

SCHEMA_POSTGRES = [
    "CREATE SCHEMA IF NOT EXISTS vibe",
    """
    CREATE TABLE IF NOT EXISTS vibe.items (
        id           SERIAL PRIMARY KEY,
        source       TEXT NOT NULL,
        title        TEXT NOT NULL,
        url          TEXT UNIQUE NOT NULL,
        collected_at TIMESTAMPTZ NOT NULL DEFAULT now()
    )
    """,
]


def _is_sqlite(conn) -> bool:
    return isinstance(conn, sqlite3.Connection)


def _table(conn) -> str:
    """SQLite 는 스키마가 없어 items, PostgreSQL 은 vibe.items."""
    return "items" if _is_sqlite(conn) else "vibe.items"


def _placeholder(conn) -> str:
    """sqlite3 는 ?, psycopg 는 %s 를 쓴다."""
    return "?" if _is_sqlite(conn) else "%s"


def connect(dsn: str | None = None):
    """Open a database connection.

    *dsn* (or ``DATABASE_URL``) starting with ``postgres`` opens PostgreSQL;
    anything else is treated as a SQLite file path.
    """
    dsn = dsn or os.environ.get("DATABASE_URL") or DEFAULT_SQLITE_PATH
    if dsn.startswith("postgres"):
        import psycopg  # PostgreSQL 을 쓸 때만 필요하다

        return psycopg.connect(dsn)
    return sqlite3.connect(dsn)


def init_schema(conn) -> None:
    """Create the items table if it is not there yet."""
    cur = conn.cursor()
    if _is_sqlite(conn):
        cur.execute(SCHEMA_SQLITE)
    else:
        for statement in SCHEMA_POSTGRES:
            cur.execute(statement)
    conn.commit()


def save_items(conn, items: list[dict]) -> int:
    """Insert *items*, skipping any whose url is already stored.

    Returns the number of rows actually inserted — a re-run over the same
    items returns 0 rather than raising. ``url UNIQUE`` is the final defence
    against duplicates; this function makes hitting it a no-op.
    """
    rows = [
        (item.get("source", ""), item["title"], item["url"])
        for item in items
        if item.get("url") and item.get("title")
    ]
    if not rows:
        return 0

    ph = _placeholder(conn)
    sql = (
        f"INSERT INTO {_table(conn)} (source, title, url) "
        f"VALUES ({ph}, {ph}, {ph}) ON CONFLICT (url) DO NOTHING"
    )
    cur = conn.cursor()
    inserted = 0
    for row in rows:
        cur.execute(sql, row)
        if cur.rowcount and cur.rowcount > 0:
            inserted += cur.rowcount
    conn.commit()
    return inserted


def count_items(conn) -> int:
    """Return how many items are stored."""
    cur = conn.cursor()
    cur.execute(f"SELECT COUNT(*) FROM {_table(conn)}")
    return cur.fetchone()[0]
