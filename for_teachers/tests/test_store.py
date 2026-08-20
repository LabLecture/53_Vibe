import pytest

from store import connect, count_items, init_schema, save_items

PAPERS = [
    {"source": "arxiv", "title": "Attention Is All You Need",
     "url": "http://arxiv.org/abs/1706.03762v7"},
    {"source": "arxiv", "title": "Denoising Diffusion Probabilistic Models",
     "url": "http://arxiv.org/abs/2006.11239v2"},
]


@pytest.fixture
def conn(tmp_path):
    """DATABASE_URL 없이 SQLite 파일로 — 네트워크도 PostgreSQL 도 필요 없다."""
    connection = connect(str(tmp_path / "vibe.db"))
    init_schema(connection)
    yield connection
    connection.close()


def test_save_items_inserts_every_row(conn):
    assert save_items(conn, PAPERS) == 2
    assert count_items(conn) == 2


def test_save_items_skips_duplicate_urls(conn):
    save_items(conn, PAPERS)

    # 같은 항목을 다시 저장해도 늘지 않는다 — url UNIQUE 가 최종 방어선이다.
    assert save_items(conn, PAPERS) == 0
    assert count_items(conn) == 2


def test_save_items_drops_rows_without_url_or_title(conn):
    dirty = PAPERS + [
        {"source": "arxiv", "title": "no url"},
        {"source": "arxiv", "title": "", "url": "http://arxiv.org/abs/0000.00000v1"},
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
    assert save_items(connection, PAPERS) == 2
    connection.close()

    assert (tmp_path / "vibe.db").exists()
