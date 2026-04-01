import graphics as gr

from colors import Color
from spatial import Box, Position, Turn


class Button:

    def __init__(self, box: Box) -> None:
        self.box = box
        self.prepare_graphics()

    @property
    def center(self) -> Position:
        return self.box.center

    def prepare_graphics(self) -> None:
        self.rectangle = gr.Rectangle(*self.box.as_points())
        self.rectangle.setOutline("dark grey")
        self.rectangle.setFill("dark gray")
        self.decorations = list()

    def decorate(self, graphic: gr.GraphicsObject):
        self.decorations.append(graphic)

    def draw_to(self, window: gr.GraphWin) -> None:
        self.rectangle.draw(window)
        for decoration in self.decorations:
            decoration.draw(window)

    def clicked(self, click: Position) -> bool:
        return self.box.contains(click)


class TextButton(Button):

    def __init__(self, box: Box, label: str) -> None:
        super().__init__(box)
        self.label = label
        self.text = gr.Text(self.center.as_point(), label)
        self.text.setTextColor("white")
        self.decorate(self.text)
        self.rectangle.setOutline("white")

    def set_fill(self, color: Color) -> None:
        self.rectangle.setFill(color)


class ColorButton(Button):

    def __init__(self, box: Box, color: Color) -> None:
        super().__init__(box)
        self.color = color
        self.rectangle.setFill(color)


class RotateButton(Button):

    def __init__(self, box: Box, turn: Turn) -> None:
        super().__init__(box)
        self.turn = turn
        self.text = gr.Text(self.center.as_point(), self.turn.name)
        self.text.setTextColor("white")
        self.text.setSize(8)
        self.decorate(self.text)
        self.rectangle.setOutline("white")
