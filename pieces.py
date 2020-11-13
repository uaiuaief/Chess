class Piece:
    def __init__(self):
        raise TypeError('Class Piece can not be instantiated')

    def __repr__(self):
        return f'{self.COLOR} {self.NAME}'

    def move(self, x, y):
        enemy_piece = self.board.get_piece(x, y)

        if enemy_piece:
            self.board.pieces.remove(enemy_piece)

        self.x = x
        self.y = y

    def can_move(self, x, y):
        target_piece = self.board.get_piece(x, y)
        in_bounds = 0 <= x <= 7 and 0 <= y <= 7

        if self.NAME == 'king':
            if self.square_is_attacked(x, y):
                return False

        if not in_bounds:
            return False
        elif not target_piece:
            return True
        elif target_piece.COLOR != self.COLOR:
            return True
        else:
            return False

    def get_move_intersection(self, self_moves, enemy_moves):
        intersection = [m for m in self_moves if m in enemy_moves]
        return intersection

    def _is_defending(self):
        pass
    # def simulate(self, x, y):
    #     old_pos = [self.x, self.y]
    #     self.x, self.y = x, y
    #
    #     king = self.board.king[self.COLOR]
    #     if king.is_in_check():
    #         self.x, self.y = old_pos
    #         return False
    #     else:
    #         self.x, self.y = old_pos
    #         return True

    def square_is_attacked(self, x, y):
        ghost_piece = Ghost(self.COLOR, x, y, self.board)
        if ghost_piece.attackers():
            return True

    def _pawn_capture(self):
        moves = []
        one = 1 if self.COLOR == 'black' else -1

        capture_moves = [
            [self.x - 1, self.y + one],
            [self.x + 1, self.y + one]
        ]

        for move in capture_moves:
            piece = self.board.get_piece(move[0], move[1])
            if piece and piece.COLOR != self.COLOR:
                moves.append(move)

        return moves

    def add_movement(self, arr, x, y, scan):
        target_square = [x, y]
        piece = self.board.get_piece(target_square[0], target_square[1])

        if scan:
            arr.append(target_square)
            if piece and piece.COLOR != self.COLOR:
                return True
        else:
            if self.can_move(target_square[0], target_square[1]):
                arr.append(target_square)

            if piece:
                if self.NAME == 'ghost' and piece.NAME == 'king' and piece.COLOR == self.COLOR:
                    pass
                else:
                    return True

    def _upward_movement(self, scan=False):
        upward_movement = []

        for i in range(self.y, 0, -1):
            _break = self.add_movement(upward_movement, self.x, i-1, scan=scan)
            if _break:
                break

        return upward_movement

    def _downward_movement(self, scan=False):
        downward_movement = []

        for i in range(self.y+1, 8):
            _break = self.add_movement(downward_movement, self.x, i, scan=scan)
            if _break:
                break

        return downward_movement

    def _rightward_movement(self, scan=False):
        rightward_movement = []

        for i in range(self.x + 1, 8):
            _break = self.add_movement(rightward_movement, i, self.y, scan=scan)
            if _break:
                break

        return rightward_movement

    def _leftward_movement(self, scan=False):
        leftward_movement = []

        for i in range(self.x, 0, -1):
            _break = self.add_movement(leftward_movement, i - 1, self.y, scan=scan)
            if _break:
                break

        return leftward_movement

    def _upper_left_diagonal(self, scan=False):
        upper_left_diagonal_moves = []

        for i in range(1, 8):
            if 0 <= self.y-i < 8 and 0 <= self.x-i < 8:
                _break = self.add_movement(upper_left_diagonal_moves, self.x - i, self.y - i, scan=scan)
                if _break:
                    break

        return upper_left_diagonal_moves

    def _upper_right_diagonal(self, scan=False):
        upper_right_diagonal_moves = []

        for i in range(1, 8):
            if 0 <= self.y - i < 8 and 0 <= self.x + i < 8:
                _break = self.add_movement(upper_right_diagonal_moves, self.x + i, self.y - i, scan=scan)
                if _break:
                    break

        return upper_right_diagonal_moves

    def _bottom_left_diagonal(self, scan=False):
        bottom_left_diagonal_moves = []

        for i in range(1, 8):
            if 0 <= self.y + i < 8 and 0 <= self.x - i < 8:
                _break = self.add_movement(bottom_left_diagonal_moves, self.x - i, self.y + i, scan=scan)
                if _break:
                    break

        return bottom_left_diagonal_moves

    def _bottom_right_diagonal(self, scan=False):
        bottom_right_diagonal_moves = []

        for i in range(1, 8):
            if 0 <= self.y + i < 8 and 0 <= self.x + i < 8:
                _break = self.add_movement(bottom_right_diagonal_moves, self.x + i, self.y + i, scan=scan)
                if _break:
                    break

        return bottom_right_diagonal_moves

    def _l_moves(self):
        moves = []
        move_list = [
            [self.x + 1, self.y - 2],
            [self.x - 1, self.y - 2],
            [self.x + 1, self.y + 2],
            [self.x - 1, self.y + 2],
            [self.x + 2, self.y - 1],
            [self.x + 2, self.y + 1],
            [self.x - 2, self.y - 1],
            [self.x - 2, self.y + 1]
        ]
        for index in move_list:
            x, y = index
            if self.can_move(x, y):
                moves.append(index)

        return moves


class Pawn(Piece):
    def __init__(self, color, x, y, board):
        self.board = board
        self.COLOR = color
        self.NAME = 'pawn'
        self.first_move = True
        self.en_passant = False
        self.x = x
        self.y = y
        self.moves = None
        self.attacker = None
        self.blocking_moves = None

    def move(self, x, y):
        self.first_move = False

        enemy_piece = self.board.get_piece(x, y)

        if abs(self.y - y) == 2:
            self.en_passant = True

        if self.x - x != 0 and not enemy_piece:
            self._capture_en_passant(x, y)

        if enemy_piece:
            self.board.pieces.remove(enemy_piece)

        self.x = x
        self.y = y

    def _capture_en_passant(self, x, y):
        one = 1 if self.COLOR == 'white' else -1
        piece = self.board.get_piece(x, y + one)
        if piece and piece.COLOR != self.COLOR:
            self.board.pieces.remove(piece)

    def get_moves(self):
        up = self._move_up()
        capture = self._pawn_capture()
        en_passant = self._en_passant_moves()
        king = self.board.king[self.COLOR]

        possible_moves = up + capture + en_passant

        if self.blocking_moves:
            possible_moves = self.get_move_intersection(possible_moves, self.blocking_moves)

        if king.attackers and len(king.attackers) > 1:
            possible_moves = []
        elif king.attackers:
            possible_moves = self.get_move_intersection(possible_moves, king.king_defending_moves)


        self.moves = possible_moves

    def _en_passant_moves(self):
        moves = []
        piece_at_right = self.board.get_piece(self.x+1, self.y)
        piece_at_left = self.board.get_piece(self.x-1, self.y)

        if piece_at_right:
            is_pawn = piece_at_right.NAME == 'pawn'
            is_enemy = piece_at_right.COLOR != self.COLOR
            if is_pawn and is_enemy and piece_at_right.en_passant:
                if piece_at_right.COLOR == 'black':
                    moves.append([self.x+1, self.y-1])
                else:
                    moves.append([self.x+1, self.y+1])

        if piece_at_left:
            is_pawn = piece_at_left.NAME == 'pawn'
            is_enemy = piece_at_left.COLOR != self.COLOR
            if is_pawn and is_enemy and piece_at_left.en_passant:
                if piece_at_left.COLOR == 'black':
                    moves.append([self.x-1, self.y-1])
                else:
                    moves.append([self.x-1, self.y+1])
        return moves

    def _move_up(self):
        moves = []
        one = 1 if self.COLOR == 'black' else -1
        two = 2 if self.COLOR == 'black' else -2

        one_up = [self.x, self.y + one]
        two_up = [self.x, self.y + two]
        in_bounds = 0 <= one_up[1] <= 7
        if in_bounds and not self.board.get_piece(one_up[0], one_up[1]):
            moves.append(one_up)

        if self.first_move and not self.board.get_piece(one_up[0], one_up[1]) and not self.board.get_piece(two_up[0], two_up[1]):
            moves.append(two_up)

        return moves


class Rook(Piece):
    def __init__(self, color, x, y, board):
        self.board = board
        self.COLOR = color
        self.NAME = 'rook'
        self.x = x
        self.y = y
        self.moves = None
        self.already_moved = False
        self.blocking_moves = None

    def move(self, x, y):
        super().move(x, y)
        self.already_moved = True

    def get_moves(self):

        up = self._upward_movement()
        down = self._downward_movement()
        right = self._rightward_movement()
        left = self._leftward_movement()
        possible_moves = up + down + right + left
        # possible_moves = right
        if self.blocking_moves:
            possible_moves = self.get_move_intersection(possible_moves, self.blocking_moves)
        # if not king.check:
        king = self.board.king[self.COLOR]
        if king.attackers and len(king.attackers) > 1:
            possible_moves = []
        elif king.attackers:
            possible_moves = self.get_move_intersection(possible_moves, king.king_defending_moves)

        self.moves = possible_moves
        # elif [king.attacking_piece.x, king.attacking_piece.y] in possible_moves:
        #     self.moves = [[king.attacking_piece.x, king.attacking_piece.y]]
        # else:
        #     self.moves = []


class Knight(Piece):
    def __init__(self, color, x, y, board):
        self.board = board
        self.COLOR = color
        self.NAME = 'knight'
        self.x = x
        self.y = y
        self.moves = None
        self.blocking_moves = None

    def get_moves(self):
        possible_moves = self._l_moves()

        # king = board.king[self.COLOR]
        # if not king.check:

        if self.blocking_moves:
            possible_moves = self.get_move_intersection(possible_moves, self.blocking_moves)

        king = self.board.king[self.COLOR]
        if king.attackers and len(king.attackers) > 1:
            possible_moves = []
        elif king.attackers:
            possible_moves = self.get_move_intersection(possible_moves, king.king_defending_moves)

        self.moves = possible_moves
        # elif [king.attacking_piece.x, king.attacking_piece.y] in possible_moves:
        #     self.moves = [[king.attacking_piece.x, king.attacking_piece.y]]
        # else:
        #     self.moves = []


class Bishop(Piece):
    def __init__(self, color, x, y, board):
        self.board = board
        self.COLOR = color
        self.NAME = 'bishop'
        self.x = x
        self.y = y
        self.moves = None
        self.blocking_moves = None

    def get_moves(self):
        upper_left = self._upper_left_diagonal()
        upper_right = self._upper_right_diagonal()
        bottom_left = self._bottom_left_diagonal()
        bottom_right = self._bottom_right_diagonal()

        possible_moves = upper_left + upper_right + bottom_left + bottom_right

        if self.blocking_moves:
            possible_moves = self.get_move_intersection(possible_moves, self.blocking_moves)

        # king = board.king[self.COLOR]
        # if not king.check:
        king = self.board.king[self.COLOR]
        if king.attackers and len(king.attackers) > 1:
            possible_moves = []
        elif king.attackers:
            possible_moves = self.get_move_intersection(possible_moves, king.king_defending_moves)

        self.moves = possible_moves
        # elif [king.attacking_piece.x, king.attacking_piece.y] in possible_moves:
        #     self.moves = [[king.attacking_piece.x, king.attacking_piece.y]]
        # else:
        #     self.moves = []


class Queen(Piece):
    def __init__(self, color, x, y, board):
        self.board = board
        self.COLOR = color
        self.NAME = 'queen'
        self.x = x
        self.y = y
        self.moves = None
        self.blocking_moves = None

    def get_moves(self):
        up = self._upward_movement()
        down = self._downward_movement()
        right = self._rightward_movement()
        left = self._leftward_movement()

        upper_left = self._upper_left_diagonal()
        upper_right = self._upper_right_diagonal()
        bottom_left = self._bottom_left_diagonal()
        bottom_right = self._bottom_right_diagonal()

        possible_moves = up + down + right + left + upper_left + upper_right + bottom_left + bottom_right

        if self.blocking_moves:
            possible_moves = self.get_move_intersection(possible_moves, self.blocking_moves)
        # king = board.king[self.COLOR]
        # if not king.check:
        king = self.board.king[self.COLOR]
        if king.attackers and len(king.attackers) > 1:
            possible_moves = []
        elif king.attackers:
            possible_moves = self.get_move_intersection(possible_moves, king.king_defending_moves)

        self.moves = possible_moves
        # elif [king.attacking_piece.x, king.attacking_piece.y] in possible_moves:
        #     self.moves = [[king.attacking_piece.x, king.attacking_piece.y]]
        # else:
        #     self.moves = []


class King(Piece):
    def __init__(self, color, x, y, board):
        self.board = board
        self.COLOR = color
        self.NAME = 'king'
        self.x = x
        self.y = y
        self.already_moved = False
        self.check = False
        self.attackers = None
        self.moves = None
        self.king_defending_moves = None

    def move(self, x, y):
        self.already_moved = True
        if x - self.x == 2:
            castling_rook = self.board.get_piece(7, self.y)
            castling_rook.move(x-1, self.y)
        elif x - self.x == -2:
            castling_rook = self.board.get_piece(0, self.y)
            castling_rook.move(x+1, self.y)

        super().move(x, y)

    def get_moves(self):
        self.set_blocking_moves()
        self.is_in_check()
        possible_moves = []

        move_list = [
            [self.x+1, self.y],
            [self.x+1, self.y+1],
            [self.x+1, self.y-1],
            [self.x-1, self.y],
            [self.x-1, self.y+1],
            [self.x-1, self.y-1],
            [self.x, self.y+1],
            [self.x, self.y-1]
        ]

        for move in move_list:
            x, y = move
            if self.can_move(x, y):
                possible_moves.append(move)

        possible_moves += self._castle_moves()

        self.moves = possible_moves

    def _castle_moves(self):
        moves = []
        if not self.already_moved:
            for i in range(self.x+1, 8):
                piece = self.board.get_piece(i, self.y)
                if not piece:
                    continue
                elif piece and piece.NAME != 'rook':
                    break
                elif piece.COLOR == self.COLOR and not piece.already_moved:
                    moves.append([self.x+2, self.y])

            for i in range(self.x, 0, -1):
                piece = self.board.get_piece(i-1, self.y)
                if not piece:
                    continue
                elif piece and piece.NAME != 'rook':
                    break
                elif piece.COLOR == self.COLOR and not piece.already_moved:
                    moves.append([self.x-2, self.y])

        return moves

    def is_in_check(self):
        if self.square_is_attacked(self.x, self.y):
            self.check = True
            # print(self.attackers)
        else:
            self.check = False

    def _defender_blocking_moves(self, move_list, piece_names):
        defender = None
        for move in move_list:
            piece = self.board.get_piece(move[0], move[1])
            if defender:
                if piece and (piece.COLOR == self.COLOR or piece.NAME not in piece_names):
                    break
                elif piece:
                    defender.blocking_moves = move_list

            elif piece:
                if piece.COLOR == self.COLOR:
                    defender = piece
                else:
                    if piece.NAME in piece_names:
                        self.king_defending_moves = move_list
                    break

        return []

    def set_blocking_moves(self):
        ghost = Ghost(self.COLOR, self.x, self.y, self.board)
        up = ghost._upward_movement(scan=True)
        down = ghost._downward_movement(scan=True)
        left = ghost._leftward_movement(scan=True)
        right = ghost._rightward_movement(scan=True)
        upper_left = ghost._upper_left_diagonal(scan=True)
        upper_right = ghost._upper_right_diagonal(scan=True)
        bottom_left = ghost._bottom_left_diagonal(scan=True)
        bottom_right = ghost._bottom_right_diagonal(scan=True)

        for each in self.board.pieces:
            if each.COLOR == self.COLOR:
                each.blocking_moves = None

        blocking_moves = self._defender_blocking_moves(up, ['rook', 'queen']) \
            + self._defender_blocking_moves(down, ['rook', 'queen']) \
            + self._defender_blocking_moves(left, ['rook', 'queen']) \
            + self._defender_blocking_moves(right, ['rook', 'queen']) \
            + self._defender_blocking_moves(upper_left, ['bishop', 'queen']) \
            + self._defender_blocking_moves(upper_right, ['bishop', 'queen']) \
            + self._defender_blocking_moves(bottom_left, ['bishop', 'queen']) \
            + self._defender_blocking_moves(bottom_right, ['bishop', 'queen'])



    """ CHECK 
    case 1:
        the king tries to move into a square that's being atacked by an enemy piece
        DONE
    
    case 2:
        there's an allied piece protecting the king from an enemy attack, this piece
        can't move or the king will be in check.
        DONE
    
    case 3:
        the king is in check, and it has to get safe or an allied piece has to to protect it.
        DONE
        
    case 4 - Check mate:
        the king is in check and no movement is possible to get out of it.
    
    """


class Ghost(Piece):
    def __init__(self, color, x, y, board):
        self.board = board
        self.COLOR = color
        self.NAME = 'ghost'
        self.x = x
        self.y = y
        self.moves = None

    def attackers(self):
        rook_movement = self.check_rook_movement()
        bishop_movement = self.check_bishop_movement()
        pawn_movement = self.check_pawn_movement()
        knight_movement = self.check_knight_movement()

        attackers = rook_movement + bishop_movement + pawn_movement + knight_movement

        king = self.board.king[self.COLOR]
        if [self.x, self.y] == [king.x, king.y]:
            if attackers:
                king.attackers = attackers
            else:
                king.attackers = None

        return attackers

    def check_rook_movement(self):
        attackers = []

        up = self._upward_movement()
        down = self._downward_movement()
        left = self._leftward_movement()
        right = self._rightward_movement()
        possible_moves = up + down + left + right

        for each in possible_moves:
            piece = self.board.get_piece(each[0], each[1])
            if piece and (piece.NAME == 'rook' or piece.NAME == 'queen'):
                attackers.append(piece)

        return attackers

    def check_bishop_movement(self):
        attackers = []

        upper_left = self._upper_left_diagonal()
        upper_right = self._upper_right_diagonal()
        bottom_left = self._bottom_left_diagonal()
        bottom_right = self._bottom_right_diagonal()
        possible_moves = upper_left + upper_right + bottom_left + bottom_right

        for each in possible_moves:
            piece = self.board.get_piece(each[0], each[1])
            if piece and (piece.NAME == 'bishop' or piece.NAME == 'queen'):
                attackers.append(piece)

        return attackers

    def check_pawn_movement(self):
        attackers = []
        possible_moves = self._pawn_capture()

        for each in possible_moves:
            piece = self.board.get_piece(each[0], each[1])
            if piece and (piece.NAME == 'pawn'):
                attackers.append(piece)

        return attackers

    def check_knight_movement(self):
        attackers = []
        possible_moves = self._l_moves()
        for each in possible_moves:
            piece = self.board.get_piece(each[0], each[1])
            if piece and (piece.NAME == 'knight'):
                attackers.append(piece)

        return attackers


