from typing import TYPE_CHECKING

import arcade

from .color import Color, ColorProp

if TYPE_CHECKING:
    pass


def parse_xywh_to_lbrt(
    x: float, y: float, w: float, h: float
) -> tuple[float, float, float, float]:
    left = x
    bottom = y
    right = x + w
    top = y + h
    return left, bottom, right, top


class Draw:
    @staticmethod
    def filled_rect(
        xywh: tuple[float, float, float, float],
        color: Color,
    ) -> None:
        x, y, w, h = xywh
        arcade.draw_lbwh_rectangle_filled(
            left=x,
            bottom=y,
            width=w,
            height=h,
            color=color.as_tuple(),
        )

    @staticmethod
    def filled_rounded_rect(
        xywh: tuple[float, float, float, float],
        color: Color | ColorProp,
        radius: tuple[float, float, float, float] = (0, 0, 0, 0),
    ) -> None:
        x, y, w, h = xywh
        tl, tr, br, bl = radius
        col = color.as_tuple() if color else (0, 0, 0, 0)

        # Center vertical rect
        arcade.draw_lbwh_rectangle_filled(
            x + max(tl, bl),
            y,
            w - max(tl, bl) - max(tr, br),
            h,
            col,
        )

        # Center horizontal rect
        arcade.draw_lbwh_rectangle_filled(
            x,
            y + max(bl, br),
            w,
            h - max(tl, tr) - max(bl, br),
            col,
        )

        Draw._corner(x + tl, y + h - tl, tl, 90, 180, col)
        Draw._corner(x + w - tr, y + h - tr, tr, 0, 90, col)
        Draw._corner(x + w - br, y + br, br, 270, 360, col)
        Draw._corner(x + bl, y + bl, bl, 180, 270, col)

    @staticmethod
    def _corner(
        cx: float,
        cy: float,
        radius: float,
        start: float,
        end: float,
        color: tuple,
    ):
        if radius <= 0:
            return

        arcade.draw_arc_filled(
            center_x=cx,
            center_y=cy,
            width=radius * 2,
            height=radius * 2,
            color=color,
            start_angle=start,
            end_angle=end,
        )

    @staticmethod
    def outline_rounded_rect(
        xywh: tuple[float, float, float, float],
        color: Color | ColorProp,
        radius: tuple[float, float, float, float] = (0, 0, 0, 0),
        border_width: float = 1,
    ) -> None:
        x, y, w, h = xywh
        tl, tr, br, bl = radius

        c = color if isinstance(color, Color) else Color(color)
        col = c.as_tuple()

        # Top
        arcade.draw_line(
            x + tl,
            y + h,
            x + w - tr,
            y + h,
            col,
            border_width,
        )

        # Bottom
        arcade.draw_line(
            x + bl,
            y,
            x + w - br,
            y,
            col,
            border_width,
        )

        # Left
        arcade.draw_line(
            x,
            y + bl,
            x,
            y + h - tl,
            col,
            border_width,
        )

        # Right
        arcade.draw_line(
            x + w,
            y + br,
            x + w,
            y + h - tr,
            col,
            border_width,
        )

        Draw._corner_outline(
            x + tl,
            y + h - tl,
            tl,
            90,
            180,
            col,
            border_width * 2,
        )

        Draw._corner_outline(
            x + w - tr,
            y + h - tr,
            tr,
            0,
            90,
            col,
            border_width * 2,
        )

        Draw._corner_outline(
            x + w - br,
            y + br,
            br,
            270,
            360,
            col,
            border_width * 2,
        )

        Draw._corner_outline(
            x + bl,
            y + bl,
            bl,
            180,
            270,
            col,
            border_width * 2,
        )

    @staticmethod
    def _corner_outline(
        cx: float,
        cy: float,
        radius: float,
        start: float,
        end: float,
        color: tuple,
        border_width: float,
    ):
        if radius <= 0:
            return

        arcade.draw_arc_outline(
            center_x=cx,
            center_y=cy,
            width=radius * 2,
            height=radius * 2,
            color=color,
            start_angle=start,
            end_angle=end,
            border_width=border_width,
        )
