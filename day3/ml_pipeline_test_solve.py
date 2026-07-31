"""Day 3 · 3.10 [실습] 정답본 — 누수 탐지 게이트.

교안 3.10 ①에서 에이전트에게 먼저 만들게 하는 `test_ml_pipeline.py` 의 참고 답안.
(파일명이 ``test_*.py`` 가 아니라 pytest 가 자동 수집하지 않는다 — 대조용이다.)

핵심 아이디어: **신호가 0인 데이터를 넣어 본다.**
특성도 정답도 난수라면 어떤 모델이든 정답률은 동전 던지기(0.5) 근처여야 한다.
그보다 뚜렷이 높다면 학습을 잘한 게 아니라 **test 를 훔쳐본 것**이다.

실측 기준(시드 8개):
    올바른 구현 0.417 ~ 0.567   |   누수 구현 0.700 ~ 0.800
따라서 임계값 0.65 가 양쪽에 여유를 두고 둘을 가른다.
"""

import numpy as np
import pytest
from sklearn.datasets import load_wine

from ml_pipeline import run_experiment

LEAK_GATE = 0.65


def make_pure_noise(seed: int):
    """신호가 전혀 없는 데이터 — 특성도 정답도 난수."""
    rng = np.random.default_rng(seed)
    return rng.normal(size=(200, 2000)), rng.integers(0, 2, size=200)


def test_wine_baseline_is_reasonable():
    """진짜 신호가 있는 데이터에서는 잘 맞혀야 한다."""
    wine = load_wine()
    assert run_experiment(wine.data, wine.target) >= 0.90


@pytest.mark.parametrize("seed", [0, 1, 2, 3])
def test_no_leakage_on_pure_noise(seed):
    """신호가 0인 데이터에서 점수가 높으면 = 누수다.

    이 테스트가 실패하면 전처리(특성 선택·스케일)를 분할 **전에** 했다는 뜻이다.
    전처리를 Pipeline 안으로 넣으면 통과한다.
    """
    X, y = make_pure_noise(seed)
    acc = run_experiment(X, y, random_state=seed)
    assert acc <= LEAK_GATE, (
        f"신호가 없는 데이터에서 acc={acc:.3f} — 누수 의심. "
        "전처리를 분할 전에 하지 않았는지 확인하세요."
    )
