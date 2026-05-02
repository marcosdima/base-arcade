from dataclasses import dataclass, field, fields

from ..core import Color, ColorProp, Font

UNSET = object()


def unset_field():
    return field(default=UNSET)


def color_field():
    return field(default=UNSET, metadata={'color': True})


MARGIN_COMBINATION = {
    'top': 'vertical',
    'right': 'horizontal',
    'bottom': 'vertical',
    'left': 'horizontal',
}


@dataclass
class BaseDataClass:
    def __post_init__(self):
        for f in fields(self):
            value = getattr(self, f.name)
            if f.metadata.get('color') and value is not UNSET:
                setattr(self, f.name, Color(value))

    def is_set(self, key: str) -> bool:
        return getattr(self, key) is not UNSET

    def resolve_value(self, tries: list[str], default_value) -> float:
        for intent in tries:
            value = getattr(self, intent)
            if value is not UNSET:
                return value
        return default_value


@dataclass
class Margin(BaseDataClass):
    margin: float = unset_field()
    top: float = unset_field()
    right: float = unset_field()
    bottom: float = unset_field()
    left: float = unset_field()
    horizontal: float = unset_field()
    vertical: float = unset_field()

    def get_tuple(self) -> tuple[float, float, float, float]:
        return (
            self.resolve_value(['top', 'vertical', 'margin'], 0),
            self.resolve_value(['right', 'horizontal', 'margin'], 0),
            self.resolve_value(['bottom', 'vertical', 'margin'], 0),
            self.resolve_value(['left', 'horizontal', 'margin'], 0),
        )


@dataclass
class Padding(BaseDataClass):
    padding: float = unset_field()
    top: float = unset_field()
    right: float = unset_field()
    bottom: float = unset_field()
    left: float = unset_field()
    horizontal: float = unset_field()
    vertical: float = unset_field()

    def get_tuple(self) -> tuple[float, float, float, float]:
        return (
            self.resolve_value(['top', 'vertical', 'padding'], 0),
            self.resolve_value(['right', 'horizontal', 'padding'], 0),
            self.resolve_value(['bottom', 'vertical', 'padding'], 0),
            self.resolve_value(['left', 'horizontal', 'padding'], 0),
        )


@dataclass
class Border(BaseDataClass):
    color: ColorProp = color_field()

    width: float = unset_field()
    top: float = unset_field()
    right: float = unset_field()
    bottom: float = unset_field()
    left: float = unset_field()

    lateral: float = unset_field()
    horizontal: float = unset_field()

    radius: float = unset_field()
    top_left: float = unset_field()
    top_right: float = unset_field()
    bottom_right: float = unset_field()
    bottom_left: float = unset_field()

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


@dataclass
class Style(BaseDataClass):
    background_color: ColorProp = color_field()
    margin: Margin = field(default_factory=Margin)
    padding: Padding = field(default_factory=Padding)
    border: Border = field(default_factory=Border)
    font: Font = unset_field()

    def merge(self, other: 'Style') -> 'Style':
        merged_fields = {}

        for f in fields(self):
            if self.is_set(f.name):
                merged_fields[f.name] = getattr(self, f.name)
            elif other.is_set(f.name):
                merged_fields[f.name] = getattr(other, f.name)

        return self.__class__(**merged_fields)
