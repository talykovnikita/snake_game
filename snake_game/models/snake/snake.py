from typing import Tuple
from snake_game.models.food.food import Food


class Snake:
    def __init__(self, head_start_pos: Tuple[int, int]):
        self.body = []
        self.body.append(head_start_pos)

    def eat_food(self, food: Food):
        self.body.insert(0, food.position)

    def __repr__(self):
        return str(self.body)
