import pytest

from src.engine.ui.core.geometry import Point, Rect


def test_point_addition():
    # Point + Point.
    p1 = Point(1, 2)
    p2 = Point(3, 4)
    result = p1 + p2
    assert result.x == 4 and result.y == 6, 'Point addition failed for Point + Point.'

    # Point + (x, y).
    p3 = Point(1, 2)
    result = p3 + (3, 4)
    assert result.x == 4 and result.y == 6, 'Point addition failed for Point + (x, y).'


def test_point_addition_invalid():
    p = Point(1, 2)

    with pytest.raises(TypeError):
        p + 'invalid'

    with pytest.raises(ValueError):
        p + (1, '2')


def test_point_parsing():
    # Tuple (int, int).
    p = Point.parse_from_tuple((5, 6))
    assert p.x == 5 and p.y == 6, 'Point parsing failed.'

    # Tuple (float, float).
    p = Point.parse_from_tuple((1.5, 2.5))
    assert p.x == 1.5 and p.y == 2.5, 'Point parsing failed for float values.'

    # Tuple with more than 2 values.
    p = Point.parse_from_tuple((1, 2, 3))
    assert p.x == 1 and p.y == 2, (
        'Point parsing failed for tuple with more than 2 values.'
    )


def test_point_parsing_invalid():
    with pytest.raises(ValueError):
        Point.parse_from_tuple((1,))  # Not enough values.

    with pytest.raises(ValueError):
        Point.parse_from_tuple((1, 'a'))  # Non-numeric value.


def test_rect_properties():
    rect = Rect(Point(1, 2), width=4, height=6)

    assert rect.x == 1, 'Rect x property failed.'
    assert rect.y == 2, 'Rect y property failed.'
    assert rect.center_x == 3, 'Rect center_x property failed.'
    assert rect.center_y == 5, 'Rect center_y property failed.'
    assert rect.center.x == 3 and rect.center.y == 5, 'Rect center property failed.'


def test_rect_contains():
    rect = Rect(Point(0, 0), width=10, height=10)

    assert rect.contains(Point(5, 5)), (
        'Rect contains method failed for a point inside the rect.'
    )
    assert rect.contains((5, 5)), (
        'Rect contains method failed for a tuple point inside the rect.'
    )
    assert not rect.contains(Point(11, 5)), (
        'Rect contains method failed for a point outside the rect.'
    )
    assert not rect.contains((11, 5)), (
        'Rect contains method failed for a tuple point outside the rect.'
    )
