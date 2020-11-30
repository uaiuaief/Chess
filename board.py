from pieces import *
from sunfish import ai_make_move, api_move, ai

CHAR_REP = {
    'a': 0, 'b': 1, 'c': 2, 'd': 3,
    'e': 4, 'f': 5, 'g': 6, 'h': 7,

    '0': 'a', '1': 'b', '2': 'c', '3': 'd',
    '4': 'e', '5': 'f', '6': 'g', '7': 'h',
}


def index_to_chess_notation(entry):
    x, y = entry
    column = CHAR_REP[str(x)]
    row = 8 - int(y)

    notation = f'{column}{str(row)}'
    print(notation)
    return notation


def convert_to_index(entry):
    char, num = list(entry)
    row = int(num)-1
    row = 7 - row
    column = CHAR_REP[char.lower()]

    return column, row


class BoardInfo:
    def __init__(self, board):
        self.board = board
        self.players = []
        self.current_turn = 'white'
        self.turn_count = 1
        self.move_count = 1
        self.move_history = {}
        self.last_movement = None
        self.last_movement_capture = False
        self.last_movement_castle = False
        self.check = False
        self.winner = None
        self.check_mate = False
        self.game_over = True
        self.resignation = False
        self.game_started = False
        self.time_up = False
        self.clock_is_running = False
        self.timer = {}
        self.captured_pieces = []
        self.against_computer = False

    def get_state(self):
        state = {
            'players': self.players,
            'current_turn': self.current_turn,
            'turn_count': self.turn_count,
            'move_count': self.move_count,
            'move_history': self.move_history,
            'last_movement': self.last_movement,
            'last_movement_capture': self.last_movement_capture,
            'last_movement_castle': self.last_movement_castle,
            'check': self.check,
            'check_mate': self.check_mate,
            'winner': self.winner,
            'game_over': self.game_over,
            'resignation': self.resignation,
            'game_started': self.game_started,
            'time_up': self.time_up,
            'clock_is_running': self.clock_is_running,
            'timer': {
                'white': self.timer['white'],
                'black': self.timer['black']
            },
            'captured_pieces': self.captured_pieces,
            'against_computer': self.against_computer,
        }
        return state

    def reset(self):
        self.current_turn = 'white'
        self.turn_count = 1
        self.move_count = 1
        self.move_history = {}
        self.last_movement = None
        self.last_movement_capture = False
        self.check = False
        self.winner = None
        self.check_mate = False
        self.game_over = True
        self.resignation = False
        self.game_started = False
        self.time_up = False
        self.captured_pieces = []
        self.against_computer = False


class BoardEvents:
    def __init__(self, board):
        self.board = board

    def promote_pawn(self, x, y, promotion):
        piece = self.board.get_piece(x, y)
        if not piece:
            raise ValueError('No piece to promote')
        elif piece.NAME != 'pawn':
            raise ValueError("Piece is not a pawn")
        elif piece.promotion:
            self.board.pieces.remove(piece)
            if promotion == 'queen':
                self.board.pieces.append(Queen(piece.COLOR, x, y, self.board))
            elif promotion == 'rook':
                self.board.pieces.append(Rook(piece.COLOR, x, y, self.board))
            elif promotion == 'bishop':
                self.board.pieces.append(Bishop(piece.COLOR, x, y, self.board))
            elif promotion == 'knight':
                self.board.pieces.append(Knight(piece.COLOR, x, y, self.board))
            else:
                raise ValueError('Piece name is not valid')

        else:
            raise ValueError("Piece can't be promoted")

    def move(self, origin_cell, target_cell, player):
        if not self.board.info.game_started:
            raise ValueError("Can't move before the game has started")

        x1, y1 = origin_cell
        x2, y2 = target_cell
        origin_piece = self.board.get_piece(x=x1, y=y1)
        target_piece = self.board.get_piece(x=x2, y=y2)

        if origin_piece is None:
            raise ValueError('No piece to move')

        move_is_allowed = (target_cell in origin_piece.moves) if origin_piece.moves else None
        if not move_is_allowed:
            raise ValueError('Movement is Not Allowed')

        # print(player.ip, player.color)

        if self.board.info.against_computer:
            if player != 'computer':
                is_your_turn = self.board.info.current_turn == origin_piece.COLOR == 'white'
            else:
                is_your_turn = True
        else:
            # is_your_turn = self.board.info.current_turn == origin_piece.COLOR
            is_your_turn = self.board.info.current_turn == origin_piece.COLOR == player.color
            # is_your_turn = True

        if not is_your_turn:
            raise ValueError("Can't move outside your turn")

        self.remove_en_passant_tag()
        if target_piece:
            self.board.info.captured_pieces.append({'color': target_piece.COLOR, 'name': target_piece.NAME})
        origin_piece.move(x2, y2)

        self.change_turn()
        self.board.update_board()
        self.board.update_move_history(origin_cell, origin_piece, target_cell, target_piece)

        self.board.info.last_movement_capture = True if target_piece else False
        castle = origin_piece.NAME == 'king' and abs(x1 - x2) == 2
        self.board.info.last_movement_castle = True if castle else False
        self.board.info.last_movement = [[x1, y1], [x2, y2]]

        if self.board.info.against_computer and self.board.info.current_turn == 'black':
            api_move([x1, y1, x2, y2])
            ai_make_move(self.board, 'computer')

    def remove_en_passant_tag(self):
        for piece in self.board.pieces:
            if piece.NAME == 'pawn':
                piece.en_passant = False

    def change_turn(self):
        self.board.info.move_count += 1

        if self.board.info.current_turn == 'white':
            self.board.info.current_turn = 'black'
        else:
            self.board.info.turn_count += 1
            self.board.info.current_turn = 'white'


class Board:
    def __init__(self):
        self.info = BoardInfo(self)
        self.events = BoardEvents(self)

        self.pieces = []
        self.king = {}
        self._setup_pieces()
        self.set_timer()

    def set_timer(self, minutes=15):
        self.info.timer['white'] = minutes * 60
        self.info.timer['black'] = minutes * 60

    def get_piece(self, x, y):
        for piece in self.pieces:
            if piece.x == x and piece.y == y:
                return piece

    def index_to_chess_notation(self, origin_cell, target_cell, origin_piece, target_piece):
        """ Don't use origin_piece or target_piece x and y position directly,
        their positions are already updated when this function is called """

        ox, oy = origin_cell[0], origin_cell[1]
        tx, ty = target_cell[0], target_cell[1]

        if origin_piece.COLOR == 'white':
            if origin_piece.NAME == 'knight':
                movement = '&#9822;'
            elif origin_piece.NAME == 'bishop':
                movement = '&#9821;'
            elif origin_piece.NAME == 'queen':
                movement = '&#9819;'
            elif origin_piece.NAME == 'rook':
                movement = '&#9820;'
            elif origin_piece.NAME == 'king':
                movement = '&#9818;'
            else:
                movement = ''
        else:
            if origin_piece.NAME == 'knight':
                movement = '&#9816;'
            elif origin_piece.NAME == 'bishop':
                movement = '&#9815;'
            elif origin_piece.NAME == 'queen':
                movement = '&#9813;'
            elif origin_piece.NAME == 'rook':
                movement = '&#9814;'
            elif origin_piece.NAME == 'king':
                movement = '&#9812;'
            else:
                movement = ''

        column = CHAR_REP[str(tx)]
        row = 8 - ty
        if target_piece:
            if origin_piece.NAME == 'pawn':
                movement += CHAR_REP[str(ox)]
            movement += 'x'

        if self.there_is_check():
            movement += '+'

        movement += column
        movement += str(row)

        castle_king = castle_queen = False
        if origin_piece.NAME == 'king' and origin_piece.COLOR == 'white':
            castle_queen = ox - tx == 2
            castle_king = ox - tx == -2
        elif origin_piece.NAME == 'king' and origin_piece.COLOR == 'black':
            castle_queen = ox - tx == 2
            castle_king = ox - tx == -2

        if castle_king:
            movement = 'O-O'
        elif castle_queen:
            movement = 'O-O-O'

        if self.info.check_mate:
            movement += '#'

        elif self.info.check:
            movement += '+'

        return movement

    def update_move_history(self, origin_cell, origin_piece, target_cell, target_piece):
        # entry = self.index_to_chess_notation(origin_piece, target_cell)
        entry = self.index_to_chess_notation(origin_cell, target_cell, origin_piece, target_piece)
        if origin_piece.COLOR == 'white':
            self.info.move_history[self.info.turn_count] = {'white': entry}
        else:
            self.info.move_history[self.info.turn_count-1][origin_piece.COLOR] = entry

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

    def there_is_check(self):
        if self.king['white'].check:
            self.info.check = 'white'
        elif self.king['black'].check:
            self.info.check = 'black'
        else:
            self.info.check = False

    def update_board(self):
        self.king['white'].get_moves()
        self.king['black'].get_moves()
        for piece in self.pieces:
            if piece.NAME != 'king':
                piece.get_moves()

        self.there_is_check()
        self.check_mate()

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
        self.info.reset()
        self.pieces = []
        self._setup_pieces()
        ai.reset_ai()

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
                self.info.game_over = True
                self.info.game_started = False
                self.info.check_mate = True
                self.info.winner = winner




# b = Board()
# for each in b.pieces:
#     print(each.x, each.y)


# print(b.get_piece(0, 0).moves(b))


# print(b.get_state())


# print(convert_to_index('C1'))
# y, x = convert_to_index('b4')
# print(b.GRID[x][y])

