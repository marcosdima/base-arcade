from ..core import Color, ColorProp, Draw, Font
from .geometry import Rect

UNSET = object()
HEREDITARY = ['font']


class BaseData:
    def is_set(self, value) -> bool:
        return value is not UNSET

    def resolve_value(self, tries: list[str], default_value) -> float:
        for intent in tries:
            value = getattr(self, intent)
            if value is not UNSET:
                return value
        return default_value


class Margin(BaseData):
    def __init__(
        self,
        margin: float | None = None,
        top: float | None = None,
        right: float | None = None,
        bottom: float | None = None,
        left: float | None = None,
        horizontal: float | None = None,
        vertical: float | None = None,
    ):
        super().__init__()

        self.margin = margin if margin is not None else UNSET
        self.top = top if top is not None else UNSET
        self.right = right if right is not None else UNSET
        self.bottom = bottom if bottom is not None else UNSET
        self.left = left if left is not None else UNSET
        self.horizontal = horizontal if horizontal is not None else UNSET
        self.vertical = vertical if vertical is not None else UNSET

    def get_tuple(self) -> tuple[float, float, float, float]:
        return (
            self.resolve_value(['top', 'vertical', 'margin'], 0),
            self.resolve_value(['right', 'horizontal', 'margin'], 0),
            self.resolve_value(['bottom', 'vertical', 'margin'], 0),
            self.resolve_value(['left', 'horizontal', 'margin'], 0),
        )

    def copy(self) -> 'Margin':
        return Margin(
            margin=self.margin,
            top=self.top,
            right=self.right,
            bottom=self.bottom,
            left=self.left,
            horizontal=self.horizontal,
            vertical=self.vertical,
        )


class Padding(BaseData):
    def __init__(
        self,
        padding: float | None = None,
        top: float | None = None,
        right: float | None = None,
        bottom: float | None = None,
        left: float | None = None,
        horizontal: float | None = None,
        vertical: float | None = None,
    ):
        super().__init__()

        self.padding = padding if padding is not None else UNSET
        self.top = top if top is not None else UNSET
        self.right = right if right is not None else UNSET
        self.bottom = bottom if bottom is not None else UNSET
        self.left = left if left is not None else UNSET
        self.horizontal = horizontal if horizontal is not None else UNSET
        self.vertical = vertical if vertical is not None else UNSET

    def get_tuple(self) -> tuple[float, float, float, float]:
        return (
            self.resolve_value(['top', 'vertical', 'padding'], 0),
            self.resolve_value(['right', 'horizontal', 'padding'], 0),
            self.resolve_value(['bottom', 'vertical', 'padding'], 0),
            self.resolve_value(['left', 'horizontal', 'padding'], 0),
        )

    def copy(self) -> 'Padding':
        return Padding(
            padding=self.padding,
            top=self.top,
            right=self.right,
            bottom=self.bottom,
            left=self.left,
            horizontal=self.horizontal,
            vertical=self.vertical,
        )


class Border(BaseData):
    def __init__(
        self,
        color: ColorProp | None = None,
        width: float = 0,
        radius: float = 0,
        top: float | None = None,
        right: float | None = None,
        bottom: float | None = None,
        left: float | None = None,
        lateral: float | None = None,
        horizontal: float | None = None,
        top_left: float | None = None,
        top_right: float | None = None,
        bottom_right: float | None = None,
        bottom_left: float | None = None,
    ):
        super().__init__()

        self.color: Color = Color(color) if color is not None else UNSET

        self.width: float = width
        self.top: float = top if top is not None else UNSET
        self.right: float = right if right is not None else UNSET
        self.bottom: float = bottom if bottom is not None else UNSET
        self.left: float = left if left is not None else UNSET

        self.lateral: float = lateral if lateral is not None else UNSET
        self.horizontal: float = horizontal if horizontal is not None else UNSET

        self.radius: float = radius if radius is not None else UNSET
        self.top_left: float = top_left if top_left is not None else UNSET
        self.top_right: float = top_right if top_right is not None else UNSET
        self.bottom_right: float = bottom_right if bottom_right is not None else UNSET
        self.bottom_left: float = bottom_left if bottom_left is not None else UNSET

    def get_tuple(self) -> tuple[float, float, float, float]:
        return (
            self.resolve_value(['top', 'horizontal', 'width'], 0),
            self.resolve_value(['right', 'lateral', 'width'], 0),
            self.resolve_value(['bottom', 'horizontal', 'width'], 0),
            self.resolve_value(['left', 'lateral', 'width'], 0),
        )

    def get_radius_tuple(self) -> tuple[float, float, float, float]:
        return (
            self.resolve_value(['top_left', 'radius'], 0),
            self.resolve_value(['top_right', 'radius'], 0),
            self.resolve_value(['bottom_right', 'radius'], 0),
            self.resolve_value(['bottom_left', 'radius'], 0),
        )

    def copy(self) -> 'Border':
        return Border(
            color=self.color.as_tuple() if self.is_set(self.color) else None,
            width=self.width if self.is_set(self.width) else 0,
            radius=self.radius if self.is_set(self.radius) else 0,
            top=self.top if self.is_set(self.top) else None,
            right=self.right if self.is_set(self.right) else None,
            bottom=self.bottom if self.is_set(self.bottom) else None,
            left=self.left if self.is_set(self.left) else None,
            lateral=self.lateral if self.is_set(self.lateral) else None,
            horizontal=self.horizontal if self.is_set(self.horizontal) else None,
            top_left=self.top_left if self.is_set(self.top_left) else None,
            top_right=self.top_right if self.is_set(self.top_right) else None,
            bottom_right=self.bottom_right if self.is_set(self.bottom_right) else None,
            bottom_left=self.bottom_left if self.is_set(self.bottom_left) else None,
        )


class Style(BaseData):
    def __init__(
        self,
        background_color: ColorProp | None = None,
        margin: Margin | None = None,
        padding: Padding | None = None,
        border: Border | None = None,
        font: Font | None = None,
    ):
        self.background_color: Color = (
            Color(background_color) if background_color is not None else UNSET
        )
        self.margin: Margin = margin if margin is not None else UNSET
        self.padding: Padding = padding if padding is not None else UNSET
        self.border: Border = border if border is not None else UNSET
        self.font: Font = font if font is not None else UNSET

    def draw_background(self, rect: Rect):
        has_background = self.is_set(self.background_color)
        has_border = self.is_set(self.border) and self.border.is_set(self.border.width)

        # Do nothing.
        if not has_border and not has_background:
            return

        start_x, start_y = (rect.x - rect.width / 2, rect.y - rect.height / 2)

        if not has_border:  # TODO: This does not work. Draws a rect.
            return

        tl, tr, br, bl = self.border.get_radius_tuple()
        Draw.filled_rounded_rect(
            xywh=(start_x, start_y, rect.width, rect.height),
            color=self.background_color if has_background else Color('transparent'),
            radius=(tl, tr, br, bl),
        )
        Draw.outline_rounded_rect(
            xywh=(start_x, start_y, rect.width, rect.height),
            color=self.border.color,
            radius=(tl, tr, br, bl),
            border_width=self.border.width,
        )

    def merge(self, other: 'Style', exclude: set[str] = set()) -> 'Style':  # noqa: B006
        merged_fields = Style()

        for name in self.__dict__:
            if name in exclude:
                continue

            val = getattr(self, name)
            other_val = getattr(other, name)
            setattr(merged_fields, name, val if self.is_set(val) else other_val)

        return merged_fields

    def heritage(self, parent_style: 'Style'):
        # Get hereditary fields from parent style.
        hereditary_fields = parent_style.get_hereditary_fields()
        for name, value in hereditary_fields.items():
            if not self.is_set(getattr(self, name)):
                setattr(self, name, value)

    def get_hereditary_fields(self) -> dict[str, any]:
        return {name: getattr(self, name, UNSET) for name in HEREDITARY}

    def copy(self) -> 'Style':
        return Style(
            background_color=self.background_color.as_tuple()
            if self.is_set(self.background_color)
            else None,
            margin=self.margin.copy() if self.is_set(self.margin) else UNSET,
            padding=self.padding.copy() if self.is_set(self.padding) else UNSET,
            border=self.border.copy() if self.is_set(self.border) else UNSET,
            font=self.font.copy() if self.is_set(self.font) else UNSET,
        )
