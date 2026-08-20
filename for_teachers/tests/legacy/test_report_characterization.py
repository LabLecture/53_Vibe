"""legacy/report.py 의 fmt()/render() 현재 동작을 고정하는 특성화 테스트.

옳고 그름은 따지지 않는다 - 지금 나오는 값을 그대로 assert 한다.
구현(legacy/report.py)은 건드리지 않는다.
"""
import re

import pytest

from legacy import report

ITEMS = [
    {"title": "Attention Is All You Need", "url": "http://arxiv.org/abs/1706.03762"},
    {"title": "Denoising Diffusion Probabilistic Models", "url": "http://arxiv.org/abs/2006.11239"},
]


@pytest.fixture(autouse=True)
def isolate_global_state(tmp_path, monkeypatch):
    """_CACHE(전역 dict)와 _LOG(로그 파일 경로)를 테스트마다 격리한다.

    실제 부작용(캐시 적재, 파일 append)은 그대로 발생시키되,
    테스트 간 오염과 저장소의 실제 report.log 오염을 막기 위해 대상만 tmp_path 로 바꾼다.
    """
    monkeypatch.setattr(report, "_CACHE", {})
    log_path = tmp_path / "report.log"
    monkeypatch.setattr(report, "_LOG", str(log_path))
    return log_path


def test_fmt_basic():
    assert report.fmt(ITEMS) == (
        " 1. Attention Is All You Need\n"
        "    http://arxiv.org/abs/1706.03762\n"
        " 2. Denoising Diffusion Probabilistic Models\n"
        "    http://arxiv.org/abs/2006.11239"
    )


def test_fmt_truncates_long_title_default_width():
    long_items = [{"title": "x" * 100, "url": None}]
    assert report.fmt(long_items) == " 1. " + "x" * 77 + "..."


def test_fmt_truncates_long_title_custom_width():
    long_items = [{"title": "x" * 100, "url": None}]
    assert report.fmt(long_items, w=10) == " 1. xxxxxxx..."


def test_fmt_missing_title_defaults_to_empty_string():
    assert report.fmt([{"url": "http://x"}]) == " 1. \n    http://x"


def test_fmt_missing_url_omits_url_line():
    assert report.fmt([{"title": "no url here"}]) == " 1. no url here"


def test_fmt_empty_items_returns_empty_string():
    assert report.fmt([]) == ""


def test_render_basic():
    assert report.render(ITEMS) == (
        "주간 리포트 (2건)\n"
        "-----------\n"
        " 1. Attention Is All You Need\n"
        "    http://arxiv.org/abs/1706.03762\n"
        " 2. Denoising Diffusion Probabilistic Models\n"
        "    http://arxiv.org/abs/2006.11239"
    )


def test_render_empty_items():
    assert report.render([]) == "새 논문 없음"


def test_render_custom_header():
    assert report.render(ITEMS, header="custom") == (
        "custom\n"
        "------\n"
        " 1. Attention Is All You Need\n"
        "    http://arxiv.org/abs/1706.03762\n"
        " 2. Denoising Diffusion Probabilistic Models\n"
        "    http://arxiv.org/abs/2006.11239"
    )


def test_fmt_caches_by_content_and_width():
    """같은 (w, items 내용) 이면 두 번째 호출은 캐시에서 그대로 반환된다."""
    first = report.fmt(ITEMS)
    assert len(report._CACHE) == 1
    key = (80, tuple((it.get("title", ""), it.get("url")) for it in ITEMS))
    assert key in report._CACHE

    second = report.fmt(ITEMS)
    assert second == first


def test_fmt_writes_miss_then_hit_to_log_file(isolate_global_state):
    log_path = isolate_global_state

    report.fmt(ITEMS)
    lines = log_path.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 1
    assert re.match(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2} miss 2$", lines[0])

    report.fmt(ITEMS)
    lines = log_path.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 2
    assert re.match(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2} hit 2$", lines[1])
