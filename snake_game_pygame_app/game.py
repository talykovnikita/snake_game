import logging
from typing import Tuple

import pygame
import pygame_menu

from snake_game import app_logger
from snake_game.models.food.food import Food
from snake_game.snake_game_controller import SnakeGameController
from snake_game.utils.enums import Colors, Directions, FoodTypes

logger = app_logger.get_logger(__name__, level=logging.DEBUG)

PIXEL_SIZE = (30, 30)
FIELD_SIZE = (50, 30)
WINDOW_SIZE = (PIXEL_SIZE[0] * FIELD_SIZE[0], PIXEL_SIZE[1] * FIELD_SIZE[1])
HEAD_START_POS = (
    PIXEL_SIZE[0] * FIELD_SIZE[0] // 2,
    PIXEL_SIZE[1] * FIELD_SIZE[1] // 2,
)
FPS_MAX = 16
SNAKE_COLOR = Colors.BLUE.value
BACKGROUND_COLOR = Colors.BLACK.value
COLOR_BY_FOOD = {FoodTypes.APPLE: Colors.GREEN.value}


class GameView:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Snake game by NT")

        self.game_surface = pygame.display.set_mode(WINDOW_SIZE)
        self.clock = pygame.time.Clock()

        self.last_score = None
        self.menu = pygame_menu.Menu(
            "Main menu ", 400, 300, theme=pygame_menu.themes.THEME_DARK
        )

        self.game_controller = None

    def run(self):
        self.show_menu()

    def show_menu(self):
        self.menu.add.button("Play", self.game_loop)
        self.menu.add.button("Quit", pygame_menu.events.EXIT)

        self.menu.mainloop(self.game_surface)

    def game_loop(self):
        self.game_controller = SnakeGameController(
            field_size=WINDOW_SIZE,
            head_start_pos=HEAD_START_POS,
            pixel_size=PIXEL_SIZE,
        )
        while not self.game_controller.is_game_over:
            is_event_caught: bool = False
            for event in pygame.event.get():
                if is_event_caught:
                    break

                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_UP, pygame.K_w]:
                        self.game_controller.current_snake_direction = Directions.UP
                        is_event_caught = True
                    if event.key in [pygame.K_RIGHT, pygame.K_d]:
                        self.game_controller.current_snake_direction = Directions.RIGHT
                        is_event_caught = True
                    if event.key in [pygame.K_DOWN, pygame.K_s]:
                        self.game_controller.current_snake_direction = Directions.DOWN
                        is_event_caught = True
                    if event.key in [pygame.K_LEFT, pygame.K_a]:
                        self.game_controller.current_snake_direction = Directions.LEFT
                        is_event_caught = True

            self.game_controller.update_field()
            self.draw_game()
            pygame.display.update()
            self.clock.tick(FPS_MAX)
            logger.debug(f"Update: {self.last_score=}")
            self.last_score = self.game_controller.current_score

        self.menu.clear()
        self.menu.add.label(f"Score: {self.game_controller.current_score}")
        self.menu.add.button("Play again", self.game_loop)
        self.menu.add.button("Quit", pygame.quit)

    def draw_game(self):
        self.game_surface.fill(color=BACKGROUND_COLOR)
        self.draw_snake()
        self.draw_food()
        self.draw_score_board()

    def draw_snake(self):
        snake_item: Tuple[int, int]
        for snake_item in self.game_controller.snake.body:
            pygame.draw.rect(
                surface=self.game_surface,
                color=SNAKE_COLOR,
                rect=[snake_item, self.game_controller.pixel_size],
            )

    def draw_food(self):
        food_item: Food
        for food_item in self.game_controller.food:
            pygame.draw.circle(
                surface=self.game_surface,
                color=COLOR_BY_FOOD[food_item.type],
                center=(food_item.position[0], food_item.position[1]),
                radius=self.game_controller.pixel_size[0] // 2,
            )

    def draw_score_board(self):
        font = pygame.font.Font(pygame.font.get_default_font(), 16)
        text = f"Score: {self.game_controller.current_score} (Record: {self.game_controller.record})"
        score_surface = font.render(text, True, Colors.WHITE.value)
        self.game_surface.blit(score_surface, (0, 0))
