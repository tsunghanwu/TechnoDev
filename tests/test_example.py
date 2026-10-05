import pytest

from project import mean


def test_mean_returns_arithmetic_mean() -> None:
    assert mean([2, 4, 6]) == 4


def test_mean_accepts_iterators() -> None:
    assert mean(value for value in [1, 2, 3]) == 2


def test_mean_rejects_empty_input() -> None:
    with pytest.raises(ValueError, match="at least one value"):
        mean([])
