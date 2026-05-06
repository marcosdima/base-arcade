from dataclasses import dataclass, field, fields

from ..core import Color, ColorProp, Draw, Font
from .geometry import Rect

UNSET = object()


def unset_field():
    return field(default=UNSET)


def hereditary_field():
    return field(default=UNSET, metadata={'hereditary': True})


@dataclass
class BaseDataClass:
    def is_set(self, key: str) -> bool:
        try:
            val = getattr(self, key)
        except AttributeError:
            try:
                val = getattr(self, f'_{key}')
            except AttributeError:
                return False
        return val is not UNSET

    def __getattribute__(self, name: str):
        # Use the base implementation to avoid recursion.
        val = object.__getattribute__(self, name)

        # Only attempt color wrapping for dataclass fields containing 'color'.
        try:
            for f in fields(self):
                if f.name == name and 'color' in f.name:
                    # If the stored value is UNSET or already a Color, return as-is.
                    if val is UNSET or isinstance(val, Color):
                        return val
                    return Color(val)
        except Exception:
            # If anything goes wrong (e.g., fields() can't operate), fall back to raw value.
            return val

        return val

    def resolve_value(self, tries: list[str], default_value) -> float:
        for intent in tries:
            value = getattr(self, intent)
            if value is not UNSET:
                return value
        return default_value

    def is_color_field(self, f) -> bool:
        # Basic heuristic: field name contains 'color'
        return hasattr(f, 'name') and 'color' in f.name

    def get_hereditary_fields(self) -> dict[str, any]:
        return {
            f.name: getattr(self, f.name)
            for f in fields(self)
            if f.metadata.get('hereditary') and self.is_set(f.name)
        }


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
    color: ColorProp = unset_field()

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
    background_color: ColorProp = unset_field()
    margin: Margin = field(default_factory=Margin)
    padding: Padding = field(default_factory=Padding)
    border: Border = field(default_factory=Border)
    font: Font = hereditary_field()

    def draw_background(self, rect: Rect):
        Draw.draw_rect(rect=rect, style=self)

    def merge(self, other: 'Style') -> 'Style':
        merged_fields = Style()

        for f in fields(self):
            name = f.name
            if self.is_set(name):
                setattr(merged_fields, name, getattr(self, name))
            elif other.is_set(name):
                setattr(merged_fields, name, getattr(other, name))

        return merged_fields

    def heritage(self, parent_style: 'Style'):
        # Get hereditary fields from parent style.
        hereditary_fields = parent_style.get_hereditary_fields()
        for name, value in hereditary_fields.items():
            if not self.is_set(name):
                setattr(self, name, value)
