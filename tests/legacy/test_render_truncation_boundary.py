"""render() 의 2000자 자르기: 줄 단위로만 자르고, "외 N건" 의 N 이 정확해야 하며,
어떤 입력에서도 결과 길이가 2000자를 넘으면 안 된다. 2000자 근처 경계 입력도 검증한다.
"""
import re

import pytest

from legacy import report

_LINE_RE = re.compile(
    r"^(주간 리포트 \(\d+건\)|-+|\s*\d+\.\s.*|\s+http\S*|외 \d+건)$"
)


@pytest.fixture(autouse=True)
def isolate_global_state(tmp_path, monkeypatch):
    monkeypatch.setattr(report, "_CACHE", {})
    monkeypatch.setattr(report, "_LOG", str(tmp_path / "report.log"))


def _single_line_items(n):
    return [{"title": "x" * 10, "url": None} for _ in range(n)]


def _two_line_items(n):
    return [
        {"title": "Paper %d has a reasonably descriptive title" % i,
         "url": "http://arxiv.org/abs/%05d" % i}
        for i in range(n)
    ]


def _assert_no_partial_line(result):
    for line in result.splitlines():
        assert _LINE_RE.match(line), "잘린 줄: %r" % line


def test_result_never_exceeds_2000_chars_for_various_sizes():
    for n in (1, 10, 50, 150, 300, 1000):
        result = report.render(_two_line_items(n))
        assert len(result) <= 2000
        _assert_no_partial_line(result)


def test_omitted_count_matches_actual_dropped_items():
    items = _two_line_items(300)
    result = report.render(items)
    assert len(result) <= 2000
    m = re.search(r"외 (\d+)건$", result)
    assert m, "잘렸는데 '외 N건' 표시가 없음"
    omitted = int(m.group(1))
    visible = len(re.findall(r"^\s*\d+\.\s", result, re.MULTILINE))
    assert visible + omitted == len(items)


def test_boundary_transition_near_2000_chars():
    prev = None
    for n in range(1, 400):
        result = report.render(_single_line_items(n))
        assert len(result) <= 2000
        if prev is not None and "외" not in prev and "외" in result:
            assert 1900 <= len(prev) <= 2000
            _assert_no_partial_line(prev)
            _assert_no_partial_line(result)
            return
        prev = result
    pytest.fail("2000자 경계를 찾지 못함")
