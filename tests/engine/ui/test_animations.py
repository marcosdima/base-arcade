from __future__ import annotations

import pytest

from src.engine.core import Color
from src.engine.ui.ui_element.animations import AnimatedValue, lerp


def test_lerp_basic():
    assert lerp(0.0, 10.0, 0.0) == 0.0
    assert lerp(0.0, 10.0, 1.0) == 10.0
    assert lerp(0.0, 10.0, 0.5) == 5.0


def test_animated_value_float_progress():
    av = AnimatedValue(
        duration=1.0,
        speed=0.5,
    )

    av.start(0.0, 1.0)

    # Simulate updates: with speed 0.5 and dt=0.2 -> increment 0.1 per update
    step = 0.1
    while av.is_playing():
        av.update(step)
        assert 0.0 <= av.value <= 1.0

    # After sufficient updates, value should reach target (or be very close)
    assert av.value == 1.0


def test_animated_value_color_progress():
    start = Color('red')
    end = Color('green')

    av = AnimatedValue(duration=1.0, speed=1.0)

    av.start(start, end)

    # Fist, value should be at start color.
    v = av.value
    assert v.r == start.r and v.g == start.g and v.b == start.b and v.a == start.a

    step = 0.1
    while av.is_playing():
        av.update(step)

    v = av.value
    assert isinstance(v, Color)
    assert v.r == end.r and v.g == end.g and v.b == end.b and v.a == end.a


def test_start_type_mismatch_raises():
    av = AnimatedValue(duration=1.0, speed=1.0)
    with pytest.raises(ValueError):
        av.start(0.0, Color('blue'))
