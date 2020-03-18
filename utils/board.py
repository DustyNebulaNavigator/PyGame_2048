from random import choice, randint
from sys import exit

from utils.cells import Cells
from pygame import K_RIGHT, K_DOWN, K_LEFT, K_UP
import pygame


class Board:
    def __init__(self, settings, screen):
        self.cells = self.generate_cell_instances(settings)
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.movement_keys = [K_UP, K_RIGHT, K_DOWN, K_LEFT]
        self.font = pygame.font.SysFont(None, 48)

    def __str__(self):
        """Will display game board when instance is passed to print function."""
        board_str = ""
        for line in self.cells:
            for instance in line:
                board_str += str(instance.value).rjust(5)
            board_str += "\n"
        return board_str

    def random_empty_location(self):
        """Returns tuple with coordinates to one empty cell."""
        empty_locations = []
        for line_nr, line in enumerate(self.cells):
            for column_nr, instance in enumerate(line):
                if instance.value == "":
                    empty_locations.append([line_nr, column_nr])
        random_location = tuple(empty_locations[randint(0, len(empty_locations)-1)])
        return random_location

    def add_tile(self, settings, quantity=1):
        """Fills as much empty cells, as passed by parameter."""
        for _ in range(quantity):
            x, y = self.random_empty_location()
            self.cells[x][y].value = choice([2, 2, 4])
            self.cells[x][y].prep_cell(settings)

    def calculate(self, direction, settings, game_over_check=False):
        cells_in_row = settings.cells_in_row
        cells_in_column = settings.cells_in_column
        """Makes required calculations and calls move method."""
        change_made = False
        if direction == K_LEFT:
            for row in range(cells_in_row):
                for column in range(cells_in_column-1):
                    if self.cells[row][column].value == self.cells[row][column + 1].value and self.cells[row][column].value != "":
                        if game_over_check:
                            # If program is checking possible moves for game over and found one
                            # then returns here to avoid cell changes without user input.
                            return False
                        self.cells[row][column].value = self.cells[row][column].value * 2
                        self.cells[row][column + 1].value = ""
                        change_made = True

        if direction == K_RIGHT:
            for row in range(cells_in_row):
                for column in range(cells_in_column-1, 0, -1):
                    if self.cells[row][column].value == self.cells[row][column - 1].value and self.cells[row][column].value != "":
                        if game_over_check:
                            return False
                        self.cells[row][column].value = self.cells[row][column].value * 2
                        self.cells[row][column - 1].value = ""
                        change_made = True

        if direction == K_UP:
            for column in range(cells_in_row):
                for row in range(cells_in_column-1):
                    if self.cells[row][column].value == self.cells[row+1][column].value and self.cells[row][column].value != "":
                        if game_over_check:
                            return False
                        self.cells[row][column].value = self.cells[row][column].value * 2
                        self.cells[row+1][column].value = ""
                        change_made = True

        if direction == K_DOWN:
            for column in range(cells_in_row):
                for row in range(cells_in_column-1, 0, -1):
                    if self.cells[row][column].value == self.cells[row - 1][column].value and self.cells[row][column].value != "":
                        if game_over_check:
                            return False
                        self.cells[row][column].value = self.cells[row][column].value * 2
                        self.cells[row-1][column].value = ""
                        change_made = True

        if game_over_check:
            # If no horizontal or vertical addition is possible then game over checking reaches here.
            # If no free cells left, then True is returned and Game is over.
            try:
                self.random_empty_location()
            except ValueError:
                # Game is over
                return True

        return change_made

    def move(self, direction, settings):
        """Moves all cells to given direction. ->|1.1.| K_right -> |..11|"""
        cells_in_row = settings.cells_in_row
        cells_in_column = settings.cells_in_column

        change_made = False
        if direction == K_RIGHT:
            for row in range(cells_in_row):
                column = 0
                while column < cells_in_column-1:
                    if self.cells[row][column].value != "" and self.cells[row][column + 1].value == "":
                        self.cells[row][column].value, self.cells[row][column + 1].value = self.cells[row][column + 1].value, self.cells[row][column].value
                        column = 0
                        change_made = True
                        continue
                    column += 1

        if direction == K_LEFT:
            for row in range(cells_in_row):
                column = cells_in_column-1
                while column > 0:
                    if self.cells[row][column].value != "" and self.cells[row][column - 1].value == "":
                        self.cells[row][column].value, self.cells[row][column - 1].value = self.cells[row][column - 1].value, self.cells[row][column].value
                        column = cells_in_column-1
                        change_made = True
                        continue
                    column -= 1

        if direction == K_UP:
            for column in range(cells_in_column):
                row = cells_in_row-1
                while row > 0:
                    if self.cells[row][column].value != "" and self.cells[row-1][column].value == "":
                        self.cells[row][column].value, self.cells[row-1][column].value = self.cells[row-1][column].value, self.cells[row][column].value
                        row = cells_in_row-1
                        change_made = True
                        continue
                    row -= 1

        if direction == K_DOWN:
            for column in range(cells_in_column):
                row = 0
                while row < cells_in_row-1:
                    if self.cells[row][column].value != "" and self.cells[row+1][column].value == "":
                        self.cells[row][column].value, self.cells[row+1][column].value = self.cells[row+1][column].value, self.cells[row][column].value
                        row = 0
                        change_made = True
                        continue
                    row += 1
        return change_made

    def check_game_over(self, settings):
        """Checks if movement in any direction would cause addition of some tiles."""
        if not self.calculate(K_UP, settings, game_over_check=True):
            # Game is not over
            return False
        if not self.calculate(K_RIGHT, settings, game_over_check=True):
            # Game is not over
            return False
        # Game is over
        return True

    def reset_game(self, settings):
        """Used to start new game when player has lost previous one."""
        self.cells = self.generate_cell_instances(settings)
        self.add_tile(settings, quantity=3)

    def game_over(self, settings):
        """The screen that is shown when GAME is OVER"""
        while True:
            # screen center coordinates
            x_center, y_center = self.screen_rect.center

            # Text: "Press 'n' for new game."
            image_new_game = self.font.render("Press 'n' for NEW GAME", True, [0, 0, 0], None)
            image_new_game_rect = image_new_game.get_rect()
            image_new_game_rect.center = (x_center, y_center - 100)
            self.screen.blit(image_new_game, image_new_game_rect)

            # Text: "GAME OVER"
            image_game_over = self.font.render("GAME OVER", True, [0, 125, 250], None)
            image_game_over_rect = image_game_over.get_rect()
            image_game_over_rect.center = self.screen_rect.center
            self.screen.blit(image_game_over, image_game_over_rect)

            # Text: "Press 'q' to quit game."
            image_quit = self.font.render("Press 'q' to quit game", True, [0, 125, 250], None)
            image_quit_rect = image_quit.get_rect()
            image_quit_rect.center = (x_center, y_center + 100)
            self.screen.blit(image_quit, image_quit_rect)

            # Draws new display.
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # If game window is closed.
                    exit()
                elif event.type == pygame.KEYDOWN:
                    # If keyboard keys are pressed.
                    if event.key == pygame.K_q:
                        exit()
                    if event.key == pygame.K_n:
                        self.reset_game(settings)
                        return None

    @staticmethod
    def generate_cell_instances(settings):
        cell_instances = []
        for row in range(settings.cells_in_row):

            cell_instances_in_row = [Cells(settings, row, column) for column in range(settings.cells_in_column)]
            cell_instances.append(cell_instances_in_row)

        return cell_instances

    def draw_board(self, settings):
        for row_nr, row in enumerate(self.cells):
            for column_nr, cell in enumerate(row):

                # Change cell background color
                cell.change_cell_color(settings)

                # Draws cells (just background). parameters: (destination surface, desired color, rectangle)
                pygame.draw.rect(self.screen, self.cells[row_nr][column_nr].cell_color, self.cells[row_nr][column_nr].cell_rect)

                # Creates images from from cell values.
                self.cells[row_nr][column_nr].prep_cell(settings)

                # Draws cell values to game board.
                self.screen.blit(cell.image, cell.image_rect)
