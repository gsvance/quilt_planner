from typing import List, Tuple

import graphics as gr

from buttons import TextButton, ColorButton, RotateButton
from colors import get_colors, Color
from mouse import (Mouse, MouseSetting, NothingMouse, ColoringMouse,
                   RotatingMouse)
from quilt import Quilt
from save_load import save_quilt_data, load_quilt_data
from spatial import Interval, Box, Position, Turn


BUTTON_SPACING = 10
SECTION_SPACING = 2 * BUTTON_SPACING

SMALL_BUTTON_WIDTH = 35
MEDIUM_BUTTON_WIDTH = 60
LARGE_BUTTON_WIDTH = 2 * MEDIUM_BUTTON_WIDTH + BUTTON_SPACING

BUTTON_HEIGHT = SMALL_BUTTON_WIDTH

PANEL_WIDTH = 2 * BUTTON_SPACING + LARGE_BUTTON_WIDTH
PANEL_TOP_HEIGHT = BUTTON_SPACING + 2 * SECTION_SPACING + 2 * BUTTON_HEIGHT


class Controls:

    def __init__(self, top_left: Position) -> None:
        self.box = self.compute_box(top_left)
        self.frame = self.create_frame()
        self.quit_button = self.make_quit_button()
        self.save_button, self.load_button = self.make_save_load_buttons()
        self.color_buttons = self.make_color_buttons()
        self.rotate_buttons = self.make_rotate_buttons()
        self.quit_flag = False
        self.setting = NothingMouse()
        self.quilt_ref: Quilt | None = None

    def compute_box(self, top_left: Position) -> Box:
        small_button_rows = max(len(get_colors()), len(Turn))
        row_height = BUTTON_HEIGHT + BUTTON_SPACING
        panel_height = PANEL_TOP_HEIGHT + row_height * small_button_rows
        y_range = Interval(top_left.y, top_left.y + panel_height)
        x_range = Interval(top_left.x, top_left.x + PANEL_WIDTH)
        return Box(x_range, y_range)

    def create_frame(self) -> gr.Rectangle:
        frame = gr.Rectangle(*self.box.as_points())
        frame.setFill('')
        frame.setOutline('dark gray')
        return frame

    def make_quit_button(self) -> TextButton:
        x_range = Interval(self.box.x_min + BUTTON_SPACING,
                           self.box.x_max - BUTTON_SPACING)
        y_min = self.box.y_min + BUTTON_SPACING
        y_range = Interval(y_min, y_min + BUTTON_HEIGHT)
        button = TextButton(Box(x_range, y_range), "Quit")
        button.set_fill(Color("firebrick3"))
        return button

    def make_save_load_buttons(self) -> Tuple[TextButton, TextButton]:
        y_min = self.quit_button.box.y_max + SECTION_SPACING
        y_range = Interval(y_min, y_min + BUTTON_HEIGHT)
        save_x_min = self.box.x_min + BUTTON_SPACING
        save_x_range = Interval(save_x_min, save_x_min + MEDIUM_BUTTON_WIDTH)
        load_x_max = self.box.x_max - BUTTON_SPACING
        load_x_range = Interval(load_x_max - MEDIUM_BUTTON_WIDTH, load_x_max)
        save_button = TextButton(Box(save_x_range, y_range), "Save")
        load_button = TextButton(Box(load_x_range, y_range), "Load")
        save_button.set_fill(Color("SlateBlue2"))
        load_button.set_fill(Color("green3"))
        return save_button, load_button

    def make_color_buttons(self) -> List[ColorButton]:
        x_min = self.save_button.box.x_mid - SMALL_BUTTON_WIDTH / 2
        x_range = Interval(x_min, x_min + SMALL_BUTTON_WIDTH)
        first_y_min = self.save_button.box.y_max + SECTION_SPACING
        delta_y = BUTTON_HEIGHT + BUTTON_SPACING
        buttons = list()
        for i, color_i in enumerate(get_colors()):
            y_min_i = first_y_min + i * delta_y
            y_range_i = Interval(y_min_i, y_min_i + BUTTON_HEIGHT)
            button_i = ColorButton(Box(x_range, y_range_i), color_i)
            buttons.append(button_i)
        return buttons

    def make_rotate_buttons(self) -> List[RotateButton]:
        x_min = self.load_button.box.x_mid - SMALL_BUTTON_WIDTH / 2
        x_range = Interval(x_min, x_min + SMALL_BUTTON_WIDTH)
        first_y_min = self.load_button.box.y_max + SECTION_SPACING
        delta_y = BUTTON_HEIGHT + BUTTON_SPACING
        buttons = list()
        for i, turn_i in enumerate(Turn):
            y_min_i = first_y_min + i * delta_y
            y_range_i = Interval(y_min_i, y_min_i + BUTTON_HEIGHT)
            button_i = RotateButton(Box(x_range, y_range_i), turn_i)
            buttons.append(button_i)
        return buttons

    def has_been_quit(self) -> bool:
        return self.quit_flag

    def set_quilt_ref(self, quilt: Quilt | None) -> None:
        self.quilt_ref = quilt

    def draw_to(self, window: gr.GraphWin) -> None:
        self.frame.draw(window)
        self.quit_button.draw_to(window)
        self.save_button.draw_to(window)
        self.load_button.draw_to(window)
        for button in self.color_buttons:
            button.draw_to(window)
        for button in self.rotate_buttons:
            button.draw_to(window)

    def clicked_by(self, mouse: Mouse) -> bool:
        return self.box.contains(mouse.click)

    def react_to(self, mouse: Mouse) -> None:
        if self.quit_button.clicked(mouse.click):
            self.quit_flag = True
        if self.save_button.clicked(mouse.click):
            assert self.quilt_ref is not None
            name = "test_quilt"
            data = self.quilt_ref.save_json()
            save_quilt_data(data, name)
        if self.load_button.clicked(mouse.click):
            assert self.quilt_ref is not None
            name = "test_quilt"
            data = load_quilt_data(name)
            self.quilt_ref.load_json(data)
        for button in self.color_buttons:
            if button.clicked(mouse.click):
                self.setting = ColoringMouse(button.color)
        for button in self.rotate_buttons:
            if button.clicked(mouse.click):
                self.setting = RotatingMouse(button.turn)

    def mouse_setting(self) -> MouseSetting:
        return self.setting
