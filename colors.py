from typing import NewType, List


Color = NewType('Color', str)


AVAILABLE_COLORS: List[str] = [
    "white",
    "light gray",
    "black",
    "red",
    "orange",
    "lemon chiffon",
    "forest green",
    "LightSkyBlue1",
    "purple1",
]


def get_colors() -> List[Color]:
    return list(map(Color, AVAILABLE_COLORS))
