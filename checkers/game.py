from .board import *


class Game:
    def __init__(self, win):
        self._init()
        self.win = win

    def update(self):
        self.board.draw(self.win)
        self.draw_valid_moves()
        pygame.display.update()

    def _init(self):
        self.selected = None
        self.board = Board()
        self.turn = RED
        self.all_moves = {}
        self.update_moves()

    def winner(self):
        return self.board.winner()

    def reset(self):
        self._init()

    def select(self, piece_x, piece_y):
        if self.selected:
            result = self._move(piece_x, piece_y)
            if not result:
                self.selected = None
                self.select(piece_x, piece_y)

        piece = self.board.get_piece(piece_x, piece_y)
        if piece != 0 and piece.color == self.turn:
            self.selected = piece
            return True

        return False

    def _move(self, row, col):
        piece = self.board.get_piece(row, col)
        if self.selected and piece == 0 and (row, col) in self.all_moves[self.selected]:
            self.board.move(self.selected, row, col)
            skipped = self.all_moves[self.selected][(row, col)]
            if skipped:
                self.board.remove(skipped)

                piece = self.board.get_piece(row, col)
                result = {}
                new_moves = self.board.get_valid_moves(piece)
                for move in new_moves:
                    if new_moves[move]:
                        result[move] = new_moves[move]
                if result:
                    for board_piece in self.all_moves:
                        if board_piece != piece:
                            self.all_moves[board_piece] = {}
                        else:
                            self.all_moves[board_piece] = result
                    return True

            self.change_turn()
        else:
            return False

        return True

    def update_moves(self):
        can_kill = False
        for y in range(8):
            for x in range(10):
                piece = self.board.get_figure_at(x, y)
                if piece and piece.color == self.turn:
                    moves = self.board.get_valid_moves(piece)
                    self.all_moves[piece] = moves
                    for move in moves:
                        if moves[move]:
                            can_kill = True

        if can_kill:
            result = {}
            for piece in self.all_moves:
                result[piece] = {}
                for move in self.all_moves[piece]:
                    if self.all_moves[piece][move]:
                        result[piece][move] = self.all_moves[piece][move]
            self.all_moves = result

    def draw_valid_moves(self):
        if self.selected:
            for move in self.all_moves[self.selected]:
                row, col = move
                pygame.draw.circle(self.win, GREEN,
                                   (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), 15)

    def change_turn(self):
        if self.turn == RED:
            self.turn = WHITE
        else:
            self.turn = RED
        self.selected = None
        self.update_moves()
