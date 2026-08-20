"""render() 결과가 Discord 메시지 한도(2000자)를 넘으면 안 된다는 요구의 테스트.

구현(legacy/report.py)은 아직 이 요구를 반영하지 않는다 - 실패가 정상(레드).
legacy/ 는 건드리지 않는다.
"""
import pytest

from legacy import report

ITEMS = [
    {"title": "Attention Is All You Need", "url": "http://arxiv.org/abs/1706.03762"},
    {"title": "Denoising Diffusion Probabilistic Models", "url": "http://arxiv.org/abs/2006.11239"},
]


@pytest.fixture(autouse=True)
def isolate_global_state(tmp_path, monkeypatch):
    monkeypatch.setattr(report, "_CACHE", {})
    monkeypatch.setattr(report, "_LOG", str(tmp_path / "report.log"))


def test_render_short_list_unchanged():
    assert report.render(ITEMS) == (
        "주간 리포트 (2건)\n"
        "-----------\n"
        " 1. Attention Is All You Need\n"
        "    http://arxiv.org/abs/1706.03762\n"
        " 2. Denoising Diffusion Probabilistic Models\n"
        "    http://arxiv.org/abs/2006.11239"
    )


def test_render_long_list_truncated_under_2000_chars():
    long_items = [
        {"title": "paper title %d" % i, "url": "http://arxiv.org/abs/%04d" % i}
        for i in range(200)
    ]
    result = report.render(long_items)
    assert len(result) <= 2000
    assert "외" in result and "건" in result
