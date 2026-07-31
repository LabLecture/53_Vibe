"""Day 3 · 3.10 [실습] 정답본 — 누수 없는 ML 파이프라인.

교안 3.10에서 에이전트에게 만들게 하는 `ml_pipeline.py` 의 참고 답안이다.
먼저 직접(또는 에이전트로) 만들어 본 뒤에 대조용으로 열어 볼 것.

핵심: 전처리(특성 선택·스케일)를 **모두 sklearn Pipeline 안에** 넣는다.
그러면 `fit` 이 train 에만 적용되는 것이 **구조적으로 보장**된다 —
사람이 순서를 기억할 필요가 없어진다.
"""

from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

DEFAULT_K = 20
TEST_SIZE = 0.3


def build_pipeline(k: int = DEFAULT_K) -> Pipeline:
    """특성 선택 → 표준화 → 분류를 하나로 묶은 파이프라인.

    세 단계가 한 객체이므로 ``fit(Xtr, ytr)`` 한 번이면 **전처리까지 train
    에만** 학습된다. 분할 전에 실수로 전체 데이터를 만질 여지가 없다.
    """
    return Pipeline([
        ("select", SelectKBest(f_classif, k=k)),
        ("scale", StandardScaler()),
        ("clf", LogisticRegression(max_iter=1000)),
    ])


def run_experiment(X, y, k: int = DEFAULT_K, random_state: int = 0) -> float:
    """*X*, *y* 를 분할해 학습하고 **test 정확도**를 돌려준다.

    ``k`` 가 특성 수보다 크면 특성 수에 맞춘다(작은 데이터셋 대응).
    """
    k = min(k, X.shape[1])
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_SIZE, random_state=random_state
    )
    pipeline = build_pipeline(k).fit(X_train, y_train)
    return accuracy_score(y_test, pipeline.predict(X_test))


if __name__ == "__main__":
    from sklearn.datasets import load_wine

    wine = load_wine()
    print(f"wine test acc: {run_experiment(wine.data, wine.target):.3f}")
