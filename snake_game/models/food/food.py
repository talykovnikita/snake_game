from abc import ABC
from dataclasses import dataclass
from typing import Tuple
from snake_game.utils.enums import FoodTypes


@dataclass()
class Food(ABC):
    position: Tuple[int, int]
    type: FoodTypes

    @classmethod
    def create(cls, position: Tuple[int, int]):
        return cls(position=position, type=cls.type)

    def __repr__(self):
        return f"Food {self.type}\n" f"{self.position}"
