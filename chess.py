import pygame as pg
import numpy as np

pg.init()
WIDTH = 1000
HEIGHT = 600

screen = pg.display.set_mode((WIDTH, HEIGHT))
bgColor = (250, 224, 255)
lightSq = (240, 217, 181)
darkSq = (181, 136, 99)

boardPattern = np.zeros((8,8), dtype = int)
SQSIZE = HEIGHT // 8
x_offset = WIDTH // 2 - 4*SQSIZE

board_state = 
[
    [black_rook, ],
    [],
    [],
    [],
    [],
    [],
    [],
    []
]

ICONS = {}

def loadImages(sqsize):
    colors = ['white', 'black']
    piece_type = ['pawn', 'knight', 'rook', 'queen', 'bishop', 'king']

    for color in colors:
        for type in piece_type:
            name = f"{color}_{type}"

            img = pg.image.load(f"icons/{name}.png").convert_alpha()
            scaled_img = pg.transform.smoothscale(img, (sqsize, sqsize))

            ICONS[name] = scaled_img

class Piece:
    def __init__(self, color, row, col):
        self.color = color
        self.hasMoved = False
        self.alive = True
        self.row = row
        self.col = col

        self.image = None

    def move(self, new_row, new_col):
        self.row = new_row
        self.col = new_col
        self.hasMoved = True

    def draw(self, screen, sqsize, x_offset):
        x_pos = self.col * sqsize + x_offset
        y_pos = self.row * sqsize

        if self.image is not None:
            screen.blit(self.image, (x_pos, y_pos))

    def get_valid_moves(self, board_state):
        raise NotImplementedError("Every specific piece must write its own movement math!")

class Pawn(Piece):
    def __init__(self, color, row, col):
        super().__init__(color, row, col)

        icon_key = f"{color}_pawn"
        self.image = ICONS[icon_key]

        if self.color == 'white':
            self.direction = -1
        else:
            self.direction = 1

    def get_valid_moves(self, board_state):
        # piece logic

        pass

class Knight(Piece):
    def __init__(self, color, row, col):
        super().__init__(color, row, col)

        self.image = ICONS[f"{self.color}_knight"]

class Bishop(Piece):
    def __init__(self, color, row, col):
        super().__init__(color, row, col)

        self.image = ICONS[f"{self.color}_bishop"]

class Rook(Piece):
    def __init__(self, color, row, col):
        super().__init__(color, row, col)

        self.image = ICONS[f"{self.color}_rook"]

class Queen(Piece):
    def __init__(self, color, row, col):
        super().__init__(color, row, col)

        self.image = ICONS[f"{self.color}_queen"]

class King(Piece):
    def __init__(self, color, row, col):
        super().__init__(color, row, col)

        self.image = ICONS[f"{self.color}_king"]


loadImages(SQSIZE)

running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    screen.fill(bgColor)

    for row in range(8):
        for col in range(8):
            if ((row + col) % 2 == 0):
                boardPattern[row][col] = 0
                color = lightSq
            else:
                boardPattern[row][col] = 1
                color = darkSq

            x_pos = col * SQSIZE + (WIDTH // 2 - 4*SQSIZE)
            y_pos = row * SQSIZE

            pg.draw.rect(screen, color, (x_pos, y_pos, SQSIZE, SQSIZE))

    pg.display.flip()

pg.quit()