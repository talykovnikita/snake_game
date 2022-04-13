import pygame
from pygame import Surface
from typing import Tuple

from snake_game.models.food.food import Food
from snake_game.snake_game_controller import SnakeGameController
from snake_game.utils.enums import Colors, Directions, FoodTypes

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


def main():
    pygame.init()

    game_surface = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("Snake game by NT")
    clock = pygame.time.Clock()

    game_controller = SnakeGameController(
        field_size=WINDOW_SIZE,
        head_start_pos=HEAD_START_POS,
        pixel_size=PIXEL_SIZE,
    )

    while not game_controller.is_game_over:
        is_event_caught: bool = False
        for event in pygame.event.get():
            if is_event_caught:
                break

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_UP, pygame.K_w]:
                    game_controller.current_snake_direction = Directions.UP
                    is_event_caught = True
                if event.key in [pygame.K_RIGHT, pygame.K_d]:
                    game_controller.current_snake_direction = Directions.RIGHT
                    is_event_caught = True
                if event.key in [pygame.K_DOWN, pygame.K_s]:
                    game_controller.current_snake_direction = Directions.DOWN
                    is_event_caught = True
                if event.key in [pygame.K_LEFT, pygame.K_a]:
                    game_controller.current_snake_direction = Directions.LEFT
                    is_event_caught = True

        game_controller.update_field()
        draw_game(game_surface=game_surface, game_controller=game_controller)
        pygame.display.update()
        clock.tick(FPS_MAX)
    pygame.quit()
    quit()


def draw_game(game_surface: Surface, game_controller: SnakeGameController):
    game_surface.fill(color=BACKGROUND_COLOR)
    draw_snake(game_surface=game_surface, game_controller=game_controller)
    draw_food(game_surface=game_surface, game_controller=game_controller)
    draw_score_board(game_surface=game_surface, game_controller=game_controller)


def draw_snake(game_surface: Surface, game_controller: SnakeGameController):
    snake_item: Tuple[int, int]
    for snake_item in game_controller.snake.body:
        pygame.draw.rect(
            surface=game_surface,
            color=SNAKE_COLOR,
            rect=[snake_item, game_controller.pixel_size],
        )


def draw_food(game_surface: Surface, game_controller: SnakeGameController):
    food_item: Food
    for food_item in game_controller.food:
        pygame.draw.circle(
            surface=game_surface,
            color=COLOR_BY_FOOD[food_item.type],
            center=(food_item.position[0], food_item.position[1]),
            radius=game_controller.pixel_size[0] // 2,
        )


def draw_score_board(game_surface: Surface, game_controller: SnakeGameController):
    font = pygame.font.Font(pygame.font.get_default_font(), 16)
    text = (
        f"Score: {game_controller.current_score} (Record: {game_controller.record})"
    )
    score_surface = font.render(text, True, Colors.WHITE.value)
    game_surface.blit(score_surface, (0, 0))


if __name__ == "__main__":
    main()
