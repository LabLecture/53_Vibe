import http.server
import threading

import pytest

from crawler import fetch, parse


class _DisallowAllHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        if self.path == "/robots.txt":
            body = b"User-agent: *\nDisallow: /\n"
        else:
            body = b"<html><body>blocked</body></html>"
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args) -> None:
        pass


@pytest.fixture
def disallow_all_server():
    server = http.server.HTTPServer(("127.0.0.1", 0), _DisallowAllHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    yield f"http://127.0.0.1:{server.server_port}/"
    server.shutdown()
    thread.join()


def test_fetch_returns_page_body():
    assert fetch("https://example.com") != ""


def test_fetch_respects_robots_disallow(disallow_all_server):
    with pytest.raises(PermissionError):
        fetch(disallow_all_server)


def test_parse_extracts_items():
    items = parse("<ul><li>first</li><li>second</li></ul>")
    assert len(items) == 2


def test_parse_empty_page_yields_no_items():
    assert parse("") == []
