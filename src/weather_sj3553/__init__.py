# read version from installed package
from importlib.metadata import version
__version__ = version("weather_sj3553")

from .weather_sj3553 import (
    celsius_to_fahrenheit,
    summarize_temperatures,
    clean_readings,
)