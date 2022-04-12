from enum import Enum


class Colors(Enum):
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    BLACK = (0, 0, 0)


class Forms(Enum):
    CIRCLE = 0
    SQUARE = 1


class Directions(Enum):
    RIGHT = (1, 0)
    UP = (0, -1)
    LEFT = (-1, 0)
    DOWN = (0, 1)


class FoodTypes(Enum):
    NONE = 0
    APPLE = 1
