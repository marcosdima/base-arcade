from typing import TYPE_CHECKING

import arcade
from arcade import Rect as ArcadeRect

from ..ui.geometry import Rect
from .color import Color

if TYPE_CHECKING:
    from ..ui.style import Style

type border_type = float | tuple[float, float] | tuple[float, float, float, float]


class Draw:
    @staticmethod
    def draw_rect(
        rect: Rect | ArcadeRect,
        style: 'Style',
    ) -> None:
        """
        Draw a rectangle with optional background color and border.

        Args:
            rect: Rectangle to draw (Rect or arcade.Rect)
            style: UI style data source for background and border
        """
        if rect is None or style is None:
            return

        # Convert to arcade.Rect if needed
        arcade_rect = rect.as_arcade_rect() if isinstance(rect, Rect) else rect

        has_background = style.is_set('background_color')
        border_widths = style.border.get_tuple()
        has_border = any(value > 0 for value in border_widths)

        if not has_background and not has_border:
            return

        color = style.background_color if has_background else Color('transparent')
        color_tuple = color.as_tuple()

        border_color = style.border.color if style.border.is_set('color') else color
        border_color_tuple = border_color.as_tuple()

        tl, tr, br, bl = style.border.get_radius_tuple()
        width = max(border_widths)

        x = arcade_rect.left
        y = arcade_rect.bottom
        w = arcade_rect.width
        h = arcade_rect.height

        # Clamp radii so corners fit within the rectangle.
        max_radius = min(w, h) / 2
        tl = max(0, min(tl, max_radius))
        tr = max(0, min(tr, max_radius))
        br = max(0, min(br, max_radius))
        bl = max(0, min(bl, max_radius))
        radius = max(tl, tr, br, bl)

        # Draw background
        if has_background and radius > 0:
            # Draw main rectangle body
            arcade.draw_lbwh_rectangle_filled(
                x + radius, y, w - 2 * radius, h, color_tuple
            )
            arcade.draw_lbwh_rectangle_filled(
                x, y + radius, w, h - 2 * radius, color_tuple
            )

            # Draw corner arcs
            arc_specs = Draw._arc_specs(x, y, w, h, tl, tr, br, bl)
            for radius_val, cx, cy, start_angle, end_angle in arc_specs:
                if radius_val > 0:
                    arcade.draw_arc_filled(
                        center_x=cx,
                        center_y=cy,
                        width=2 * radius_val,
                        height=2 * radius_val,
                        color=color_tuple,
                        start_angle=start_angle,
                        end_angle=end_angle,
                    )
        elif has_background:
            arcade.draw_rect_filled(arcade_rect, color_tuple)

        # Draw border
        if has_border and width > 0:
            if radius > 0:
                # Draw border arcs
                arc_specs = Draw._arc_specs(x, y, w, h, tl, tr, br, bl)
                for radius_val, cx, cy, start_angle, end_angle in arc_specs:
                    if radius_val > 0:
                        arcade.draw_arc_outline(
                            center_x=cx,
                            center_y=cy,
                            width=2 * radius_val,
                            height=2 * radius_val,
                            color=border_color_tuple,
                            start_angle=start_angle,
                            end_angle=end_angle,
                            border_width=width,
                        )

                # Draw border lines for straight sides
                arcade.draw_line(
                    start_x=x + tl,
                    start_y=y,
                    end_x=x + w - tr,
                    end_y=y,
                    color=border_color_tuple,
                    line_width=width,
                )  # Bottom
                arcade.draw_line(
                    start_x=x + tr,
                    start_y=y + h,
                    end_x=x + w - bl,
                    end_y=y + h,
                    color=border_color_tuple,
                    line_width=width,
                )  # Top
                arcade.draw_line(
                    start_x=x,
                    start_y=y + bl,
                    end_x=x,
                    end_y=y + h - tl,
                    color=border_color_tuple,
                    line_width=width,
                )  # Left
                arcade.draw_line(
                    start_x=x + w,
                    start_y=y + br,
                    end_x=x + w,
                    end_y=y + h - tr,
                    color=border_color_tuple,
                    line_width=width,
                )  # Right
            else:
                arcade.draw_lbwh_rectangle_outline(
                    left=x,
                    bottom=y,
                    width=w,
                    height=h,
                    color=border_color_tuple,
                    border_width=width,
                )

    @staticmethod
    def _arc_specs(
        x: float,
        y: float,
        w: float,
        h: float,
        tl: float,
        tr: float,
        br: float,
        bl: float,
    ) -> tuple[tuple[float, float, float, float, float], ...]:
        """
        Return arc metadata per corner in TL, TR, BR, BL order.
        Each item is: (radius, cx, cy, start_angle, end_angle).
        """
        return (
            (tl, x + tl, y + h - tl, 90, 180),
            (tr, x + w - tr, y + h - tr, 0, 90),
            (br, x + w - br, y + br, 270, 360),
            (bl, x + bl, y + bl, 180, 270),
        )
