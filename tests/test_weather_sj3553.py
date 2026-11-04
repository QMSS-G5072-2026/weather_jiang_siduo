import math

import pandas as pd
import pytest

import weather_sj3553
from weather_sj3553 import (
    celsius_to_fahrenheit,
    summarize_temperatures,
    clean_readings,
)


@pytest.fixture
def raw_readings():
    return pd.DataFrame(
        {
            "station": ["B", "A", "A", "B", "A"],
            "date": [
                "2026-01-02",
                "2026-01-02",
                "2026-01-01",
                "2026-01-01",
                "2026-01-03",
            ],
            "temp_c": [20.0, 10.0, math.nan, 100.0, -100.0],
        }
    )


def test_version_is_defined():
    assert isinstance(weather_sj3553.__version__, str)


def test_celsius_to_fahrenheit():
    assert celsius_to_fahrenheit(0) == 32.0
    assert celsius_to_fahrenheit(100) == 212.0


def test_celsius_to_fahrenheit_invalid_type():
    with pytest.raises(TypeError):
        celsius_to_fahrenheit("cold")


def test_celsius_to_fahrenheit_below_absolute_zero():
    with pytest.raises(ValueError):
        celsius_to_fahrenheit(-300)


def test_summarize_temperatures():
    result = summarize_temperatures([10.0, 20.0, float("nan")])

    assert result["mean"] == 15.0
    assert result["min"] == 10.0
    assert result["max"] == 20.0
    assert result["n_missing"] == 1


def test_summarize_temperatures_no_valid_values():
    with pytest.raises(ValueError):
        summarize_temperatures([float("nan"), float("nan")])


def test_clean_readings(raw_readings):
    result = clean_readings(raw_readings)

    assert len(result) == 2

    assert list(result["station"]) == ["A", "B"]
    assert list(result["temp_c"]) == [10.0, 20.0]
    assert list(result["temp_f"]) == [50.0, 68.0]

    assert list(result.index) == [0, 1]


def test_clean_readings_does_not_modify_input(raw_readings):
    original = raw_readings.copy()

    clean_readings(raw_readings)

    pd.testing.assert_frame_equal(raw_readings, original)