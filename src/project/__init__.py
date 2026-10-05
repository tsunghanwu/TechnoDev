"""Reusable starter functionality for scripts and notebooks."""

from collections.abc import Iterable


def mean(values: Iterable[float]) -> float:
    """Return the arithmetic mean of a non-empty iterable of numbers."""
    total = 0.0
    count = 0
    for value in values:
        total += value
        count += 1
    if count == 0:
        raise ValueError("mean requires at least one value")
    return total / count
