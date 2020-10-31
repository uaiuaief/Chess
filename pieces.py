class Piece:
    def __repr__(self):
        return f'{self.COLOR} {self.NAME}'

    def get_xy_difference(self, origin, target):
        ox, oy = origin
        tx, ty = target

        # print(tx-ox)
        return tx-ox, ty-oy

    def can_move(self, target):
        piece = target.get_piece()

        if piece is None:
            return True
        elif self.COLOR == piece.COLOR:
            return False
        else:
            return True


class Pawn(Piece):
    def __init__(self, color):
        self.COLOR = color
        self.NAME = 'pawn'
        self.first_move = True

    def is_move_allowed(self, pos_now, pos_then, capture):
        ay, ax = pos_now
        by, bx = pos_then

    def get_possible_moves(self, pos_now, grid):
        # White
        possible_moves = []
        ax, ay = pos_now

        current = grid[ay][ax]
        # test
        # grid[ay+1][ax+1].set_piece(Tower('black'))
        # grid[ay-1][ax+1].set_piece(Tower('white'))
        #

        if self.COLOR == 'white':
            cell_above = grid[ay + 1][ax]
            # print('CELL ABOVE ', cell_above, cell_above.POSITION)
            # print('CURRENT CELL ', current, pos_now)
            print()
            for row in grid:
                for cell in row:
                    dx, dy = self.get_xy_difference(pos_now, cell.POSITION)

                    cell_above_is_empty = cell_above.get_piece() is None
                    cell_piece = cell.get_piece()
                    cell_is_empty = cell_piece is None
                    cell_has_enemy = not cell_is_empty and cell_piece.COLOR != self.COLOR
                    can_capture = cell_has_enemy and cell_piece.NAME != 'king'

                    is_one_up = dy == 1
                    is_two_up = dy == 2 and dx == 0
                    is_diagonal = abs(dx) == 1 and is_one_up

                    can_move_one_up = is_one_up and cell_is_empty and dx == 0
                    can_move_diagonal = is_diagonal and can_capture
                    can_move_two_up = self.first_move and is_two_up and cell_is_empty and cell_above_is_empty

                    if can_move_one_up or can_move_diagonal or can_move_two_up:
                        possible_moves.append(cell)
                        # print(cell)

        else:
            cell_below = grid[ay - 1][ax]
            # print('CELL BELOW', cell_below, cell_below.POSITION)
            # print('CURRENT CELL ', current, pos_now)
            # print()
            for row in grid:
                for cell in row:
                    dx, dy = self.get_xy_difference(pos_now, cell.POSITION)

                    cell_below_is_empty = cell_below.get_piece() is None
                    cell_piece = cell.get_piece()
                    cell_is_empty = cell_piece is None
                    cell_has_enemy = not cell_is_empty and cell_piece.COLOR != self.COLOR
                    can_capture = cell_has_enemy and cell_piece.NAME != 'king'

                    is_one_down = dy == -1
                    is_two_down = dy == -2 and dx == 0
                    is_diagonal = abs(dx) == 1 and is_one_down

                    can_move_one_down = is_one_down and cell_is_empty and dx == 0
                    can_move_diagonal = is_diagonal and can_capture
                    can_move_two_down = self.first_move and is_two_down and cell_is_empty and cell_below_is_empty

                    if can_move_one_down or can_move_diagonal or can_move_two_down:
                        # print(cell)
                        possible_moves.append(cell)


        # print(possible_moves)
        return possible_moves


class Rook(Piece):
    def __init__(self, color):
        self.COLOR = color
        self.NAME = 'rook'

    def get_possible_moves(self, pos_now, grid):
        possible_moves = []
        x, y = pos_now

        # print(x, y)
        # Tower upwards movement
        for i in range(y+1, 8):
            square = grid[i][x]
            piece = square.get_piece()
            if self.can_move(target=square) is True:
                possible_moves.append(square)
                if piece:
                    break
            else:
                break

        # Tower downwards movement
        for i in range(y, 0, -1):
            square = grid[i-1][x]
            piece = square.get_piece()
            if self.can_move(target=square) is True:
                possible_moves.append(square)
                if piece:
                    break
            else:
                break

        # Tower right movement
        for i in range(x + 1, 8):
            square = grid[y][i]
            piece = square.get_piece()
            if self.can_move(target=square) is True:
                possible_moves.append(square)
                if piece:
                    break
            else:
                break

        # Tower left movement
        for i in range(x, 0, -1):
            square = grid[y][i-1]
            piece = square.get_piece()
            if self.can_move(target=square) is True:
                possible_moves.append(square)
                if piece:
                    break
            else:
                break
        # print('pos: ', grid[y][x], '\nmoves ', possible_moves)
        return possible_moves


class Knight(Piece):
    def __init__(self, color):
        self.COLOR = color
        self.NAME = 'knight'

    def get_possible_moves(self, pos_now, grid):
        possible_moves = []
        x, y = pos_now

        for row in grid:
            for cell in row:
                diff_x, diff_y = self.get_xy_difference(pos_now, cell.POSITION)
                if abs(diff_x) == 2 and abs(diff_y) == 1 or abs(diff_y) == 2 and abs(diff_x) == 1:
                    if self.can_move(cell):
                        possible_moves.append(cell)

        # print('pos: ', grid[y][x], '\nmoves ', possible_moves)
        return possible_moves


class Bishop(Piece):
    def __init__(self, color):
        self.COLOR = color
        self.NAME = 'bishop'

    def get_possible_moves(self, pos_now, grid):
        possible_moves = []
        x, y = pos_now

        # upper left diagonal
        for i in range(1, 8):
            if 0 <= y+i < 8 and 0 <= x-i < 8:
                square = grid[y+i][x-i]
                piece = square.get_piece()
                if self.can_move(square):
                    possible_moves.append(square)
                if piece:
                    break

        # upper right diagonal
        for i in range(1, 8):
            if 0 <= y + i < 8 and 0 <= x + i < 8:
                square = grid[y + i][x + i]
                piece = square.get_piece()
                if self.can_move(square):
                    possible_moves.append(square)
                if piece:
                    break

        # down left diagonal
        for i in range(1, 8):
            if 0 <= y - i < 8 and 0 <= x - i < 8:
                square = grid[y - i][x - i]
                piece = square.get_piece()
                if self.can_move(square):
                    possible_moves.append(square)
                if piece:
                    break

        # down right diagonal
        for i in range(1, 8):
            if 0 <= y - i < 8 and 0 <= x + i < 8:
                square = grid[y - i][x + i]
                piece = square.get_piece()
                if self.can_move(square):
                    possible_moves.append(square)
                if piece:
                    break

        # print('pos: ', grid[y][x], '\nmoves ', possible_moves)
        return possible_moves


class Queen(Piece):
    def __init__(self, color):
        self.COLOR = color
        self.NAME = 'queen'

    def get_possible_moves(self, pos_now, grid):
        possible_moves = []
        x, y = pos_now

        # print(x, y)
        # Queen upwards movement
        for i in range(y + 1, 8):
            square = grid[i][x]
            piece = square.get_piece()
            if self.can_move(target=square) is True:
                possible_moves.append(square)
                if piece:
                    break
            else:
                break

        # Queen downwards movement
        for i in range(y, 0, -1):
            square = grid[i - 1][x]
            piece = square.get_piece()
            if self.can_move(target=square) is True:
                possible_moves.append(square)
                if piece:
                    break
            else:
                break

        # Queen right movement
        for i in range(x + 1, 8):
            square = grid[y][i]
            piece = square.get_piece()
            if self.can_move(target=square) is True:
                possible_moves.append(square)
                if piece:
                    break
            else:
                break

        # Queen left movement
        for i in range(x, 0, -1):
            square = grid[y][i - 1]
            piece = square.get_piece()
            if self.can_move(target=square) is True:
                possible_moves.append(square)
                if piece:
                    break
            else:
                break

        # upper left diagonal
        for i in range(1, 8):
            if 0 <= y + i < 8 and 0 <= x - i < 8:
                square = grid[y + i][x - i]
                piece = square.get_piece()
                if self.can_move(square):
                    possible_moves.append(square)
                if piece:
                    break

        # upper right diagonal
        for i in range(1, 8):
            if 0 <= y + i < 8 and 0 <= x + i < 8:
                square = grid[y + i][x + i]
                piece = square.get_piece()
                if self.can_move(square):
                    possible_moves.append(square)
                if piece:
                    break

        # down left diagonal
        for i in range(1, 8):
            if 0 <= y - i < 8 and 0 <= x - i < 8:
                square = grid[y - i][x - i]
                piece = square.get_piece()
                if self.can_move(square):
                    possible_moves.append(square)
                if piece:
                    break

        # down right diagonal
        for i in range(1, 8):
            if 0 <= y - i < 8 and 0 <= x + i < 8:
                square = grid[y - i][x + i]
                piece = square.get_piece()
                if self.can_move(square):
                    possible_moves.append(square)
                if piece:
                    break

        # print('pos: ', grid[y][x], '\nmoves ', possible_moves)
        return possible_moves


class King(Piece):
    def __init__(self, color):
        self.COLOR = color
        self.NAME = 'king'

    def get_possible_moves(self, pos_now, grid):
        possible_moves = []
        x, y = pos_now
        # x,y = 4, 3

        for row in grid:
            for cell in row:
                diff_x, diff_y = self.get_xy_difference(pos_now, cell.POSITION)
                if abs(diff_x) <= 1 and abs(diff_y) <= 1:
                    if self.can_move(cell):
                        possible_moves.append(cell)

        # print('pos: ', grid[y][x], '\nmoves ', possible_moves)
        return possible_moves






