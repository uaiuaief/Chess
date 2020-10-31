from pieces import *


# class Screen:
#     pass
CHAR_REP = {
    'a': 0, 'b': 1, 'c': 2, 'd': 3,
    'e': 4, 'f': 5, 'g': 6, 'h': 7,

    '0': 'a', '1': 'b', '2': 'c', '3': 'd',
    '4': 'e', '5': 'f', '6': 'g', '7': 'h',
}


def convert_to_index(entry):
    char, num = list(entry)
    row = int(num)-1
    column = CHAR_REP[char.lower()]

    return column, row


class Board:
    def __init__(self):
        self.GRID = self.init_grid()
        self.init_board()
        self.turn = 'white'
        # self.pieces

    def get_piece(self, i, j):
        piece = self.GRID[j][i].get_piece()
        return piece

    def move(self, origin_cell, target_cell):
        # x1, y1 = convert_to_index(origin_cell)
        # x2, y2 = convert_to_index(target_cell)

        x1, y1 = origin_cell
        x2, y2 = target_cell

        sqr_one = self.GRID[y1][x1]
        sqr_two = self.GRID[y2][x2]

        sqr1_piece = sqr_one.get_piece()

        possible_moves = sqr1_piece.get_possible_moves((x1, y1), self.GRID)

        move_is_allowed = sqr_two in possible_moves
        # is_your_turn = sqr1_piece.COLOR == self.turn
        is_your_turn = True
        if move_is_allowed and is_your_turn:
            sqr_one.set_piece(None)
            sqr_two.set_piece(sqr1_piece)
            sqr1_piece.first_move = False
            self.change_turn()

        else:
            raise ValueError('Movement Not allowed')

    def change_turn(self):
        if self.turn == 'white':

            self.turn = 'black'
        else:
            self.turn = 'white'

    def init_board(self):
        self._setup_pieces()

    def _setup_pieces(self):
        for i in range(8):
            self.GRID[1][i].set_piece(Pawn('white'))
            self.GRID[6][i].set_piece(Pawn('black'))

        ''' Whites '''
        self.GRID[0][0].set_piece(Rook('white'))
        self.GRID[0][7].set_piece(Rook('white'))
        self.GRID[0][1].set_piece(Knight('white'))
        self.GRID[0][6].set_piece(Knight('white'))
        self.GRID[0][2].set_piece(Bishop('white'))
        self.GRID[0][5].set_piece(Bishop('white'))
        self.GRID[0][3].set_piece(Queen('white'))
        self.GRID[0][4].set_piece(King('white'))

        ''' Blacks '''
        self.GRID[7][0].set_piece(Rook('black'))
        self.GRID[7][7].set_piece(Rook('black'))
        self.GRID[7][1].set_piece(Knight('black'))
        self.GRID[7][6].set_piece(Knight('black'))
        self.GRID[7][2].set_piece(Bishop('black'))
        self.GRID[7][5].set_piece(Bishop('black'))
        self.GRID[7][3].set_piece(Queen('black'))
        self.GRID[7][4].set_piece(King('black'))

    @staticmethod
    def init_grid():
        grid = []
        for x in range(8):
            column = []
            for y in range(8):
                column.append(Square(y, x))
            grid.append(column)

        return grid

    def get_state(self):
        state = []
        for row in self.GRID:
            for square in row:
                piece = square.get_piece()
                if piece:

                    pos_now = square.POSITION
                    moves = piece.get_possible_moves(pos_now, self.GRID)
                    index_list = []
                    # print(moves)
                    if moves:
                        for each in moves:
                            x, y = each.POSITION
                            index_list.append({'x': x, 'y': y})

                    piece_attributes = {
                        'color': piece.COLOR,
                        'name': piece.NAME,
                        'x': square.POSITION[0],
                        'y': square.POSITION[1],
                        'moves': index_list,
                    }
                    state.append(piece_attributes)
        return state

    def reset_board(self):
        self.GRID = self.init_grid()
        self.init_board()
        self.turn = 'white'


class Square:
    def __init__(self, x, y):
        self.POSITION = (x, y)
        self._piece = None

    def __repr__(self):
        x, y = self.POSITION
        pos_rep = f'{CHAR_REP[str(x)]}{y+1}'

        return f'{pos_rep} - {self._piece}'
        # return f'{self.POSITION}'

    def get_piece(self):
        return self._piece

    def set_piece(self, piece):
        self._piece = piece



# class Player:
#     pass


# b = Board()
# b.get_state()


# print(convert_to_index('C1'))
# y, x = convert_to_index('b4')
# print(b.GRID[x][y])

