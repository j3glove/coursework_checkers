import pygame
from .constants import BLACK, ROWS, RED, SQUARE_SIZE, COLS, WHITE
from .piece import Piece


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

    def remove(self, pieces):
        for piece in pieces:
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

    def get_valid_moves(self, piece):
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row


        if piece.color == RED:
            for i in range(piece.col - 1, piece.col + 2, 2):
                if i >= 0 and i < COLS and self.board[piece.row + 1][i] != 0 and self.board[piece.row + 1][i].color == WHITE:
                    if i > piece.col:
                        moves.update(self._traverse_right(row + 1, min(row + 3, ROWS), 1, piece.color, right))
                    else:
                        moves.update(self._traverse_left(row + 1, min(row + 3, ROWS), 1, piece.color, left))
            moves.update(self._traverse_left(row - 1, max(row - 3, -1), -1, piece.color, left))
            moves.update(self._traverse_right(row - 1, max(row - 3, -1), -1, piece.color, right))
        if piece.color == WHITE:
            for i in range(piece.col - 1, piece.col + 2, 2):
                if i >= 0 and i < COLS and self.board[piece.row - 1][i] != 0 and self.board[piece.row - 1][i].color == RED:
                    if i > piece.col:
                        moves.update(self._traverse_right(row - 1, max(row - 3, -1), -1, piece.color, right))
                    else:
                        moves.update(self._traverse_left(row - 1, max(row - 3, -1), -1, piece.color, left))
            moves.update(self._traverse_left(row + 1, min(row + 3, ROWS), 1, piece.color, left))
            moves.update(self._traverse_right(row + 1, min(row + 3, ROWS), 1, piece.color, right))
        if piece.king:
            moves.update(self.test_red(piece.col, piece.row))
                # moves.update(self.king_traverse_left(row + 1, min(row + 3, ROWS), 1, piece.color, left))
                # moves.update(self.king_traverse_right(row + 1, min(row + 3, ROWS), 1, piece.color, right))
                # moves.update(self.king_traverse_left(row - 1, max(row - 3, -1), -1, piece.color, left))
                # moves.update(self.king_traverse_right(row - 1, max(row - 3, -1), -1, piece.color, right))

        return moves

    def _traverse_left(self, start, stop, step, color, left, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:
                break

            current = self.board[r][left]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, left)] = last + skipped
                else:
                    moves[(r, left)] = last

                if last:
                    if step == -1:
                        row = max(r - 3, -1)
                    else:
                        row = min(r + 3, ROWS)
                    moves.update(self._traverse_left(r + step, row, step, color, left - 1, skipped=last))
                    moves.update(self._traverse_left(r + step, row, step, color, left + 1, skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            left -= 1

        return moves

    def _traverse_right(self, start, stop, step, color, right, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= COLS:
                break

            current = self.board[r][right]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, right)] = last + skipped
                else:
                    moves[(r, right)] = last

                if last:
                    if step == -1:
                        row = max(r - 3, -1)
                    else:
                        row = min(r + 3, ROWS)
                    moves.update(self._traverse_right(r + step, row, step, color, right - 1, skipped=last))
                    moves.update(self._traverse_right(r + step, row, step, color, right + 1, skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            right += 1

        return moves

    def king_traverse_left(self, start, stop, step, color, left, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:
                break

            current = self.board[r][left]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, left)] = last + skipped
                else:
                    moves[(r, left)] = last + last

                if last:
                    if step == -1:
                        row = max(r - 3, -1)
                    else:
                        row = min(r + 3, ROWS)
                    moves.update(self._traverse_left(r + step, row, step, color, left - 1, skipped=last))
                    moves.update(self._traverse_left(r + step, row, step, color, left + 1, skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            left -= 1

        return moves

    def king_traverse_right(self, start, stop, step, color, right, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= COLS:
                break

            current = self.board[r][right]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, right)] = last + skipped
                else:
                    moves[(r, right)] = last + last

                if last:
                    if step == -1:
                        row = max(r - 3, -1)
                    else:
                        row = min(r + 3, ROWS)
                    moves.update(self._traverse_right(r + step, row, step, color, right - 1, skipped=last))
                    moves.update(self._traverse_right(r + step, row, step, color, right + 1, skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            right += 1

        return moves

    def test_red(self, piece_x, piece_y):
        moves = {}
        i = piece_y
        j = piece_x
        while (True): # ЛевоВерх
            if (i > 7 or j < 0 or j >= 9 or i < 0):
                break
            if (self.board[i][j] != 0 and self.board[i-1][j-1] != 0):
                break
            if self.board[i][j] == 0:
                moves[(i, j)] = self.board[i][j]
            i -= 1
            j -= 1

        i = piece_y
        j = piece_x
        while (True): #ПравоВерх
            if (i > 7 or j <= 0 or j > 9 or i <= 0):
                break
            if (self.board[i][j] != 0  and self.board[i+1][j-1] != 0):
                break
            if self.board[i][j] == 0:
                moves[(i, j)] = self.board[i][j]
            i -= 1
            j += 1


        i = piece_y
        j = piece_x
        while (True): #ЛевоНиз
            if (i >= 7 or j <= 0 or j > 9 or i < 0):
                break
            if (self.board[i][j] != 0 and self.board[i-1][j+1] != 0):
                break
            if self.board[i][j] == 0:
                moves[(i, j)] = self.board[i][j]
            i += 1
            j -= 1


        i = piece_y
        j = piece_x
        while (True): #ПравоНиз
            if (i >= 7 or j <= 0 or j >= 9 or i < 0):
                break
            if (self.board[i][j] != 0 and self.board[i+1][j+1] != 0):
                break
            if self.board[i][j] == 0:
                moves[(i, j)] = self.board[i][j]
            i += 1
            j += 1

        return moves



