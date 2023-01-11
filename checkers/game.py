from .board import *
from minimax.algorithm import *
from copy import deepcopy


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
        self.all_moves = self.board.get_bot_moves(self.turn)

    def draw_valid_moves(self):
        if self.selected:
            for move in self.all_moves[self.selected]:
                row, col = move
                pygame.draw.circle(self.win, GREEN, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), 15)

    def change_turn(self):
        if self.turn == RED:
            self.turn = WHITE
        else:
            self.turn = RED
        self.selected = None
        self.update_moves()

    def minimax(self, position, depth, max_player):
        if depth == 0 or position.winner() != None:
            return position.evaluate(), position

        if max_player:
            maxEval = float('-inf')
            best_move = None
            for move in self.get_all_moves(position, WHITE):
                evaluation = self.minimax(move, depth - 1, False)[0]
                maxEval = max(maxEval, evaluation)
                if maxEval == evaluation:
                    best_move = move

            return maxEval, best_move
        else:
            minEval = float('inf')
            best_move = None
            for move in self.get_all_moves(position, RED):
                evaluation = self.minimax(move, depth - 1, True)[0]
                minEval = min(minEval, evaluation)
                if minEval == evaluation:
                    best_move = move

            return minEval, best_move

    def simulate_move(self, piece, move, board, skip):
        board.move(piece, move[0], move[1])
        if skip:
            board.remove(skip)

        return board

    def get_all_moves(self, board, color):
        moves = []
        for piece in board.get_all_pieces(color):
            valid_moves = board.get_valid_moves(piece)
            for move, skip in valid_moves.items():
                temp_board = deepcopy(board)
                temp_piece = temp_board.get_piece(piece.row, piece.col)
                new_board = self.simulate_move(temp_piece, move, temp_board, skip)
                moves.append(new_board)

        return moves

    def get_board(self):
        return self.board

    def ai_move(self, board):
        self.board = board
        self.change_turn()


