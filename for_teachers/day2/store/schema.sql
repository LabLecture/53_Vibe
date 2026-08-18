CREATE TABLE IF NOT EXISTS paper (
    arxiv_id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    authors TEXT NOT NULL,
    url TEXT NOT NULL,
    published_at TEXT NOT NULL,
    collected_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS sent_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    arxiv_id TEXT NOT NULL REFERENCES paper (arxiv_id),
    sent_at TEXT NOT NULL
);
