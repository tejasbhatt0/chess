import pygame as pg
import numpy as np
import sys
import os

def resource_path(relative_path):
    # If running as an .exe, look in the temp folder. Otherwise, look in the normal folder.
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

# Initialize pygame
pg.init()
WIDTH = 1000
HEIGHT = 600

# Create screen object, decide background colour, and colour of light and dark squares
screen = pg.display.set_mode((WIDTH, HEIGHT))
bgColor = (250, 224, 255)
lightSq = (240, 217, 181)
darkSq = (181, 136, 99)

# Creates the board pattern that renders the alternating pattern eventually (rn has only 0s) 
boardPattern = np.zeros((8,8), dtype = int)

SQSIZE = HEIGHT // 8
x_offset = WIDTH // 2 - 4*SQSIZE

# Created to store all the chess piece icons
ICONS = {}

# Loads icon pieces
def loadImages(sqsize):
    colors = ['white', 'black']
    piece_type = ['pawn', 'knight', 'rook', 'queen', 'bishop', 'king']

    for color in colors:
        for type in piece_type:
            name = f"{color}_{type}"

            img_path = resource_path(f"icons/{name}.png")
            img = pg.image.load(img_path).convert_alpha()
            scaled_img = pg.transform.scale(img, (sqsize*0.8, sqsize*0.8))

            ICONS[name] = scaled_img

# Piece class that all other piece types will inherit
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
        x_sq = self.col * sqsize + x_offset
        y_sq = self.row * sqsize

        if self.image is not None:

            x_off = (sqsize - self.image.get_width()) // 2
            y_off = (sqsize - self.image.get_height()) // 2

            x_center = x_sq + x_off
            y_center = y_sq + y_off
            screen.blit(self.image, (x_center, y_center))

    def get_valid_moves(self, board_state):
        raise NotImplementedError("Every specific piece must write its own movement math!")

# Classes from here are pretty self-explanatory
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
        moves = []

        one_step = self.row + self.direction
        if 0 <= one_step <= 7 and board_state[one_step][self.col] is None:
            moves.append((one_step, self.col))

            if self.hasMoved is False:
                two_step = self.row + 2*self.direction
                if 0 <= two_step <= 7 and board_state[two_step][self.col] is None:
                    moves.append((two_step, self.col))

        return moves


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

# Stores data on where the pieces are on the board
board_state = [[None for _ in range(8)] for _ in range(8)]

# Selected piece memory
selected_piece = None

def setupBoard():
    for i in range(8):
        for j in range(8):
            # Sets up all the pawns
            if i == 1:
                board_state[i][j] = Pawn('black', i, j)
            elif i == 6:
                board_state[i][j] = Pawn('white', i, j)

            # Sets up all other black pieces
            if i == 0:
                # Rooks
                if j == 0 or j == 7:
                    board_state[i][j] = Rook('black', i, j)
                
                # Knights
                if j == 1 or j == 6:
                    board_state[i][j] = Knight('black', i, j)
                
                # Bishops
                if j == 2 or j == 5:
                    board_state[i][j] = Bishop('black', i, j)
                
                # The Queen
                if j == 3:
                    board_state[i][j] = Queen('black', i, j)

                # The King
                if j == 4:
                    board_state[i][j] = King('black', i, j)

            # And again for the white pieces
            elif i == 7:

                if j == 0 or j == 7:
                    board_state[i][j] = Rook('white', i, j)

                if j == 1 or j == 6:
                    board_state[i][j] = Knight('white', i, j)

                if j == 2 or j == 5:
                    board_state[i][j] = Bishop('white', i, j)

                if j == 3:
                    board_state[i][j] = Queen('white', i, j)

                if j == 4:
                    board_state[i][j] = King('white', i, j)

setupBoard()

running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        elif event.type == pg.MOUSEBUTTONDOWN:
            # Gets co-ords where the mouse was cliked and stores it in variables
            x_mouse, y_mouse = pg.mouse.get_pos()

            # Reverses math to find clicked col
            clicked_col = int((x_mouse - x_offset) // SQSIZE)

            # Reverses math to find clicked row
            clicked_row = int(y_mouse // SQSIZE)

            if 0 <= clicked_col <= 7 and 0 <= clicked_row <= 7:
                selected_piece = board_state[clicked_row][clicked_col]

                if selected_piece:
                    print(f"The valid moves are: {selected_piece.get_valid_moves(board_state)}")

                if selected_piece is not None:
                    print('clicked piece')
                else:
                    print("didn't click piece")

    screen.fill(bgColor)

    for row in range(8):
        for col in range(8):
            if ((row + col) % 2 == 0):
                boardPattern[row][col] = 0
                color = lightSq
            else:
                boardPattern[row][col] = 1
                color = darkSq

            x_pos = col * SQSIZE + x_offset
            y_pos = row * SQSIZE

            pg.draw.rect(screen, color, (x_pos, y_pos, SQSIZE, SQSIZE))

            if selected_piece is not None:
                x_high = selected_piece.col * SQSIZE + x_offset
                y_high = selected_piece.row * SQSIZE

                pg.draw.rect(screen, (100, 255, 255), (x_high, y_high, SQSIZE, SQSIZE), 4)

            piece = board_state[row][col]
            if piece is not None:
                piece.draw(screen, SQSIZE, x_offset)

    pg.display.flip()

pg.quit()