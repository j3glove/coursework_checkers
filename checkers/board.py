from checkers.piece import *



class Board:
    def __init__(self):
        self.board = []
        self.red_left = self.white_left = 15
        self.red_kings = self.white_kings = 0
        self.create_board()

    def draw_squares(self, win):
        win.fill(BLACK)
        for row in range(ROWS):
            for col in range(COLS):
                if (row + col)%2 == 0:
                    pygame.draw.rect(win, RED, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def evaluate(self):
        k=5
        ves_pos = self.white_left - self.red_left + (self.white_kings * k - self.red_kings * k)
        evalpos = -ves_pos
        return evalpos

    def get_all_pieces(self, color):
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color == color:
                    pieces.append(piece)
        return pieces

    def move(self, piece, row, col):
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)

        if row == ROWS - 1 and piece.color == WHITE or row == 0 and piece.color == RED:
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
        moves.update(self.check_pos_right_upside(piece, piece.col, piece.row))
        moves.update(self.check_pos_left_upside(piece, piece.col, piece.row))
        moves.update(self.check_pos_left_bottom(piece, piece.col, piece.row))
        moves.update(self.check_pos_right_bottom(piece, piece.col, piece.row))

        if piece.king:
            moves.update(self.test_red(piece, piece.col, piece.row))

        return moves

    def get_bot_moves(self, turn):
        can_kill = False
        all_moves ={}
        for y in range(8):
            for x in range(10):
                piece = self.get_figure_at(x, y)
                if piece and piece.color == turn:
                    moves = self.get_valid_moves(piece)
                    all_moves[piece] = moves
                    for move in moves:
                        if moves[move]:
                            can_kill = True

        if can_kill:
            result = {}
            for piece in all_moves:
                result[piece] = {}
                for move in all_moves[piece]:
                    if all_moves[piece][move]:
                        result[piece][move] = all_moves[piece][move]
            all_moves = result
        return all_moves

    def check_pos_right_bottom(self, piece, piece_x, piece_y):
        moves = {}
        y = piece_y
        x = piece_x
        dx = 1
        dy = 1
        if self.get_figure_at(x + dx, y + dy) == 0 and piece.color == WHITE:
            moves[(y + dy, x + dx)] = self.get_figure_at(x + dx, y + dy)
        if self.get_figure_at(x + dx * 2, y + dy * 2) == 0 and isinstance(self.get_figure_at(x + dx, y + dy), Piece) and self.get_figure_at(x + dx, y + dy).color != piece.color:
            moves[(y + dy * 2, x + dx * 2)] = self.get_figure_at(x + dx, y + dy)
        return moves

    def check_pos_right_upside(self, piece, piece_x, piece_y):
        moves = {}
        y = piece_y
        x = piece_x
        dx = 1
        dy = -1
        if self.get_figure_at(x + dx, y + dy) == 0 and piece.color == RED:
            moves[(y + dy, x + dx)] = self.get_figure_at(x + dx, y + dy)
        if self.get_figure_at(x + dx * 2, y + dy * 2) == 0 and isinstance(self.get_figure_at(x + dx, y + dy), Piece) and self.get_figure_at(x + dx, y + dy).color != piece.color:
            moves[(y + dy * 2, x + dx * 2)] = self.get_figure_at(x + dx, y + dy)
        return moves

    def check_pos_left_bottom(self, piece, piece_x, piece_y):
        moves = {}
        y = piece_y
        x = piece_x
        dx = -1
        dy = 1
        if self.get_figure_at(x + dx, y + dy) == 0 and piece.color == WHITE:
            moves[(y + dy, x + dx)] = self.get_figure_at(x + dx, y + dy)
        if self.get_figure_at(x + dx * 2, y + dy * 2) == 0 and isinstance(self.get_figure_at(x + dx, y + dy), Piece) and self.get_figure_at(x + dx, y + dy).color != piece.color:
            moves[(y + dy * 2, x + dx * 2)] = self.get_figure_at(x + dx, y + dy)
        return moves

    def check_pos_left_upside(self, piece, piece_x, piece_y):
        moves = {}
        y = piece_y
        x = piece_x
        dx = -1
        dy = -1
        if self.get_figure_at(x + dx, y + dy) == 0 and piece.color == RED:
            moves[(y + dy, x + dx)] = self.get_figure_at(x + dx, y + dy)
        if self.get_figure_at(x + dx * 2, y + dy * 2) == 0 and isinstance(self.get_figure_at(x + dx, y + dy), Piece) and self.get_figure_at(x + dx, y + dy).color != piece.color:
            moves[(y + dy * 2, x + dx * 2)] = self.get_figure_at(x + dx, y + dy)
        return moves

    def test_red(self, piece, piece_x, piece_y):
        moves = {}
        y = piece_y
        x = piece_x

        dx = 0
        dy = 0
        king_dx = 1
        king_dy = 1
        while True:
            dx += king_dx
            dy += king_dy
            if self.get_figure_at(x + dx, y + dy) == 0:
                moves[(y + dy, x + dx)] = self.get_figure_at(x + dx, y + dy)
            else:
                if self.get_figure_at(x + dx + king_dx, y + dy + king_dy) != 0 or piece.color == self.get_figure_at(x + dx,y + dy).color:
                    break
                if self.get_figure_at(x + dx, y + dy) != 0 and piece.color != self.get_figure_at(x + dx, y + dy).color and self.get_figure_at(x + dx + king_dx, y + dy + king_dy) == 0:
                    moves[(y + dy + king_dy, x + dx + king_dx)] = self.get_figure_at(x + dx, y + dy)
                    eated_piece = self.get_figure_at(x + dx, y + dy)
                    while True:
                        dx += king_dx
                        dy += king_dy
                        if self.get_figure_at(x + dx, y + dy) != 0:
                            break
                        moves[(y + dy, x + dx)] = eated_piece
                    break

        dx = 0
        dy = 0
        king_dx = -1
        king_dy = 1
        while True:
            dx += king_dx
            dy += king_dy
            if self.get_figure_at(x + dx, y + dy) == 0:
                moves[(y + dy, x + dx)] = self.get_figure_at(x + dx, y + dy)
            else:
                if self.get_figure_at(x + dx + king_dx, y + dy + king_dy) != 0 or piece.color == self.get_figure_at(x + dx,y + dy).color:
                    break
                if self.get_figure_at(x + dx, y + dy) != 0 and piece.color != self.get_figure_at(x + dx, y + dy).color and self.get_figure_at(x + dx + king_dx, y + dy + king_dy) == 0:
                    moves[(y + dy + king_dy, x + dx + king_dx)] = self.get_figure_at(x + dx, y + dy)
                    eated_piece = self.get_figure_at(x + dx, y + dy)
                    while True:
                        dx += king_dx
                        dy += king_dy
                        if self.get_figure_at(x + dx, y + dy) != 0:
                            break
                        moves[(y + dy, x + dx)] = eated_piece
                    break

        dx = 0
        dy = 0
        king_dx = 1
        king_dy = -1
        while True:
            dx += king_dx
            dy += king_dy
            if self.get_figure_at(x + dx, y + dy) == 0:
                moves[(y + dy, x + dx)] = self.get_figure_at(x + dx, y + dy)
            else:
                if self.get_figure_at(x + dx + king_dx, y + dy + king_dy) != 0 or piece.color == self.get_figure_at(x + dx,y + dy).color:
                    break
                if self.get_figure_at(x + dx, y + dy) != 0 and piece.color != self.get_figure_at(x + dx, y + dy).color and self.get_figure_at(x + dx + king_dx, y + dy + king_dy) == 0:
                    moves[(y + dy + king_dy, x + dx + king_dx)] = self.get_figure_at(x + dx, y + dy)
                    eated_piece = self.get_figure_at(x + dx, y + dy)
                    while True:
                        dx += king_dx
                        dy += king_dy
                        if self.get_figure_at(x + dx, y + dy) != 0:
                            break
                        moves[(y + dy, x + dx)] = eated_piece
                    break

        dx = 0
        dy = 0
        king_dx = -1
        king_dy = -1
        while True:
            dx += king_dx
            dy += king_dy
            if self.get_figure_at(x + dx, y + dy) == 0:
                moves[(y + dy, x + dx)] = self.get_figure_at(x + dx, y + dy)
            else:
                if self.get_figure_at(x + dx + king_dx, y + dy + king_dy) != 0 or piece.color == self.get_figure_at(x + dx,y + dy).color:
                    break
                if self.get_figure_at(x + dx, y + dy) != 0 and piece.color != self.get_figure_at(x + dx, y + dy).color and self.get_figure_at(x + dx + king_dx, y + dy + king_dy) == 0:
                    moves[(y + dy + king_dy, x + dx + king_dx)] = self.get_figure_at(x + dx, y + dy)
                    eated_piece = self.get_figure_at(x + dx, y + dy)
                    while True:
                        dx += king_dx
                        dy += king_dy
                        if self.get_figure_at(x + dx, y + dy) != 0:
                            break
                        moves[(y + dy, x + dx)] = eated_piece
                    break

        return moves
