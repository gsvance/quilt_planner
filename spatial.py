import enum
import math
from typing import TypeVar, Tuple

import graphics as gr


P = TypeVar('P', bound='Position')


@enum.unique
class Turn(enum.Enum):
    CCW = -1
    CW = +1


@enum.unique
class Corner(enum.Enum):
    TOP_LEFT = 0
    TOP_RIGHT = 1
    BOTTOM_RIGHT = 2
    BOTTOM_LEFT = 3

    def next_corner(self, turn: Turn) -> 'Corner':
        return Corner((self.value + turn.value) % len(Corner))


class Position:

    __slots__ = ('_x', '_y')

    def __init__(self, x: int | float, y: int | float) -> None:
        self._x = x
        self._y = y

    @classmethod
    def from_point(cls: type[P], point: gr.Point) -> P:
        return cls(point.getX(), point.getY())

    def as_point(self) -> gr.Point:
        return gr.Point(self._x, self._y)

    @property
    def x(self) -> int | float:
        return self._x

    @property
    def y(self) -> int | float:
        return self._y

    def distance_to(self, position: 'Position') -> float:
        x_difference = self.x - position.x
        y_difference = self.y - position.y
        return math.hypot(x_difference, y_difference)


class Interval:

    __slots__ = ('_lower', '_upper')

    def __init__(self, lower: int | float, upper: int | float) -> None:
        assert lower < upper
        self._lower = lower
        self._upper = upper

    @property
    def lower(self) -> int | float:
        return self._lower

    @property
    def upper(self) -> int | float:
        return self._upper

    @property
    def length(self) -> int | float:
        return self._upper - self._lower

    @property
    def midpoint(self) -> float:
        return self._lower + 0.5 * self.length

    def contains(self, value: int | float) -> bool:
        return self._lower < value < self._upper


class Box:

    __slots__ = ('_x_interval', '_y_interval')

    def __init__(self, x_interval: Interval, y_interval: Interval) -> None:
        self._x_interval = x_interval
        self._y_interval = y_interval

    def as_points(self) -> Tuple[gr.Point, gr.Point]:
        top_left = gr.Point(self.x_min, self.y_min)
        bottom_right = gr.Point(self.x_max, self.y_max)
        return top_left, bottom_right

    @property
    def x_interval(self) -> Interval:
        return self._x_interval

    @property
    def y_interval(self) -> Interval:
        return self._y_interval

    @property
    def x_min(self) -> int | float:
        return self._x_interval.lower

    @property
    def x_mid(self) -> float:
        return self._x_interval.midpoint

    @property
    def x_max(self) -> int | float:
        return self._x_interval.upper

    @property
    def y_min(self) -> int | float:
        return self._y_interval.lower

    @property
    def y_mid(self) -> float:
        return self._y_interval.midpoint

    @property
    def y_max(self) -> int | float:
        return self._y_interval.upper

    @property
    def width(self) -> int | float:
        return self._x_interval.length

    @property
    def height(self) -> int | float:
        return self._y_interval.length

    @property
    def center(self) -> Position:
        return Position(self._x_interval.midpoint, self._y_interval.midpoint)

    def contains(self, position: Position) -> bool:
        return (self._x_interval.contains(position.x)
                and self._y_interval.contains(position.y))

    def corner(self, corner: Corner) -> Position:
        if corner is Corner.TOP_LEFT:
            return Position(self.x_min, self.y_min)
        elif corner is Corner.TOP_RIGHT:
            return Position(self.x_max, self.y_min)
        elif corner is Corner.BOTTOM_RIGHT:
            return Position(self.x_max, self.y_max)
        elif corner is Corner.BOTTOM_LEFT:
            return Position(self.x_min, self.y_max)
        else:
            assert False
