from typing import Tuple

import graphics as gr

from colors import Color
from controls import Controls
from mouse import Mouse, NothingMouse
from quilt import Quilt
from spatial import Position


WINDOW_TITLE = "Quilt Planner"
WINDOW_BACKGROUND = Color("AntiqueWhite2")
WINDOW_BORDER = 20


class Interface:

    def __init__(self) -> None:
        self.controls, self.quilt = self.create_graphics()
        self.controls.set_quilt_ref(self.quilt)
        self.window = self.create_window()
        self.draw_graphics()

    def create_graphics(self) -> Tuple[Controls, Quilt]:
        controls = Controls(Position(WINDOW_BORDER, WINDOW_BORDER))
        quilt = Quilt(Position(controls.box.x_max + WINDOW_BORDER,
                               WINDOW_BORDER))
        return controls, quilt

    def create_window(self) -> gr.GraphWin:
        width = (3 * WINDOW_BORDER
                 + self.controls.box.width
                 + self.quilt.box.width)
        height = (2 * WINDOW_BORDER
                  + max(self.controls.box.height,
                        self.quilt.box.height))
        window = gr.GraphWin(WINDOW_TITLE, round(width), round(height))
        window.setBackground(WINDOW_BACKGROUND)
        return window

    def draw_graphics(self) -> None:
        self.controls.draw_to(self.window)
        self.quilt.draw_to(self.window)

    def run_click_loop(self) -> None:
        while self.continue_loop():
            self.process_click()

    def continue_loop(self) -> bool:
        return not self.controls.has_been_quit()

    def process_click(self) -> None:
        mouse = self.get_mouse()
        '''
        if self.controls.clicked_by(mouse):
            self.controls.react_to(mouse)
            mouse.update_setting(self.controls.mouse_setting())
        '''
        self.controls.react_to(mouse)
        mouse.update_setting(self.controls.mouse_setting())
        if self.quilt.clicked_by(mouse):
            self.quilt.react_to(mouse)

    def get_mouse(self) -> Mouse:
        clicked_position = Position.from_point(self.window.getMouse())
        return Mouse(clicked_position, NothingMouse())

    def finish(self) -> None:
        self.window.close()
