from typing import List, Dict, Any

import graphics as gr

from colors import Color
from mouse import Mouse, NothingMouse, ColoringMouse, RotatingMouse
from save_load import get_save_load_version
from spatial import Interval, Box, Position, Turn, Corner


QUILT_COLUMNS = 12
QUILT_ROWS = 11
QUILT_BLOCK_PIXELS = 50
QUILT_START_COLOR = Color("white")
QUILT_SEAM_COLOR = Color("dark grey")


class QuiltTriangle:

    def __init__(self, enclosure: Box, right_angle: Corner) -> None:
        self.enclosure = enclosure
        self.right_angle = right_angle
        self.fabric_color = QUILT_START_COLOR
        self.seam_color = QUILT_SEAM_COLOR
        self.polygon = self.create_polygon()
        self.my_window: gr.GraphWin | None = None

    def create_polygon(self) -> gr.Polygon:
        polygon = gr.Polygon(self.compute_points())
        polygon.setFill(self.fabric_color)
        polygon.setOutline(self.seam_color)
        return polygon

    def compute_points(self) -> List[gr.Point]:
        vertices = [self.clockwise_vertex, self.right_angle_vertex,
                    self.counterclockwise_vertex]
        return [vertex.as_point() for vertex in vertices]

    @property
    def right_angle_vertex(self) -> Position:
        return self.enclosure.corner(self.right_angle)

    @property
    def clockwise_vertex(self) -> Position:
        corner = self.right_angle.next_corner(Turn.CW)
        return self.enclosure.corner(corner)

    @property
    def counterclockwise_vertex(self) -> Position:
        corner = self.right_angle.next_corner(Turn.CCW)
        return self.enclosure.corner(corner)

    @property
    def excluded_vertex(self) -> Position:
        clockwise_corner = self.right_angle.next_corner(Turn.CW)
        corner = clockwise_corner.next_corner(Turn.CW)
        return self.enclosure.corner(corner)

    def draw_to(self, window: gr.GraphWin) -> None:
        assert self.my_window is None
        self.polygon.draw(window)
        self.my_window = window

    def undraw(self) -> None:
        assert self.my_window is not None
        self.polygon.undraw()
        self.my_window = None

    def rotate(self, turn: Turn) -> None:
        window = self.my_window
        self.undraw()
        self.right_angle = self.right_angle.next_corner(turn)
        self.polygon = self.create_polygon()
        if window is not None:
            self.draw_to(window)

    def color(self, color: Color, click: Position) -> None:
        my_distance = click.distance_to(self.right_angle_vertex)
        other_distance = click.distance_to(self.excluded_vertex)
        if my_distance < other_distance:
            self.fabric_color = color
            self.polygon.setFill(self.fabric_color)

    def region_clicked_by(self, click: Position) -> bool:
        return self.enclosure.contains(click)

    def polygon_clicked_by(self, click: Position) -> bool:
        return (self.region_clicked_by(click)
                and self.is_nearer_triangle(click))

    def is_nearer_triangle(self, point: Position) -> bool:
        my_distance = point.distance_to(self.right_angle_vertex)
        other_distance = point.distance_to(self.excluded_vertex)
        return my_distance < other_distance

    def save_json(self) -> Dict[str, Any]:
        return {
            "class": "QuiltTriangle",
            "right_angle": self.right_angle.name,
            "fabric_color": str(self.fabric_color),
        }

    def load_json(self, data: Dict[str, Any]) -> None:
        assert data["class"] == "QuiltTriangle"
        self.right_angle = Corner.__members__[data["right_angle"]]
        self.fabric_color = Color(data["fabric_color"])
        window = self.my_window
        self.undraw()
        self.polygon = self.create_polygon()
        if window is not None:
            self.draw_to(window)


class QuiltBlock:

    def __init__(self, top_left: Position, side_length: int | float) -> None:
        self.box = self.compute_box(top_left, side_length)
        self.triangles = self.generate_triangles()
        self.my_window: gr.GraphWin | None = None

    def compute_box(self,
                    top_left: Position,
                    side_length: int | float) -> Box:
        x_range = Interval(top_left.x, top_left.x + side_length)
        y_range = Interval(top_left.y, top_left.y + side_length)
        return Box(x_range, y_range)

    def generate_triangles(self) -> List[QuiltTriangle]:
        return [QuiltTriangle(self.box, Corner.TOP_RIGHT),
                QuiltTriangle(self.box, Corner.BOTTOM_LEFT)]

    def draw_to(self, window: gr.GraphWin) -> None:
        self.my_window = window
        for triangle in self.triangles:
            triangle.draw_to(window)

    def clicked_by(self, mouse: Mouse) -> bool:
        return self.box.contains(mouse.click)

    def react_to(self, mouse: Mouse) -> None:
        for triangle in self.triangles:
            self.apply_mouse(mouse, triangle)

    def apply_mouse(self, mouse: Mouse, triangle: QuiltTriangle) -> None:
        if isinstance(mouse.setting, NothingMouse):
            pass
        elif isinstance(mouse.setting, ColoringMouse):
            if triangle.polygon_clicked_by(mouse.click):
                triangle.color(mouse.setting.color, mouse.click)
        elif isinstance(mouse.setting, RotatingMouse):
            if triangle.region_clicked_by(mouse.click):
                triangle.rotate(mouse.setting.turn)
        else:
            assert False

    def save_json(self) -> Dict[str, Any]:
        return {
            "class": "QuiltBlock",
            "triangles": [triangle.save_json()
                          for triangle in self.triangles],
        }

    def load_json(self, data: Dict[str, Any]) -> None:
        assert data["class"] == "QuiltBlock"
        for triangle_data, triangle in zip(data["triangles"], self.triangles):
            triangle.load_json(triangle_data)


class Quilt:

    def __init__(self, top_left: Position) -> None:
        self.rows, self.columns = QUILT_ROWS, QUILT_COLUMNS
        self.block_pixels = QUILT_BLOCK_PIXELS
        self.box = self.compute_box(top_left)
        self.blocks = self.generate_blocks()

    def compute_box(self, top_left: Position) -> Box:
        width = self.columns * self.block_pixels
        height = self.rows * self.block_pixels
        x_range = Interval(top_left.x, top_left.x + width)
        y_range = Interval(top_left.y, top_left.y + height)
        return Box(x_range, y_range)

    def generate_blocks(self) -> List[QuiltBlock]:
        return [self.create_block_at(row, column)
                for row in range(self.rows)
                for column in range(self.columns)]

    def create_block_at(self, row: int, column: int) -> QuiltBlock:
        position = self.compute_block_position(row, column)
        return QuiltBlock(position, self.block_pixels)

    def compute_block_position(self, row: int, column: int) -> Position:
        assert 0 <= row < self.rows
        assert 0 <= column < self.columns
        x = self.box.x_min + column * self.block_pixels
        y = self.box.y_min + row * self.block_pixels
        return Position(x, y)

    def draw_to(self, window: gr.GraphWin) -> None:
        for block in self.blocks:
            block.draw_to(window)

    def clicked_by(self, mouse: Mouse) -> bool:
        return self.box.contains(mouse.click)

    def react_to(self, mouse: Mouse) -> None:
        for block in self.blocks:
            if block.clicked_by(mouse):
                block.react_to(mouse)

    def save_json(self) -> Dict[str, Any]:
        return {
            "version": get_save_load_version(),
            "class": "Quilt",
            "blocks": [block.save_json() for block in self.blocks],
        }

    def load_json(self, data: Dict[str, Any]) -> None:
        assert data["version"] == get_save_load_version()
        assert data["class"] == "Quilt"
        for block_data, block in zip(data["blocks"], self.blocks):
            block.load_json(block_data)
