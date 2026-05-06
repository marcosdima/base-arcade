from typing import TYPE_CHECKING, Literal

from ...core import Event
from ...input import MouseButton
from ..geometry import Point

if TYPE_CHECKING:
    from . import UIElement


type MouseOverEvent = tuple[float, float]
EventName = Literal[
    'on_mouse_over',
    'on_mouse_in',
    'on_mouse_out',
    'on_mouse_press',
    'on_mouse_release',
    'on_mouse_scroll',
]

EVENT_PRIORITY = 5


class UIEvents:
    def __init__(self, owner: 'UIElement'):
        # Instance of the event system for this UI element.
        self.on_mouse_over = Event[Point, Point]()
        self.on_mouse_in = Event[Point]()
        self.on_mouse_out = Event[Point]()
        self.on_mouse_press = Event[Point, MouseButton, set]()
        self.on_mouse_release = Event[Point, MouseButton, set]()
        self.on_mouse_scroll = Event[Point, int, int]()

        # Set the owner of the events for debugging and context.
        self.owner = owner

        self.on_mouse_over.subscribe(self.owner._on_mouse_over, EVENT_PRIORITY)
        self.on_mouse_in.subscribe(self.owner._on_mouse_in, EVENT_PRIORITY)
        self.on_mouse_out.subscribe(self.owner._on_mouse_out, EVENT_PRIORITY)
        self.on_mouse_press.subscribe(self.owner._on_mouse_press, EVENT_PRIORITY)
        self.on_mouse_release.subscribe(self.owner._on_mouse_release, EVENT_PRIORITY)
        self.on_mouse_scroll.subscribe(self.owner._on_mouse_scroll, EVENT_PRIORITY)

        # Set up debug listeners if debugging is enabled.
        if self.owner.debug.enabled:
            self.on_mouse_over.subscribe(
                lambda p, dp: self.owner.debug.print(
                    'Event', f'on_mouse_over(p={p}, dp={dp})'
                )
            )
            self.on_mouse_in.subscribe(
                lambda p: self.owner.debug.print('Event', f'on_mouse_in(p={p})')
            )
            self.on_mouse_out.subscribe(
                lambda p: self.owner.debug.print('Event', f'on_mouse_out(p={p})')
            )
            self.on_mouse_press.subscribe(
                lambda p, button, modifiers: self.owner.debug.print(
                    'Event',
                    f'on_mouse_press(p={p}, button={button}, modifiers={modifiers})',
                )
            )
            self.on_mouse_release.subscribe(
                lambda p, button, modifiers: self.owner.debug.print(
                    'Event',
                    f'on_mouse_release(p={p}, button={button}, modifiers={modifiers})',
                )
            )
            self.on_mouse_scroll.subscribe(
                lambda p, scroll_x, scroll_y: self.owner.debug.print(
                    'Event',
                    f'on_mouse_scroll(p={p}, scroll_x={scroll_x}, scroll_y={scroll_y})',
                )
            )

    def trigger(self, event: EventName, *args, **kwargs):
        if event == 'on_mouse_over':
            return self.on_mouse_over.trigger(*args, **kwargs)
        elif event == 'on_mouse_in':
            return self.on_mouse_in.trigger(*args, **kwargs)
        elif event == 'on_mouse_out':
            return self.on_mouse_out.trigger(*args, **kwargs)
        elif event == 'on_mouse_press':
            return self.on_mouse_press.trigger(*args, **kwargs)
        elif event == 'on_mouse_release':
            return self.on_mouse_release.trigger(*args, **kwargs)
        elif event == 'on_mouse_scroll':
            return self.on_mouse_scroll.trigger(*args, **kwargs)
        else:
            raise ValueError(f'Unknown event type: {event}')


"""        # Set up owner events listeners.
        """
