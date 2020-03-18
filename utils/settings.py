class Settings:
    """Initialize game settings."""

    def __init__(self):
        # Screen settings
        self.screen_width = 400
        self.screen_height = 400

        # Board settings
        self.cells_in_row = 4
        self.cells_in_column = 4

        # Line settings
        self.line_thickness = 1
        self.line_color = (0, 0, 0)

        # Cells settings
        self.cell_text_color = (30, 30, 30)
        self.cell_colors = {
            # Cell value : Cell color
            "": (230, 230, 230),
            2: (252, 104, 12),
            4: (252, 104, 12),
            8: (229, 160, 57),
            16: (229, 192, 57),
            32: (229, 229, 57),
            64: (114, 229, 57),
            128: (57, 229, 163),
            256: (57, 229, 163),
            512: (57, 223, 229),
            1024: (57, 180, 229),
            2048: (57, 146, 229),
            4096: (57, 111, 229),
            8192: (57, 80, 229),
            16384: (117, 57, 229)
        }
