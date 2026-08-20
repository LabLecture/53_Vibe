"""title 이 비어있거나 공백뿐인 항목은 render() 목록에서 빠지고, 남은 항목만 1부터 재번호.

legacy/report.py 는 이 파일 작성 후 통과하도록 수정한다.
"""
import pytest

from legacy import report


@pytest.fixture(autouse=True)
def isolate_global_state(tmp_path, monkeypatch):
    monkeypatch.setattr(report, "_CACHE", {})
    monkeypatch.setattr(report, "_LOG", str(tmp_path / "report.log"))


def test_render_skips_blank_and_whitespace_titles_and_renumbers():
    items = [
        {"title": "", "url": "http://a"},
        {"title": "Valid One", "url": "http://b"},
        {"title": "   ", "url": "http://c"},
        {"title": "Valid Two", "url": "http://d"},
    ]
    assert report.render(items) == (
        "주간 리포트 (2건)\n"
        "-----------\n"
        " 1. Valid One\n"
        "    http://b\n"
        " 2. Valid Two\n"
        "    http://d"
    )


def test_render_all_blank_titles_returns_empty_message():
    items = [{"title": ""}, {"title": "   ", "url": "http://x"}]
    assert report.render(items) == "새 논문 없음"
