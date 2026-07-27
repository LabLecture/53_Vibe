import http.server
import json
import threading

import pytest

from notifier import format_message, send


class _CaptureHandler(http.server.BaseHTTPRequestHandler):
    received_bodies: list[bytes] = []

    def do_POST(self) -> None:
        length = int(self.headers.get("Content-Length", 0))
        type(self).received_bodies.append(self.rfile.read(length))
        self.send_response(204)
        self.end_headers()

    def log_message(self, format: str, *args) -> None:
        pass


class _FailingHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self) -> None:
        self.send_response(400)
        self.end_headers()

    def log_message(self, format: str, *args) -> None:
        pass


@pytest.fixture
def capture_webhook_server():
    _CaptureHandler.received_bodies = []
    server = http.server.HTTPServer(("127.0.0.1", 0), _CaptureHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    yield f"http://127.0.0.1:{server.server_port}/", _CaptureHandler
    server.shutdown()
    thread.join()


@pytest.fixture
def failing_webhook_server():
    server = http.server.HTTPServer(("127.0.0.1", 0), _FailingHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    yield f"http://127.0.0.1:{server.server_port}/"
    server.shutdown()
    thread.join()


def test_format_message_includes_every_item():
    message = format_message([{"title": "first"}, {"title": "second"}])
    assert "first" in message
    assert "second" in message


def test_format_message_empty_items():
    assert format_message([]) == ""


def test_send_without_webhook_url_returns_false(monkeypatch):
    monkeypatch.delenv("DISCORD_WEBHOOK_URL", raising=False)
    assert send("hello") is False


def test_send_posts_message_content(monkeypatch, capture_webhook_server):
    url, handler = capture_webhook_server
    monkeypatch.setenv("DISCORD_WEBHOOK_URL", url)

    assert send("hello world") is True

    assert len(handler.received_bodies) == 1
    payload = json.loads(handler.received_bodies[0])
    assert payload["content"] == "hello world"


def test_send_returns_false_on_webhook_error(monkeypatch, failing_webhook_server):
    monkeypatch.setenv("DISCORD_WEBHOOK_URL", failing_webhook_server)
    assert send("hello") is False
