import datetime, time
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


class BoardInfo:
    def __init__(self, board):
        self.board = board
        self.players = {'one': None, 'two': None}
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
        self.time_up = False
        self.clock_is_running = False
        self.timer = {}

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
            'time_up': self.time_up,
            'clock_is_running': self.clock_is_running,
            'timer': {
                'white': self.timer['white'],
                'black': self.timer['black']
            },
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
        self.time_up = False
        self.clock_is_running = False
        self.timer = {}


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
        x1, y1 = origin_cell
        x2, y2 = target_cell
        origin_piece = self.board.get_piece(x=x1, y=y1)
        target_piece = self.board.get_piece(x=x2, y=y2)

        if origin_piece is None:
            return

        move_is_allowed = (target_cell in origin_piece.moves) if origin_piece.moves else None
        print(player.ip, player.color)
        # is_your_turn = self.board.info.current_turn == origin_piece.COLOR == player.color
        is_your_turn = self.board.info.current_turn == origin_piece.COLOR
        # is_your_turn = True
        if move_is_allowed and is_your_turn:
            self.board.remove_en_passant_tag()
            self.board.update_move_history(origin_piece, target_cell)
            origin_piece.move(x2, y2)
            self.board.change_turn()
            self.board.update_board()

            self.board.info.last_movement_capture = True if target_piece else False
            castle = origin_piece.NAME == 'king' and abs(x1 - x2) == 2
            self.board.info.last_movement_castle = True if castle else False

            if self.board.info.check_mate:
                winner = self.board.info.winner
                if winner == 'white':
                    self.board.info.move_history[self.board.info.turn_count][winner] += '#'
                elif winner == 'black':
                    self.board.info.move_history[self.board.info.turn_count-1][winner] += '#'

            elif self.board.king['black'].check:
                self.board.info.move_history[self.board.info.turn_count]['white'] += '+'
            elif self.board.king['white'].check:
                self.board.info.move_history[self.board.info.turn_count-1]['black'] += '+'
            self.board.info.last_movement = [[x1, y1], [x2, y2]]

        else:
            raise ValueError('Movement Not allowed')


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

    # def move(self, origin_cell, target_cell, player):
    #     x1, y1 = origin_cell
    #     x2, y2 = target_cell
    #     origin_piece = self.get_piece(x=x1, y=y1)
    #     target_piece = self.get_piece(x=x2, y=y2)
    #
    #     if origin_piece is None:
    #         return
    #
    #     move_is_allowed = (target_cell in origin_piece.moves) if origin_piece.moves else None
    #     print(player.ip, player.color)
    #     # is_your_turn = self.info.current_turn == origin_piece.COLOR == player.color
    #     is_your_turn = self.info.current_turn == origin_piece.COLOR
    #     # is_your_turn = True
    #     if move_is_allowed and is_your_turn:
    #         self.remove_en_passant_tag()
    #         self.update_move_history(origin_piece, target_cell)
    #         origin_piece.move(x2, y2)
    #         self.change_turn()
    #         self.update_board()
    #
    #         self.info.last_movement_capture = True if target_piece else False
    #         castle = origin_piece.NAME == 'king' and abs(x1 - x2) == 2
    #         self.info.last_movement_castle = True if castle else False
    #
    #         if self.info.check_mate:
    #             winner = self.info.winner
    #             if winner == 'white':
    #                 self.info.move_history[self.info.turn_count][winner] += '#'
    #             elif winner == 'black':
    #                 self.info.move_history[self.info.turn_count-1][winner] += '#'
    #
    #         elif self.king['black'].check:
    #             self.info.move_history[self.info.turn_count]['white'] += '+'
    #         elif self.king['white'].check:
    #             self.info.move_history[self.info.turn_count-1]['black'] += '+'
    #         self.info.last_movement = [[x1, y1], [x2, y2]]
    #
    #     else:
    #         raise ValueError('Movement Not allowed')

    def index_to_chess_notation(self, piece, target):
        movement = ''
        # print(piece.x, target[0])
        # movement = piece.NAME[0]

        if piece.COLOR == 'white':
            if piece.NAME == 'knight':
                movement = '&#9822;'
            elif piece.NAME == 'bishop':
                movement = '&#9821;'
            elif piece.NAME == 'queen':
                movement = '&#9819;'
            elif piece.NAME == 'rook':
                movement = '&#9820;'
            elif piece.NAME == 'king':
                movement = '&#9818;'
            else:
                movement = ''
        else:
            if piece.NAME == 'knight':
                movement = '&#9816;'
            elif piece.NAME == 'bishop':
                movement = '&#9815;'
            elif piece.NAME == 'queen':
                movement = '&#9813;'
            elif piece.NAME == 'rook':
                movement = '&#9814;'
            elif piece.NAME == 'king':
                movement = '&#9812;'
            else:
                movement = ''

        x, y = target
        enemy_piece = self.get_piece(x, y)
        column = CHAR_REP[str(x)]
        row = 8 - y
        if enemy_piece:
            if piece.NAME == 'pawn':
                movement += CHAR_REP[str(piece.x)]
            movement += 'x'

        if self.there_is_check():
            movement += '+'

        movement += column
        movement += str(row)

        castle_king = castle_queen = False
        if piece.NAME == 'king' and piece.COLOR == 'white':
            castle_queen = piece.x - target[0] == 2
            castle_king = piece.x - target[0] == -2
        elif piece.NAME == 'king' and piece.COLOR == 'black':
            castle_queen = piece.x - target[0] == 2
            castle_king = piece.x - target[0] == -2

        if castle_king:
            movement = 'O-O'
        elif castle_queen:
            movement = 'O-O-O'

        return movement
        # return [piece_name, movement]

    def update_move_history(self, origin_piece, target_cell):
        x2, y2 = target_cell
        target_piece = self.get_piece(x2, y2)

        entry = self.index_to_chess_notation(origin_piece, target_cell)
        if origin_piece.COLOR == 'white':
            self.info.move_history[self.info.turn_count] = {'white': entry}
        else:
            self.info.move_history[self.info.turn_count][origin_piece.COLOR] = entry

    # def promote_pawn(self, x, y, promotion):
    #     piece = self.get_piece(x, y)
    #     if not piece:
    #         raise ValueError('No piece to promote')
    #     elif piece.NAME != 'pawn':
    #         raise ValueError("Piece is not a pawn")
    #     elif piece.promotion:
    #         self.pieces.remove(piece)
    #         if promotion == 'queen':
    #             self.pieces.append(Queen(piece.COLOR, x, y, self))
    #         elif promotion == 'rook':
    #             self.pieces.append(Rook(piece.COLOR, x, y, self))
    #         elif promotion == 'bishop':
    #             self.pieces.append(Bishop(piece.COLOR, x, y, self))
    #         elif promotion == 'knight':
    #             self.pieces.append(Knight(piece.COLOR, x, y, self))
    #         else:
    #             raise ValueError('Piece name is not valid')
    #
    #     else:
    #         raise ValueError("Piece can't be promoted")

    def remove_en_passant_tag(self):
        for piece in self.pieces:
            if piece.NAME == 'pawn':
                piece.en_passant = False

    def change_turn(self):
        self.info.move_count += 1
        if self.info.current_turn == 'white':
            self.info.current_turn = 'black'
        else:
            self.info.turn_count += 1
            self.info.current_turn = 'white'

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
        self.set_timer()
        self.pieces = []
        self._setup_pieces()

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

                self.info.check_mate = True
                self.info.winner = winner


# class _Board:
#     def __init__(self):
#         self.info = BoardInfo(self)
#         self.events = BoardEvents(self)
#
#         self.players = {'one': None, 'two': None}
#         self.turn_count = 1
#         self.pieces = []
#         self.turn = 'white'
#         self.king = {}
#         self.move_count = 1
#         self._setup_pieces()
#
#         self.move_history = {}
#         self.last_movement = None
#         self.check = False
#         self.game_over = True
#         self.time_up = False
#         self.clock_running = False
#         self.timer = {}
#         self.set_timer()
#
#     def set_timer(self, minutes=5):
#         self.timer['white'] = minutes*60
#         self.timer['black'] = minutes*60
#
#     def get_piece(self, x, y):
#         for piece in self.pieces:
#             if piece.x == x and piece.y == y:
#                 return piece
#
#     def move(self, origin_cell, target_cell, player):
#         x1, y1 = origin_cell
#         x2, y2 = target_cell
#         origin_piece = self.get_piece(x=x1, y=y1)
#         target_piece = self.get_piece(x=x2, y=y2)
#
#         if origin_piece is None:
#             return
#
#         move_is_allowed = (target_cell in origin_piece.moves) if origin_piece.moves else None
#         print(player.ip, player.color)
#         # is_your_turn = self.turn == origin_piece.COLOR == player.color
#         is_your_turn = self.turn == origin_piece.COLOR
#         # is_your_turn = True
#         if move_is_allowed and is_your_turn:
#             self.remove_en_passant_tag()
#             origin_piece.move(x2, y2)
#             self.change_turn()
#             self.update_board()
#             self.last_movement = [[x1, y1], [x2, y2]]
#
#             # TODO
#             if origin_piece.COLOR == 'white':
#                 self.move_history[self.turn_count] = [f'{self.turn_count}. '+index_to_chess_notation(origin_piece.NAME, target_cell)]
#             else:
#                 white_move = self.move_history[self.turn_count-1]
#                 self.move_history[self.turn_count-1] = [white_move, [index_to_chess_notation(origin_piece.NAME, target_cell)]]
#             # TODO
#
#         else:
#             raise ValueError('Movement Not allowed')
#
#     def promote_pawn(self, x, y, promotion):
#         piece = self.get_piece(x, y)
#         if not piece:
#             raise ValueError('No piece to promote')
#         elif piece.NAME != 'pawn':
#             raise ValueError("Piece is not a pawn")
#         elif piece.promotion:
#             self.pieces.remove(piece)
#             if promotion == 'queen':
#                 self.pieces.append(Queen(piece.COLOR, x, y, self))
#             elif promotion == 'rook':
#                 self.pieces.append(Rook(piece.COLOR, x, y, self))
#             elif promotion == 'bishop':
#                 self.pieces.append(Bishop(piece.COLOR, x, y, self))
#             elif promotion == 'knight':
#                 self.pieces.append(Knight(piece.COLOR, x, y, self))
#             else:
#                 raise ValueError('Piece name is not valid')
#
#         else:
#             raise ValueError("Piece can't be promoted")
#
#     def remove_en_passant_tag(self):
#         for piece in self.pieces:
#             if piece.NAME == 'pawn':
#                 piece.en_passant = False
#
#     def change_turn(self):
#         self.move_count += 1
#         if self.turn == 'white':
#             self.turn = 'black'
#         else:
#             self.turn_count += 1
#             self.turn = 'white'
#
#     def _setup_pieces(self):
#         for i in range(8):
#             pass
#             self.pieces.append(Pawn('black', x=i, y=1, board=self))
#             self.pieces.append(Pawn('white', x=i, y=6, board=self))
#
#         ''' Blacks '''
#         self.pieces.append(Rook('black', y=0, x=0, board=self))
#         self.pieces.append(Rook('black', y=0, x=7, board=self))
#         self.pieces.append(Knight('black', y=0, x=1, board=self))
#         self.pieces.append(Knight('black', y=0, x=6, board=self))
#         self.pieces.append(Bishop('black', y=0, x=2, board=self))
#         self.pieces.append(Bishop('black', y=0, x=5, board=self))
#         self.pieces.append(Queen('black', y=0, x=3, board=self))
#         self.king['black'] = King('black', y=0, x=4, board=self)
#         self.pieces.append(self.king['black'])
#
#         ''' Whites '''
#         self.pieces.append(Rook('white', y=7, x=0, board=self))
#         self.pieces.append(Rook('white', y=7, x=7, board=self))
#         self.pieces.append(Knight('white', y=7, x=1, board=self))
#         self.pieces.append(Knight('white', y=7, x=6, board=self))
#         self.pieces.append(Bishop('white', y=7, x=2, board=self))
#         self.pieces.append(Bishop('white', y=7, x=5, board=self))
#         self.pieces.append(Queen('white', y=7, x=3, board=self))
#
#         self.king['white'] = King('white', y=7, x=4, board=self)
#         self.pieces.append(self.king['white'])
#
#     def there_is_check(self):
#         if self.king['white'].check:
#             self.check = 'white'
#         elif self.king['black'].check:
#             self.check = 'black'
#         else:
#             self.check = False
#
#     def update_board(self):
#         self.king['white'].get_moves()
#         self.king['black'].get_moves()
#         for piece in self.pieces:
#             if piece.NAME != 'king':
#                 piece.get_moves()
#
#         self.there_is_check()
#
#     def get_state(self):
#         self.update_board()
#         state = []
#         for piece in self.pieces:
#             moves = piece.moves
#
#             index_list = []
#             if moves:
#                 for each in moves:
#                     x, y = each
#                     index_list.append({'x': x, 'y': y})
#
#             piece_attributes = {
#                 'color': piece.COLOR,
#                 'name': piece.NAME,
#                 'x': piece.x,
#                 'y': piece.y,
#                 'moves': index_list,
#             }
#             state.append(piece_attributes)
#         return state
#
#     def reset_board(self):
#         self.time_up = None
#         self.game_over = False
#         self.set_timer()
#         self.pieces = []
#         self._setup_pieces()
#         self.turn = 'white'
#         self.turn_count = 1
#         self.move_count = 1
#         self.last_movement = None
#         self.move_history = {}
#
#     def check_mate(self):
#         colors = ['white', 'black']
#
#         for color in colors:
#             moves = []
#             for piece in self.pieces:
#                 if piece.COLOR == color and piece.moves:
#                     for m in piece.moves:
#                         moves.append(m)
#             if not moves:
#                 winner = 'white' if color == 'black' else 'black'
#                 self.game_over = True
#                 return True, winner
#         return False, None




# b = Board()
# for each in b.pieces:
#     print(each.x, each.y)


# print(b.get_piece(0, 0).moves(b))


# print(b.get_state())


# print(convert_to_index('C1'))
# y, x = convert_to_index('b4')
# print(b.GRID[x][y])

