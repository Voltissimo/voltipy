from utils import convert_notation
from operator import add
from typing import NewType

# because circular imports
Board = NewType('Board', dict)


class Piece:
    def __init__(self, side: str, board: 'Board', enemy_control: set = set()):
        self.side = side
        self.board = board
        self.enemy_control = enemy_control

    def __repr__(self):
        return f"<{self.__class__.__name__} side={self.side}>"

    def get_letter(self) -> str:
        if self.side == "white":
            return TYPE_LETTER[self.__class__].upper()
        else:
            return TYPE_LETTER[self.__class__]

    @staticmethod
    def filter_out_of_bounds(all_moves: set, pos: tuple) -> set:
        return set(
            tuple(map(add, pos, i)) for i in all_moves if all(
                # check if both row and col (coord) are in bounds
                coord in range(8) for coord in map(add, pos, i)
            )
        )


class Pawn(Piece):
    value = 1

    def get_legal_moves(self, pos: tuple, in_check=False):
        pawn_home_row = 1 if self.side == "white" else 6
        forward = 1 if self.side == 'white' else -1
        row, col = pos
        legal_moves = set()

        # check if its at the end of the board
        if self.can_advance(row):
            # TODO: this shouldn't happen thanks to promotion
            pass
        else:
            # TODO: support en passant

            # move forward
            front = (row + forward, col)
            if self.board[front] is None:
                legal_moves.add(Move(pos, front, self))
                # check if can double jump
                double_front = (row + forward * 2, col)
                if row == pawn_home_row and self.board[double_front] is None:
                    en_passant_square = front
                    legal_moves.add(Move(pos, front, self, en_passant_square))

            # capture in diag
            for offset in [-1, 1]:
                diag = (row + forward, col + offset)
                if self.board[diag] is not None and self.board[diag].side != self.side:
                    legal_moves.add(convert_notation(diag))
        return legal_moves

    def can_advance(self, row):
        return (self.side == 'white' and row == 7) or (self.side == 'black' and row == 0)


class Rook(Piece):
    value = 5


class Knight(Piece):
    value = 3

    def get_legal_moves(self, pos: tuple):
        all_moves = {
            (-2, 1), (-2, -1), (-1, 2), (-1, -2), (1, 2), (1, -2), (2, 1), (2, -1)
        }
        in_bound_moves = self.filter_out_of_bounds(all_moves, pos)

        legal_moves = set()
        for possible_move in in_bound_moves:
            if self.board[possible_move] is None:
                legal_moves.add(Move(pos, possible_move, self))
            elif self.board[possible_move].side != self.side:
                if type(self.board[possible_move]) is King:
                    legal_moves.add(CheckThreat(pos, possible_move, self))
                else:
                    legal_moves.add(CaptureMove(pos, possible_move, self))

        return legal_moves


class Bishop(Piece):
    value = 3


class Queen(Piece):
    value = 9


class King(Piece):
    value = None

    def get_legal_moves(self):
        # self.enemy_control is used to filter out check suicide
        pass


# Constants
LETTER_TYPE = {
    'p': Pawn,
    'r': Rook,
    'n': Knight,
    'b': Bishop,
    'q': Queen,
    'k': King
}

TYPE_LETTER = {v: k for k, v in LETTER_TYPE.items()}


class Move:
    def __init__(self, initial_pos: tuple, arrival_pos: tuple, piece: 'Piece', en_passant_square: str = ''):
        self.departure = initial_pos
        self.arrival = arrival_pos
        self.piece = piece
        self.en_passant_square = en_passant_square

        self.full_notation = \
            f"{convert_notation(initial_pos)}{convert_notation(arrival_pos)}"
        self.reduced_notation = f"{convert_notation(arrival_pos)}"
        # this parameter is changed during runtime (when we check for move string conflicts)
        self.use_full_notation = False

    def __str__(self):
        return_str = ''
        if self.use_full_notation:
            return_str = self.full_notation
        else:
            return_str = self.reduced_notation
        # there are no prefixes on pawn moves
        if type(self.piece) is not Pawn:
            return f"{self.piece.get_letter()}{return_str}"
        else:
            return return_str

    def __repr__(self):
        return f"<{self.__class__.__name__} piece={self.piece.get_letter()} move={str(self)}>"


class CaptureMove(Move):
    def __init__(self, initial_pos: tuple, arrival_pos: tuple, piece: 'Piece'):
        super().__init__(initial_pos, arrival_pos, piece)

        self.full_notation = \
            f"{convert_notation(initial_pos)}x{convert_notation(arrival_pos)}"
        self.reduced_notation = f"x{convert_notation(arrival_pos)}"


class CheckThreat(Move):
    pass
