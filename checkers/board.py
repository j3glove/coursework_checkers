import pygame
from .constants import BLACK, ROWS, RED, SQUARE_SIZE, COLS, WHITE
from .piece import *


class Board:
    def __init__(self):
        self.board = []
        self.red_left = self.white_left = 15
        self.red_kings = self.white_kings = 0
        self.create_board()

    def draw_squares(self, win):
        win.fill(BLACK)
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(win, RED, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def move(self, piece, row, col):
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)

        if row == ROWS - 3 and piece.color == WHITE or row == 0 and piece.color == RED:
            piece.make_king()
            if piece.color == WHITE:
                self.white_kings += 1
            else:
                self.red_kings += 1

    def get_piece(self, row, col):
        return self.board[row][col]

    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if col % 2 == ((row + 1) % 2):
                    if row < 3:
                        self.board[row].append(Piece(row, col, WHITE))
                    elif row > 4:
                        self.board[row].append(Piece(row, col, RED))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)
        print(self.board)

    def draw(self, win):
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)

    def remove(self, piece):
            self.board[piece.row][piece.col] = 0
            if piece != 0:
                if piece.color == RED:
                    self.red_left -= 1
                else:
                    self.white_left -= 1

    def winner(self):
        if self.red_left <= 0:
            return RED
        elif self.white_left <= 0:
            return WHITE

        return None

    @staticmethod
    def is_valid_coordinates(piece_x, piece_y):
        return 0 <= piece_x < 10 and 0 <= piece_y < 8

    def get_figure_at(self, piece_x, piece_y):
        if not(self.is_valid_coordinates(piece_x, piece_y)):
            return -1
        return self.board[piece_y][piece_x]


    def get_valid_moves(self, piece):
        moves = {}

        if piece.color == RED:
            for i in range(piece.col - 1, piece.col + 2, 2):
                if i >= 0 and i < COLS and self.board[piece.row + 1][i] != 0 and self.board[piece.row + 1][i].color == WHITE:
                    if i > piece.col:
                        moves.update(self.check_pos(piece.col, piece.row, piece))
                    else:
                        moves.update(self.check_pos(piece.col, piece.row, piece))
            moves.update(self.check_pos(piece.col, piece.row, piece))
        if piece.color == WHITE:
            for i in range(piece.col - 1, piece.col + 2, 2):
                if i >= 0 and i < COLS and self.board[piece.row - 1][i] != 0 and self.board[piece.row - 1][i].color == RED:
                    if i > piece.col:
                        moves.update(self.check_pos(piece.col, piece.row, piece))
                    else:
                        moves.update(self.check_pos(piece.col, piece.row, piece))
            moves.update(self.check_pos(piece.col, piece.row, piece))
        if piece.king:
            moves.update(self.test_red(piece.col, piece.row))

        return moves

    def check_pos(self, piece_x, piece_y, piece):
        moves = {}
        curcolor = self.get_figure_at(piece_x, piece_y).color
        y = piece_y
        x = piece_x
        if curcolor == WHITE or piece.king or (curcolor == RED and self.get_figure_at(x + 1, y + 1) == WHITE):
            dx = 0
            dy = 0
            while True:
                dx += 1
                dy += 1
                if self.get_figure_at(x + dx, y + dy) == 0:
                    moves[(y + dy, x + dx)] = self.get_figure_at(x + dx, y + dy)
                    break
                else:
                    if self.get_figure_at(x + dx + 1, y + dy + 1) != 0 or curcolor == self.get_figure_at(x + dx, y + dy).color:
                        break
                    if self.get_figure_at(x + dx, y + dy) != 0 and curcolor != self.get_figure_at(x + dx,y + dy).color and self.get_figure_at(x + dx + 1, y + dy + 1) == 0:
                        moves[(y + dy + 1, x + dx + 1)] = self.get_figure_at(x + dx + 1, y + dy + 1)

        if curcolor == WHITE or piece.king or (curcolor == RED and self.get_figure_at(x - 1, y + 1) == WHITE):
            dx = 0
            dy = 0
            while True:
                dx -= 1
                dy += 1
                if self.get_figure_at(x + dx, y + dy) == 0:
                    moves[(y + dy, x + dx)] = self.get_figure_at(x + dx, y + dy)
                    break
                else:
                    if self.get_figure_at(x + dx - 1, y + dy + 1) != 0 or curcolor == self.get_figure_at(x + dx, y + dy).color:
                        break
                    if self.get_figure_at(x + dx, y + dy) != 0 and curcolor != self.get_figure_at(x + dx,y + dy).color and self.get_figure_at(x + dx - 1, y + dy + 1) == 0:
                        moves[(y + dy + 1, x + dx - 1)] = self.get_figure_at(x + dx - 1, y + dy + 1)

        if curcolor == RED or piece.king or (curcolor == WHITE and self.get_figure_at(x + 1, y - 1) == RED):
            dx = 0
            dy = 0
            while True:
                dx += 1
                dy -= 1
                if self.get_figure_at(x + dx, y + dy) == 0:
                    moves[(y + dy, x + dx)] = self.get_figure_at(x + dx, y + dy)
                    break
                else:
                    if self.get_figure_at(x + dx + 1, y + dy - 1) != 0 or curcolor == self.get_figure_at(x + dx, y + dy).color:
                        break
                    if self.get_figure_at(x + dx, y + dy) != 0 and curcolor != self.get_figure_at(x + dx, y + dy).color and self.get_figure_at(x + dx + 1, y + dy - 1) == 0:
                        moves[(y + dy - 1, x + dx + 1)] = self.get_figure_at(x + dx + 1, y + dy - 1)

        if curcolor == RED or piece.king or (curcolor == WHITE and self.get_figure_at(x - 1, y - 1) == RED):
            dx = 0
            dy = 0
            while True:
                dx -= 1
                dy -= 1
                if self.get_figure_at(x + dx, y + dy) == 0:
                    moves[(y + dy, x + dx)] = self.get_figure_at(x + dx, y + dy)
                    break
                else:
                    if self.get_figure_at(x + dx - 1, y + dy - 1) != 0 or curcolor == self.get_figure_at(x + dx, y + dy).color:
                        break
                    if self.get_figure_at(x + dx, y + dy) != 0  and curcolor != self.get_figure_at(x + dx,y + dy).color and self.get_figure_at(x + dx - 1, y + dy - 1) == 0:
                        moves[(y + dy - 1, x + dx - 1)] = self.get_figure_at(x + dx - 1, y + dy - 1)

        return moves

    def test_red(self, piece_x, piece_y):
        moves = {}
        curcolor = self.get_figure_at(piece_x, piece_y).color
        y = piece_y
        x = piece_x
        dx = 0
        dy = 0
        while True:
            dx += 1
            dy += 1
            if self.get_figure_at(x + dx, y + dy) == 0:
                moves[(y + dy, x + dx)] = self.get_figure_at(x + dx, y + dy)
            else:
                if self.get_figure_at(x + dx + 1, y + dy + 1) != 0 or curcolor == self.get_figure_at(x + dx, y + dy).color:
                    break
                if self.get_figure_at(x + dx, y + dy) != 0 and curcolor != self.get_figure_at(x + dx,y + dy).color:
                    pass


        dx = 0
        dy = 0
        while True:
            dx -= 1
            dy += 1
            if self.get_figure_at(x + dx, y + dy) == 0:
                moves[(y + dy, x + dx)] = self.get_figure_at(x + dx, y + dy)
            else:
                if self.get_figure_at(x + dx - 1, y + dy + 1) != 0 or curcolor == self.get_figure_at(x + dx, y + dy).color:
                    break
                if self.get_figure_at(x + dx, y + dy) != 0 and curcolor != self.get_figure_at(x + dx,y + dy).color:
                    pass


        dx = 0
        dy = 0
        while True:
            dx += 1
            dy -= 1
            if self.get_figure_at(x + dx, y + dy) == 0:
                moves[(y + dy, x + dx)] = self.get_figure_at(x + dx, y + dy)
            else:
                if self.get_figure_at(x + dx + 1, y + dy - 1) != 0 or curcolor == self.get_figure_at(x + dx, y + dy).color:
                    break
                if self.get_figure_at(x + dx, y + dy) != 0 and curcolor != self.get_figure_at(x + dx, y + dy).color:
                    pass



        dx = 0
        dy = 0
        while True:
            dx -= 1
            dy -= 1
            if self.get_figure_at(x + dx, y + dy) == 0:
                moves[(y + dy, x + dx)] = self.get_figure_at(x + dx, y + dy)
            else:
                if self.get_figure_at(x + dx - 1, y + dy - 1) != 0 or curcolor == self.get_figure_at(x + dx, y + dy).color:
                    break
                if self.get_figure_at(x + dx, y + dy) != 0  and curcolor != self.get_figure_at(x + dx,y + dy).color:
                    pass


        return moves