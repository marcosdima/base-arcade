from dataclasses import dataclass
from typing import Literal

import arcade

from .color import Color, ColorProp

AnchorX = Literal['left', 'center', 'right']
AnchorY = Literal['bottom', 'center', 'top']


@dataclass
class Font:
    """A simple wrapper around arcade's font handling."""

    name: str = 'Arial'
    size: int = 12
    color: ColorProp = 'black'
    bold: bool = False
    italic: bool = False

    def __post_init__(self) -> None:
        self.color = Color(self.color)

    def instance_text(
        self,
        text: str,
        x: float = 0.0,
        y: float = 0.0,
        anchor_x: AnchorX = 'left',
        anchor_y: AnchorY = 'bottom',
    ) -> arcade.Text:
        """Create a text label at the given position using this font."""
        return arcade.Text(
            text=text,
            x=x,
            y=y,
            color=self.color.as_tuple(),
            font_size=self.size,
            font_name=self.name,
            bold=self.bold,
            italic=self.italic,
            anchor_x=anchor_x,
            anchor_y=anchor_y,
        )

    def copy(
        self,
        name: str | None = None,
        size: int | None = None,
        color: ColorProp | None = None,
        bold: bool | None = None,
        italic: bool | None = None,
    ) -> 'Font':
        """Return a new Font with the given overrides."""
        return Font(
            name=name if name is not None else self.name,
            size=size if size is not None else self.size,
            color=color if color is not None else self.color.as_tuple(),
            bold=bold if bold is not None else self.bold,
            italic=italic if italic is not None else self.italic,
        )
