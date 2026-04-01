from colors import Color
from spatial import Turn, Position


class MouseSetting:
    pass


class NothingMouse(MouseSetting):
    pass


class RotatingMouse(MouseSetting):
    def __init__(self, turn: Turn) -> None:
        self.turn = turn


class ColoringMouse(MouseSetting):
    def __init__(self, color: Color) -> None:
        self.color = color


class Mouse:

    def __init__(self, click: Position, setting: MouseSetting) -> None:
        self.click = click
        self.setting = setting

    def update_setting(self, new_setting: MouseSetting) -> None:
        self.setting = new_setting
