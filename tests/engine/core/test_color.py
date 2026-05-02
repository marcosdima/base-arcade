import pytest

from src.engine.core import Color


def test_color_initialization():
    # Test with a color name
    color = Color('red')
    assert color.as_tuple() == (255, 0, 0, 255), (
        f'Expected (255, 0, 0, 255) but got {color.as_tuple()}'
    )

    # Test with an RGB tuple
    color = Color((0, 255, 0))
    assert color.as_tuple() == (0, 255, 0, 255), (
        f'Expected (0, 255, 0, 255) but got {color.as_tuple()}'
    )

    # Test with an RGBA tuple
    color = Color((0, 0, 255, 128))
    assert color.as_tuple() == (0, 0, 255, 128), (
        f'Expected (0, 0, 255, 128) but got {color.as_tuple()}'
    )

    # Test with an invalid color name
    with pytest.raises(ValueError):
        Color('notacolor')

    # Test with an invalid RGB tuple
    with pytest.raises(ValueError):
        Color((256, -1, 300))

    # Test with an invalid RGBA tuple
    with pytest.raises(ValueError):
        Color((0, 0, 255, -10))
