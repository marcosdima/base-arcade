from src.engine.core.color import Color
from src.engine.core.font import Font
from src.engine.ui.style import Border, Margin, Padding, Style


def test_unset_field():
    style = Style()
    assert not style.is_set(style.background_color), 'Unset field should not be set.'
    assert not style.is_set(style.margin), 'Unset field should not be set.'
    assert not style.is_set(style.border), 'Unset field should not be set.'


def test_margin_tuple():
    margin = Margin(margin=10, left=2)

    assert margin.get_tuple() == (10, 10, 10, 2), (
        'left should override margin, top, right and bottom should resolve to margin.'
    )

    margin.horizontal = 5
    assert margin.get_tuple() == (10, 5, 10, 2), (
        'after setting horizontal, right should resolve to horizontal.'
    )

    margin.vertical = 3
    assert margin.get_tuple() == (3, 5, 3, 2), (
        'after setting vertical, top and bottom should resolve to vertical.'
    )


def test_padding_tuple():
    padding = Padding(padding=5, bottom=3)

    assert padding.get_tuple() == (5, 5, 3, 5), (
        'top, right, bottom should override padding, left should resolve to padding.'
    )

    padding.horizontal = 4
    assert padding.get_tuple() == (5, 4, 3, 4), (
        'after setting horizontal, left should resolve to horizontal.'
    )

    padding.vertical = 2
    assert padding.get_tuple() == (2, 4, 3, 4), (
        'after setting vertical, top should resolve to vertical.'
    )


def test_border_width_tuple():
    border = Border(width=3, top=2)

    assert border.get_tuple() == (2, 3, 3, 3), (
        'right, bottom, left should resolve to width.'
    )

    border.horizontal = 4
    assert border.get_tuple() == (2, 3, 4, 3), (
        'after setting horizontal, bottom should resolve to horizontal.'
    )

    border.lateral = 5
    assert border.get_tuple() == (2, 5, 4, 5), (
        'after setting lateral, right and left should resolve to lateral.'
    )


def test_border_radius_tuple():
    border = Border(radius=10, top_left=5)

    assert border.get_radius_tuple() == (5, 10, 10, 10), (
        'top_left should override radius, other corners should resolve to radius.'
    )

    border.top_right = 3
    assert border.get_radius_tuple() == (5, 3, 10, 10), (
        'after setting top_right, it should override radius.'
    )

    border.bottom_left = 2
    assert border.get_radius_tuple() == (5, 3, 10, 2), (
        'after setting bottom_left, it should override radius.'
    )

    border.bottom_right = 1
    assert border.get_radius_tuple() == (5, 3, 1, 2), (
        'after setting bottom_right, it should override radius.'
    )


def test_style():
    color_tuple = (255, 0, 0, 0)
    style = Style(
        background_color=color_tuple,
        margin=Margin(margin=10, left=2),
        padding=Padding(padding=5, bottom=3),
        border=Border(width=3, top=2, radius=10, top_left=5, color='red'),
    )

    assert style.background_color == Color(color_tuple), (
        'Background color should be set correctly.'
    )
    assert style.margin.get_tuple() == (10, 10, 10, 2), (
        'Margin tuple should be correct.'
    )
    assert style.padding.get_tuple() == (5, 5, 3, 5), 'Padding tuple should be correct.'
    assert style.border.get_tuple() == (2, 3, 3, 3), (
        'Border width tuple should be correct.'
    )
    assert style.border.color == Color('red'), 'Border color should be set correctly.'
    assert style.border.get_radius_tuple() == (5, 10, 10, 10), (
        'Border radius tuple should be correct.'
    )

    style.background_color = Color('blue')
    assert style.background_color == Color('blue'), (
        'Background color should be updated correctly.'
    )


def test_style_merge():
    style1 = Style(
        background_color='red',
        margin=Margin(margin=10, left=2),
        padding=Padding(padding=5, bottom=3),
        border=Border(width=3, top=2, radius=10, top_left=5, color='red'),
    )

    style2 = Style(
        background_color='blue',
        margin=Margin(margin=20),
        padding=Padding(padding=10),
        border=Border(width=5, radius=20, color='blue'),
    )

    merged_style = style1.merge(style2)

    assert merged_style.background_color == Color('red'), (
        f'Background color should be taken from the first style, received {merged_style.bg}.'
    )
    assert merged_style.margin.get_tuple() == (10, 10, 10, 2), (
        'Margin tuple should be taken from the first style.'
    )
    assert merged_style.padding.get_tuple() == (5, 5, 3, 5), (
        'Padding tuple should be taken from the first style.'
    )
    assert merged_style.border.get_tuple() == (2, 3, 3, 3), (
        'Border width tuple should be taken from the first style.'
    )
    assert merged_style.border.color == Color('red'), (
        'Border color should be taken from the first style.'
    )
    assert merged_style.border.get_radius_tuple() == (5, 10, 10, 10), (
        'Border radius tuple should be taken from the first style.'
    )


def test_hereditary_font():
    style1 = Style(font=Font(size=12, font_color='red'))
    style2 = Style()

    assert not style2.is_set(style2.font), (
        'Font should be set in style2 after heritage.'
    )

    style2.heritage(style1)

    assert style2.font.size == 12, 'Font size should be set correctly in style2.'
    assert style2.font.color == Color('red'), (
        'Font color should be inherited from style1 in style2.'
    )

    style3 = Style(font=Font(size=14))
    style3.heritage(style1)

    assert style3.font.size == 14, (
        'Font size should not be inherited from style1 in style3 since it is already set.'
    )
