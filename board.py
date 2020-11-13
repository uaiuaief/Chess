from pieces import *

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
        self.players = {'one': None, 'two': None}
        self.turn_count = 1
        self.pieces = []
        self.turn = 'white'
        self.king = {}
        self.moves = {}
        self._setup_pieces()

    def get_piece(self, x, y):
        for piece in self.pieces:
            if piece.x == x and piece.y == y:
                return piece

    def move(self, origin_cell, target_cell, player):
        x1, y1 = origin_cell
        x2, y2 = target_cell
        origin_piece = self.get_piece(x=x1, y=y1)
        target_piece = self.get_piece(x=x2, y=y2)

        move_is_allowed = (target_cell in origin_piece.moves) if origin_piece.moves else None
        print(player.ip, player.color)
        is_your_turn = self.turn == origin_piece.COLOR == player.color
        if move_is_allowed and is_your_turn:
            self.remove_en_passant_tag()
            origin_piece.move(x2, y2)
            self.change_turn()
            self.update_board()

        else:
            raise ValueError('Movement Not allowed')

    def remove_en_passant_tag(self):
        for piece in self.pieces:
            if piece.NAME == 'pawn':
                piece.en_passant = False

    def change_turn(self):
        self.turn_count += 1
        if self.turn == 'white':
            self.turn = 'black'
        else:
            self.turn = 'white'

    def _setup_pieces(self):

        for i in range(8):
            pass
            self.pieces.append(Pawn('black', x=i, y=1, board=self))
            self.pieces.append(Pawn('white', x=i, y=6, board=self))

        ''' Blacks '''
        self.pieces.append(Rook('black', y=0, x=0, board=self))
        self.pieces.append(Rook('black', y=0, x=7, board=self))
        self.pieces.append(Knight('black', y=0, x=1, board=self))
        self.pieces.append(Knight('black', y=0, x=6, board=self))
        self.pieces.append(Bishop('black', y=0, x=2, board=self))
        self.pieces.append(Bishop('black', y=0, x=5, board=self))
        self.pieces.append(Queen('black', y=0, x=3, board=self))
        self.king['black'] = King('black', y=0, x=4, board=self)
        self.pieces.append(self.king['black'])

        ''' Whites '''
        self.pieces.append(Rook('white', y=7, x=0, board=self))
        self.pieces.append(Rook('white', y=7, x=7, board=self))
        self.pieces.append(Knight('white', y=7, x=1, board=self))
        self.pieces.append(Knight('white', y=7, x=6, board=self))
        self.pieces.append(Bishop('white', y=7, x=2, board=self))
        self.pieces.append(Bishop('white', y=7, x=5, board=self))
        self.pieces.append(Queen('white', y=7, x=3, board=self))

        self.king['white'] = King('white', y=7, x=4, board=self)
        self.pieces.append(self.king['white'])

    def update_board(self):
        self.king['white'].get_moves()
        self.king['black'].get_moves()
        for piece in self.pieces:
            if piece.NAME != 'king':
                piece.get_moves()

    def get_state(self):
        self.update_board()
        state = []
        for piece in self.pieces:
            moves = piece.moves

            index_list = []
            if moves:
                for each in moves:
                    x, y = each
                    index_list.append({'x': x, 'y': y})

            piece_attributes = {
                'color': piece.COLOR,
                'name': piece.NAME,
                'x': piece.x,
                'y': piece.y,
                'moves': index_list,
            }
            state.append(piece_attributes)
        return state

    def reset_board(self):
        self.pieces = []
        self._setup_pieces()
        self.turn = 'white'
        self.turn_count = 1

    def check_mate(self):
        colors = ['white', 'black']

        for color in colors:
            moves = []
            for piece in self.pieces:
                if piece.COLOR == color and piece.moves:
                    for m in piece.moves:
                        moves.append(m)
            if not moves:
                winner = 'white' if color == 'black' else 'black'
                return True, winner
        return False, None




b = Board()
# for each in b.pieces:
#     print(each.x, each.y)


# print(b.get_piece(0, 0).moves(b))


# print(b.get_state())


# print(convert_to_index('C1'))
# y, x = convert_to_index('b4')
# print(b.GRID[x][y])

