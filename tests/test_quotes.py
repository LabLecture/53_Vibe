from crawler.quotes import scrape_quotes


def test_scrape_quotes_returns_first_page_items():
    quotes = scrape_quotes()

    assert len(quotes) == 10
    for quote in quotes:
        assert set(quote) == {"text", "author", "tags"}
        assert quote["text"] != ""
        assert quote["author"] != ""
        assert isinstance(quote["tags"], list)
