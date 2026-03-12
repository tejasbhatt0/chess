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

current_turn = 'white'
is_flipped = False
promoting_pawn = None
en_passant_target = None

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

        # Capturing logic
        for dc in [-1, 1]:
            target_row = self.row + self.direction
            target_col = self.col + dc

            if 0 <= target_row <= 7 and 0 <= target_col <= 7:
                target_piece = board_state[target_row][target_col]
                if target_piece is not None and target_piece.color != self.color:
                    moves.append((target_row, target_col))

        global en_passant_target
        if en_passant_target is not None:
            ep_r = en_passant_target[0]
            ep_c = en_passant_target[1]

            if self.row + self.direction == ep_r and abs(self.col - ep_c) == 1:
                moves.append((ep_r, ep_c))

        return moves


class Knight(Piece):
    def __init__(self, color, row, col):
        super().__init__(color, row, col)

        self.image = ICONS[f"{self.color}_knight"]

    def get_valid_moves(self, board_state):
        moves = []
        target_sqs = [[self.row + 1, self.col + 2],
                      [self.row + 1, self.col - 2],
                      [self.row - 1, self.col + 2],
                      [self.row - 1, self.col - 2],
                      [self.row + 2, self.col + 1],
                      [self.row + 2, self.col - 1],
                      [self.row - 2, self.col + 1],
                      [self.row - 2, self.col - 1]]
        for t in target_sqs:
            r = t[0]
            c = t[1]

            if 0 <= r <= 7 and 0 <= c <= 7:
                target_sq = board_state[r][c]
                if target_sq is None or target_sq.color != self.color:
                    moves.append((r, c))

        return moves


class Bishop(Piece):
    def __init__(self, color, row, col):
        super().__init__(color, row, col)

        self.image = ICONS[f"{self.color}_bishop"]

    def get_valid_moves(self, board_state):
        moves = []

        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

        for d in directions:
            r = self.row + d[0]
            c = self.col + d[1]

            while 0 <= r <=7 and 0 <= c <=7:
                target_piece = board_state[r][c]
                
                if target_piece is None:
                    moves.append((r, c))
                elif target_piece.color != self.color:
                    moves.append((r, c))
                    break
                else:
                    break
                
                r += d[0]
                c += d[1]
        
        return moves

class Rook(Piece):
    def __init__(self, color, row, col):
        super().__init__(color, row, col)

        self.image = ICONS[f"{self.color}_rook"]

    def get_valid_moves(self, board_state):
        moves = []

        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        for d in directions:
            r = self.row + d[0]
            c = self.col + d[1]

            while 0 <= r <=7 and 0 <= c <=7:
                target_piece = board_state[r][c]
                
                if target_piece is None:
                    moves.append((r, c))
                elif target_piece.color != self.color:
                    moves.append((r, c))
                    break
                else:
                    break

                r += d[0]
                c += d[1]

        return moves

class Queen(Piece):
    def __init__(self, color, row, col):
        super().__init__(color, row, col)

        self.image = ICONS[f"{self.color}_queen"]

    def get_valid_moves(self, board_state):
        moves = []

        # All the direction the Queen can move
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]

        for d in directions:
            r = self.row + d[0]
            c = self.col + d[1]

            while 0 <= r <=7 and 0 <= c <=7:
                target_piece = board_state[r][c]
                
                if target_piece is None:
                    moves.append((r, c))
                elif target_piece.color != self.color:
                    moves.append((r, c))
                    break
                else:
                    break

                r += d[0]
                c += d[1]

        return moves

class King(Piece):
    def __init__(self, color, row, col):
        super().__init__(color, row, col)

        self.image = ICONS[f"{self.color}_king"]

    def get_valid_moves(self, board_state):
        moves = []

        directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]

        for d in directions:
            r = self.row + d[0]
            c = self.col + d[1]

            if 0 <= r <= 7 and 0 <= c <= 7:
                target_piece = board_state[r][c]
                if target_piece is None or target_piece.color != self.color:
                    moves.append((r, c))

        return moves


loadImages(SQSIZE)

# Stores data on where the pieces are on the board
board_state = [[None for _ in range(8)] for _ in range(8)]

# Selected piece memory
selected_piece = None
valid_moves = []

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

clock = pg.time.Clock()
invalid_timer = 0
shaking_piece = None

running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        elif event.type == pg.MOUSEBUTTONDOWN:
            # Gets co-ords where the mouse was cliked and stores it in variables
            x_mouse, y_mouse = pg.mouse.get_pos()

            if promoting_pawn is not None:
                p_row = promoting_pawn.row
                p_col = promoting_pawn.col

                direction = 1 if p_row == 0 else -1
                options = ['queen', 'knight', 'rook', 'bishop']

                for i, option in enumerate(options):
                    menu_row = p_row + (i * direction)
                    dr = 7 - menu_row if is_flipped else menu_row
                    dc = 7 - p_col if is_flipped else p_col

                    rect = pg.Rect(dc * SQSIZE + x_offset, dr * SQSIZE, SQSIZE, SQSIZE)

                    if rect.collidepoint(x_mouse, y_mouse):
                        color = promoting_pawn.color
                        if option == 'queen':
                            board_state[p_row][p_col] = Queen(color, p_row, p_col)
                        elif option == 'knight':
                            board_state[p_row][p_col] = Knight(color, p_row, p_col)
                        elif option == 'bishop':
                            board_state[p_row][p_col] = Bishop(color, p_row, p_col)
                        elif option == 'rook':
                            board_state[p_row][p_col] = Rook(color, p_row, p_col)

                        promoting_pawn = None
                        current_turn = 'black' if current_turn == 'white' else 'white'
                        break
                continue
                    
            # Reverses math to find clicked col
            clicked_col = int((x_mouse - x_offset) // SQSIZE)

            # Reverses math to find clicked row
            clicked_row = int(y_mouse // SQSIZE)

            if is_flipped:
                clicked_col = 7- clicked_col
                clicked_row = 7 - clicked_row
            
            if 0 <= clicked_col <= 7 and 0 <= clicked_row <= 7:
                if selected_piece is not None:
                    valid_moves = selected_piece.get_valid_moves(board_state)
                    if (clicked_row, clicked_col) in valid_moves:

                        # Check for En Passant capture before moving
                        is_en_passant = False
                        if isinstance(selected_piece, Pawn) and (clicked_row, clicked_col) == en_passant_target:
                            is_en_passant = True

                        # Check if this is a double jump to set next target
                        new_ep_target = None

                        if isinstance(selected_piece, Pawn) and abs(selected_piece.row - clicked_row) == 2:
                            new_ep_target = (selected_piece.row + selected_piece.direction, selected_piece.col)
                        
                        # Clear old piece position
                        board_state[selected_piece.row][selected_piece.col] = None
                        # Update the new position
                        selected_piece.move(clicked_row, clicked_col)
                        # Update on the rendered board
                        board_state[clicked_row][clicked_col] = selected_piece
                        

                        if is_en_passant:
                            board_state[clicked_row - selected_piece.direction][clicked_col] = None

                        en_passant_target = new_ep_target

                        if isinstance(selected_piece, Pawn) and (clicked_row == 0 or clicked_row == 7):
                            promoting_pawn = selected_piece
                            selected_piece = None
                            # We will not swap turn yet because the game is frozen
                        else:
                            selected_piece = None

                            if current_turn == 'white':
                                current_turn = 'black'
                            else:
                                current_turn = 'white'
                        
                        invalid_timer = 0

                    else:
                        target_piece = board_state[clicked_row][clicked_col]

                        if target_piece is not None and target_piece.color == selected_piece.color:
                            selected_piece = target_piece
                            invalid_timer = 0
                        else:
                            shaking_piece = selected_piece
                            invalid_timer = 40
                else:
                    clicked_piece = board_state[clicked_row][clicked_col]

                    if clicked_piece is not None:
                        if clicked_piece.color == current_turn:
                            selected_piece = clicked_piece
                            invalid_timer = 0
                        else:
                            shaking_piece = clicked_piece
                            invalid_timer = 40

        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_f:
                is_flipped = not is_flipped


    if current_turn == 'white':
        screen.fill((250, 240, 255)) # Brighter for White
    else:
        screen.fill((220, 200, 225)) # Darker for Black
    
    
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

            display_row = 7 - row if is_flipped else row
            display_col = 7 - col if is_flipped else col

            pg.draw.rect(screen, color, (display_row * SQSIZE + x_offset, display_col * SQSIZE, SQSIZE, SQSIZE))

    if selected_piece is not None:
        s_col = 7 - selected_piece.col if is_flipped else selected_piece.col
        s_row = 7 - selected_piece.row if is_flipped else selected_piece.row

        pg.draw.rect(screen, (100, 255, 255), (s_col * SQSIZE + x_offset, s_row * SQSIZE, SQSIZE, SQSIZE), 4)
        valid_moves = selected_piece.get_valid_moves(board_state)

        for move in valid_moves:
            r = move[0]
            c = move[1]

            dr = 7 - r if is_flipped else r
            dc = 7 - c if is_flipped else c

            x_pos = dc*SQSIZE + x_offset
            y_pos = dr*SQSIZE

            center_x = x_pos + (SQSIZE//2)
            center_y = y_pos + (SQSIZE//2)

            target_piece = board_state[r][c];
            
            if target_piece is None:
                pg.draw.circle(screen, (100, 200, 100), (center_x, center_y), SQSIZE//6)
            else:
                pg.draw.rect(screen, (247, 69, 84), (x_pos, y_pos, SQSIZE, SQSIZE), 5)

    if invalid_timer > 0 and shaking_piece is not None:
        r = 7 - shaking_piece.row if is_flipped else shaking_piece.row
        c = 7 - shaking_piece.col if is_flipped else shaking_piece.col
        pg.draw.rect(screen, (255, 50, 50), (c*SQSIZE + x_offset, r*SQSIZE, SQSIZE, SQSIZE))

    for row in range(8):
        for col in range(8):
            piece = board_state[row][col]
            if piece is not None:
                current_x_offset = x_offset
                draw_row = 7 - row if is_flipped else row
                draw_col = 7 - col if is_flipped else col
                curr_x = draw_col * SQSIZE + x_offset
                
                if invalid_timer > 0 and piece == shaking_piece:
                    shake_amount = int(np.sin(invalid_timer) * 5)
                    curr_x += shake_amount

                y_pos = draw_row * SQSIZE
                img = piece.image

                screen.blit(img, (curr_x + (SQSIZE - img.get_width()) // 2, y_pos + (SQSIZE - img.get_height()) // 2))

    if invalid_timer > 0:
        invalid_timer -= 1

    if promoting_pawn is not None:
        # Dims the background
        dim_surface = pg.Surface((WIDTH, HEIGHT))
        dim_surface.set_alpha(150)
        dim_surface.fill((0, 0, 0))
        screen.blit(dim_surface, (0, 0))

        # Draws the 4 options
        p_row = promoting_pawn.row
        p_col = promoting_pawn.col
        direction = 1 if p_row == 0 else -1
        options = ['queen', 'knight', 'rook', 'bishop']

        for i, option in enumerate(options):
            menu_row = p_row + (i * direction)
            dr = 7 - menu_row if is_flipped else menu_row
            dc = 7 - p_col if is_flipped else p_col

            x_pos = dc * SQSIZE + x_offset
            y_pos = dr * SQSIZE

            # Draw a sq with black border
            pg.draw.rect(screen, (240, 240, 240), (x_pos, y_pos, SQSIZE, SQSIZE))
            pg.draw.rect(screen, (50, 50, 50), (x_pos, y_pos, SQSIZE, SQSIZE), 3)

            # Gets the correct icon and centers it
            img = ICONS[f"{promoting_pawn.color}_{option}"]
            screen.blit(img, (x_pos + (SQSIZE - img.get_width()) // 2, y_pos + (SQSIZE - img.get_height()) // 2))
    pg.display.flip()

    clock.tick(120)

pg.quit()