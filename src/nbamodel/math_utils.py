from __future__ import annotations


def as_float(value: object, default: float = 0.0) -> float:
    if value is None:
        return default
    try:
        text = str(value).strip()
        if text == "":
            return default
        return float(text)
    except (TypeError, ValueError):
        return default


def as_bool(value: object) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def normalize(value: float, scale: float, low: float = -1.0, high: float = 1.0) -> float:
    if scale == 0:
        return 0.0
    return clamp(value / scale, low, high)


def american_implied_probability(odds: float) -> float:
    if odds == 0:
        return 0.5
    if odds < 0:
        return abs(odds) / (abs(odds) + 100.0)
    return 100.0 / (odds + 100.0)
