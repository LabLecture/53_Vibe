import pytest

from store import connect, count_items, init_schema, save_items

BOOKS = [
    {"source": "books.toscrape", "title": "A Light in the Attic",
     "url": "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"},
    {"source": "books.toscrape", "title": "Tipping the Velvet",
     "url": "https://books.toscrape.com/catalogue/tipping-the-velvet_999/index.html"},
]


@pytest.fixture
def conn(tmp_path):
    """DATABASE_URL 없이 SQLite 파일로 — 네트워크도 PostgreSQL 도 필요 없다."""
    connection = connect(str(tmp_path / "vibe.db"))
    init_schema(connection)
    yield connection
    connection.close()


def test_save_items_inserts_every_row(conn):
    assert save_items(conn, BOOKS) == 2
    assert count_items(conn) == 2


def test_save_items_skips_duplicate_urls(conn):
    save_items(conn, BOOKS)

    # 같은 항목을 다시 저장해도 늘지 않는다 — url UNIQUE 가 최종 방어선이다.
    assert save_items(conn, BOOKS) == 0
    assert count_items(conn) == 2


def test_save_items_drops_rows_without_url_or_title(conn):
    dirty = BOOKS + [
        {"source": "books.toscrape", "title": "no url"},
        {"source": "books.toscrape", "title": "", "url": "https://example.com/empty"},
    ]
    assert save_items(conn, dirty) == 2


def test_save_items_empty_list(conn):
    assert save_items(conn, []) == 0


def test_connect_falls_back_to_sqlite(tmp_path, monkeypatch):
    """DATABASE_URL 이 없으면 로컬 SQLite 파일로 폴백한다."""
    monkeypatch.delenv("DATABASE_URL", raising=False)
    monkeypatch.chdir(tmp_path)

    connection = connect()
    init_schema(connection)
    assert save_items(connection, BOOKS) == 2
    connection.close()

    assert (tmp_path / "vibe.db").exists()
