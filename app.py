"""
This is a game of 2048
30.11.2019
Mihkel Siim
"""

import pygame
import sys
from utils.board import Board
from utils.settings import Settings
from utils.borders import Borders


def main():
    pygame.init()
    clock_object = pygame.time.Clock()
    game_settings = Settings()
    lines = Borders(game_settings)

    # initialize screen size
    screen = pygame.display.set_mode((game_settings.screen_width, game_settings.screen_height))
    pygame.display.set_caption("2048")

    # Create game instance and add three cells to it.
    game_board = Board(game_settings, screen)
    game_board.add_tile(game_settings, quantity=3)

    while True:
        # Limits screen refreshment speed.
        clock_object.tick(30)

        game_board.draw_board(game_settings)
        lines.draw_lines(screen, game_settings)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # If game window is closed.
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                # If keyboard keys are pressed.
                if event.key in game_board.movement_keys:
                    # New tile is added only if key press initiated a change in game board.
                    # If move() or calculate() returns True, then cell value was modified, and new tile is added.
                    change_in_move_1 = game_board.move(event.key, game_settings)
                    change_in_calculate = game_board.calculate(event.key, game_settings)
                    change_in_move_2 = game_board.move(event.key, game_settings)
                    if change_in_move_1 or change_in_move_2 or change_in_calculate:
                        game_board.add_tile(game_settings, quantity=1)
                    elif game_board.check_game_over(game_settings):
                        game_board.game_over(game_settings)

                elif event.key == pygame.K_q:
                    sys.exit()

        pygame.display.flip()


if __name__ == "__main__":
    main()
