"""Characterization tests for legacy/report.py.

Lock down CURRENT behavior of fmt() and render() as-is (bugs included).
Do not "fix" anything here if a future refactor changes behavior, these
tests are expected to fail and must be re-pinned deliberately.
"""
import os
import re
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest

from legacy import report

LOG_LINE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2} (hit|miss) \d+$")


def _read_log_lines():
    if not os.path.exists(report._LOG):
        return []
    with open(report._LOG, encoding="utf-8") as f:
        return f.readlines()


@pytest.fixture(autouse=True)
def _reset_cache():
    report._CACHE.clear()
    yield
    report._CACHE.clear()


def test_fmt_basic_two_items():
    items = [
        {"title": "First Paper", "url": "http://a.example/1"},
        {"title": "Second Paper", "url": "http://a.example/2"},
    ]
    assert report.fmt(items) == (
        " 1. First Paper\n"
        "    http://a.example/1\n"
        " 2. Second Paper\n"
        "    http://a.example/2"
    )


def test_fmt_missing_title_defaults_empty():
    items = [{}]
    assert report.fmt(items) == " 1. "


def test_fmt_title_is_stripped():
    items = [{"title": "  padded title  "}]
    assert report.fmt(items) == " 1. padded title"


def test_fmt_title_exact_width_not_truncated():
    title = "x" * 80
    items = [{"title": title}]
    assert report.fmt(items, w=80) == " 1. " + title


def test_fmt_title_over_width_truncated():
    title = "x" * 81
    items = [{"title": title}]
    out = report.fmt(items, w=80)
    expected = " 1. " + "x" * 77 + "..."
    assert out == expected
    # truncated title portion is exactly w chars long
    assert len(out.split(". ", 1)[1]) == 80


def test_fmt_url_omitted_when_missing():
    items = [{"title": "No URL"}]
    assert report.fmt(items) == " 1. No URL"


def test_fmt_url_omitted_when_falsy():
    items = [{"title": "Empty URL", "url": ""}]
    assert report.fmt(items) == " 1. Empty URL"


def test_fmt_empty_items_returns_empty_string():
    assert report.fmt([]) == ""


def test_fmt_caches_by_length_not_content_stale_hit():
    """Known quirk: cache key is len(items), so a second call with a
    different-content list of the SAME length returns the stale result
    from the first call instead of recomputing."""
    first = [{"title": "Original A"}, {"title": "Original B"}]
    second = [{"title": "Different A"}, {"title": "Different B"}]

    first_result = report.fmt(first)
    second_result = report.fmt(second)

    assert second_result == first_result
    assert "Different" not in second_result


def test_fmt_cache_hit_ignores_w_param():
    items = [{"title": "x" * 81}]
    first_result = report.fmt(items, w=80)
    second_result = report.fmt(items, w=10)
    assert second_result == first_result


def test_fmt_logs_miss_then_hit_to_log_file():
    items_len2 = [{"title": "A"}, {"title": "B"}]

    before = len(_read_log_lines())
    report.fmt(items_len2)
    after_miss = _read_log_lines()
    assert len(after_miss) == before + 1
    assert after_miss[-1].rstrip("\n").endswith("miss 2")
    assert LOG_LINE_RE.match(after_miss[-1].rstrip("\n"))

    report.fmt(items_len2)
    after_hit = _read_log_lines()
    assert len(after_hit) == before + 2
    assert after_hit[-1].rstrip("\n").endswith("hit 2")
    assert LOG_LINE_RE.match(after_hit[-1].rstrip("\n"))


def test_render_empty_items_returns_fixed_message():
    assert report.render([]) == "새 논문 없음"


def test_render_default_header():
    items = [{"title": "Only Paper", "url": "http://a.example/1"}]
    out = report.render(items)
    expected_header = "주간 리포트 (1건)"
    expected = "%s\n%s\n%s" % (
        expected_header,
        "-" * len(expected_header),
        " 1. Only Paper\n    http://a.example/1",
    )
    assert out == expected


def test_render_custom_header():
    items = [{"title": "Paper"}]
    out = report.render(items, header="Custom Header")
    expected = "%s\n%s\n%s" % ("Custom Header", "-" * len("Custom Header"), " 1. Paper")
    assert out == expected


def test_render_inherits_fmt_length_cache_quirk():
    """render() calls fmt(items) with the default width, so it also
    inherits the stale-cache-by-length bug across separate render() calls."""
    first_items = [{"title": "First"}]
    second_items = [{"title": "Second"}]

    first_out = report.render(first_items)
    second_out = report.render(second_items)

    assert "First" in first_out
    assert "First" in second_out
    assert "Second" not in second_out
