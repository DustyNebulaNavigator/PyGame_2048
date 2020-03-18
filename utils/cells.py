import pygame


class Cells:
    def __init__(self, settings, x, y):
        value_coordinates = Cells.get_value_coordinates(settings)
        self.value = ""
        self.location = value_coordinates[x][y]
        self.cell_rect = self.create_cell_rect(settings)
        self.cell_color = settings.cell_colors[self.value]
        self.text_color = settings.cell_text_color
        self.font = pygame.font.SysFont(None, 48)
        self.prep_cell(settings)

    def prep_cell(self, settings):
        """Turns cell value into a rendered image."""
        # Creates a new surface - render(text, antialias, text color, background=None)
        self.image = self.font.render(str(self.value), True, self.text_color, None)
        # Creates a rectangle with the size of created image.
        self.image_rect = self.image.get_rect()
        # Gives coordinates to created rectangle
        self.image_rect.center = self.location

    @staticmethod
    def get_value_coordinates(settings):
        """Returns tuple with the center coordinate for every cell."""
        coordinates = []
        cell_width = settings.screen_width / settings.cells_in_row
        cell_height = settings.screen_height / settings.cells_in_column

        row_center_coordinates = [int(cell_width * cell_nr + cell_width / 2) for cell_nr in range(settings.cells_in_row)]
        column_center_coordinates = [int(cell_height * cell_nr + cell_height / 2) for cell_nr in range(settings.cells_in_column)]

        for row_coordinate in row_center_coordinates:
            coordinates.append([(column_coordinate, row_coordinate) for column_coordinate in column_center_coordinates])

        return tuple(coordinates)

    def create_cell_rect(self, settings):
        x, y = self.location
        # parameter meaning for "pygame.Rect()" : (x coordinate, y coordinate, width, height)
        cell_rect = pygame.Rect(x,
                                y,
                                int(settings.screen_width / settings.cells_in_row),
                                int(settings.screen_height / settings.cells_in_column)
                                )
        cell_rect.center = self.location
        return cell_rect

    def change_cell_color(self, settings):
        """Colors for cell backgrounds."""
        self.cell_color = settings.cell_colors[self.value]
