from copy import deepcopy
from checkers.board import *
import pygame

RED = (255, 0, 0)
WHITE = (255, 255, 255)

class Algorithm:
    def _init(self, board):
        self.selected = None
        self.board = board
        self.turn = RED
        self.all_moves = {}
        self.update_moves()

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
                if piece and piece.color == WHITE:
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

    def change_turn(self):
        if self.turn == RED:
            self.turn = WHITE
        else:
            self.turn = RED
        self.selected = None
        self.update_moves()

    def minimax(self, position, depth, max_player, game):
        if depth == 0 or position.winner() != None:
            return position.evaluate(), position

        if max_player:
            maxEval = float('-inf')
            best_move = None
            for move in self.get_all_moves(position, WHITE, game):
                evaluation = self.minimax(move, depth - 1, False, game)[0]
                maxEval = max(maxEval, evaluation)
                if maxEval == evaluation:
                    best_move = move

            return maxEval, best_move
        else:
            minEval = float('inf')
            best_move = None
            for move in self.get_all_moves(position, RED, game):
                evaluation = self.minimax(move, depth - 1, True, game)[0]
                minEval = min(minEval, evaluation)
                if minEval == evaluation:
                    best_move = move

            return minEval, best_move


    def simulate_move(self, piece, move, board, game, skip):
        piece1 = board.get_piece(piece.row, piece.col)
        if piece1 != 0 and piece1.color == self.turn:
            self.selected = piece1
        if self.selected:
            result = self._move(piece1.row, piece1.col)
            if not result:
                self.selected = None
                self.select(piece1.row, piece1.col)
        board.move(piece, move[0], move[1])
        if skip:
            board.remove(skip)

        return board


    def get_all_moves(self, board, color, game):
        moves = []
        for piece in board.get_all_pieces(color):
            valid_moves = board.get_valid_moves(piece)
            for move, skip in valid_moves.items():
                temp_board = deepcopy(board)
                temp_piece = temp_board.get_piece(piece.row, piece.col)
                new_board = self.simulate_move(temp_piece, move, temp_board, game, skip)
                moves.append(new_board)

        return moves


