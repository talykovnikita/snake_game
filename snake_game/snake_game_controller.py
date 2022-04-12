from snake_game import app_logger

import logging
from typing import List, Tuple
from snake_game.models.food.food import Food
from snake_game.models.food.apple import Apple
from snake_game.models.snake.snake import Snake
from snake_game.utils.enums import Directions
from random import randint

logger = app_logger.get_logger(__name__, level=logging.DEBUG)


class SnakeGameController:
    is_game_over: bool = False
    record: int = 0

    def __init__(
        self,
        field_size: Tuple[int, int],
        head_start_pos: Tuple[int, int],
        pixel_size: Tuple[int, int],
    ):
        self.field_size = field_size
        self.snake: Snake = Snake(head_start_pos=head_start_pos)
        self._current_snake_direction = Directions.UP
        self.food: List[Food] = []
        self.pixel_size = pixel_size
        self.is_food_spawn = False

        logger.debug(self)

    def __repr__(self):
        return (
            f"Game is created:\n"
            f"{self.field_size=}\n"
            f"{self.snake=}\n"
            f"{self._current_snake_direction=}\n"
            f"{self.food=}\n"
            f"{self.pixel_size=}\n"
            f"{self.is_food_spawn=}\n"
        )

    @property
    def current_snake_direction(self):
        return self._current_snake_direction

    @current_snake_direction.setter
    def current_snake_direction(self, new_direction):
        if new_direction not in Directions:
            logger.debug(f"Invalid was skipped direction: {new_direction}")
            return
        if (
            new_direction.value[0] + self._current_snake_direction.value[0] == 0
            and new_direction.value[1] + self._current_snake_direction.value[1] == 0
        ):
            logger.debug(
                f"Impossible change direction to opposite one: {new_direction}"
            )
            return

        logger.debug(f"Old direction was: {self._current_snake_direction}")
        self._current_snake_direction = new_direction
        logger.debug(f"New direction was set: {self._current_snake_direction}")

    def _rect_pos_to_circle_pos(self, position: Tuple[int, int]) -> Tuple[int, int]:
        return (
            position[0] + self.pixel_size[0] // 2,
            position[1] + self.pixel_size[1] // 2,
        )

    def _circle_pos_to_rect_pos(self, position: Tuple[int, int]) -> Tuple[int, int]:
        return (
            position[0] - self.pixel_size[0] // 2,
            position[1] - self.pixel_size[1] // 2,
        )

    def _spawn_food(self):
        rand_x = randint(0, self.field_size[0])
        rand_y = randint(0, self.field_size[1])
        rect_new_x = rand_x - rand_x % self.pixel_size[0]
        rect_new_y = rand_y - rand_y % self.pixel_size[1]

        new_food = Apple.create(
            position=self._rect_pos_to_circle_pos(position=(rect_new_x, rect_new_y))
        )
        self.food.append(new_food)
        self.is_food_spawn = True
        logger.debug(
            f"New {new_food.type.name} at {new_food.position[0], new_food.position[1]} was spawned"
        )

    def _calc_new_snake_head_pos(self):
        delta_x = (
            self._current_snake_direction.value[0] * self.pixel_size[0]
            if self._current_snake_direction.value[0]
            else 0
        )
        delta_y = (
            self._current_snake_direction.value[1] * self.pixel_size[1]
            if self._current_snake_direction.value[1]
            else 0
        )

        new_left_top_x = self.snake.body[0][0] + delta_x
        if new_left_top_x < 0:
            new_left_top_x = self.field_size[0] - self.pixel_size[0]
        if new_left_top_x == self.field_size[0]:
            new_left_top_x = 0

        new_left_top_y = self.snake.body[0][1] + delta_y
        if new_left_top_y < 0:
            new_left_top_y = self.field_size[1] - self.pixel_size[1]
        if new_left_top_y == self.field_size[1]:
            new_left_top_y = 0

        new_pos = new_left_top_x, new_left_top_y
        logger.debug(f"New head position will be: {new_pos}")

        for pos in self.snake.body:
            if pos == new_pos:
                self.is_game_over = True
                logger.debug(f"The game was loosed. Collision at position: {new_pos}")

        return new_pos

    def update_field(self):
        logger.debug(f"Snake state before update is: {self.snake}")
        if not self.is_food_spawn:
            self._spawn_food()

        new_pos = self._calc_new_snake_head_pos()

        for food in self.food:
            if self._circle_pos_to_rect_pos(position=food.position) == new_pos:
                self.food.pop()
                logger.debug(f"Food {food} was eaten")
                self.is_food_spawn = False
                self.snake.body.insert(0, new_pos)
                return

        self.snake.body.pop()
        self.snake.body.insert(0, new_pos)

        logger.debug(f"Snake state after update is: {self.snake}")
