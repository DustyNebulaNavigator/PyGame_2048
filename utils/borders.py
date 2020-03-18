import pygame


class Borders:
    def __init__(self, settings):
        self.list_of_borders = self.generate_borders(settings)

    @staticmethod
    def generate_borders(settings):
        borders = []

        # Horizontal borders
        horizontal_gap = settings.screen_width / settings.cells_in_row
        for border_nr in range(settings.cells_in_row + 1):
            # Line thickness must be subtracted from last 'x' coordinate.
            # Other ways it's going to be drawn outside screen, and wont be visible.
            if border_nr < settings.cells_in_row:
                x = horizontal_gap * border_nr
            else:
                x = horizontal_gap * border_nr - settings.line_thickness
            # Creates a line rectangle and add it to list
            borders.append(pygame.Rect(x,
                                       0,
                                       settings.line_thickness,
                                       settings.screen_height
                                       ))

        # Vertical borders
        horizontal_gap = settings.screen_width / settings.cells_in_row
        for border_nr in range(settings.cells_in_row + 1):
            # Line thickness must be subtracted from last 'y' coordinate.
            # Other ways it's going to be drawn outside screen, and wont be visible.
            if border_nr < settings.cells_in_row:
                y = horizontal_gap * border_nr
            else:
                y = horizontal_gap * border_nr - settings.line_thickness
            # Creates a line rectangle and add it to list
            borders.append(pygame.Rect(0,
                                       y,
                                       settings.screen_width,
                                       settings.line_thickness
                                       ))

        return borders

    def draw_lines(self, screen, settings):
        for line in self.list_of_borders:
            # Draws line rectangles. Parameters: (destination surface, rectangle color, rectangle)
            pygame.draw.rect(screen, settings.line_color, line)
