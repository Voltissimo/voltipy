from pieces import LETTER_TYPE, TYPE_LETTER, Piece, Move
from utils import convert_notation
from typing import Union
import pprint
pp = pprint.PrettyPrinter()


class Game:
    """
    Handles communication between player/AI, Board and AI
    """

    def __init__(self):
        self.board = Board.from_start_pos()



class Board:
    """
    Representation of the chessboard
    :input_matrix: holds the board position (objects)
    TODO: check for en passant + ability to O-O
    """
    def __init__(self, input_matrix, active_color, castling_available,
                 en_passant_square, halfmove_clock, fullmove_number):
        # Setup board parameters
        self.board_matrix = input_matrix
        self.active_color = active_color
        self.castling_available = castling_available
        self.en_passant_square = en_passant_square
        self.halfmove_clock = halfmove_clock
        self.fullmove_number = fullmove_number

        # TODO: detect that
        self.black_in_check = False
        self.white_in_check = False

    def __str__(self):
        return "\n".join([
            "".join(
                [square.get_letter() if square else '-' for square in row]
            ) for row in self.board_matrix
        ][::-1])

    def __getitem__(self, item):
        if type(item) is tuple:
            return self.board_matrix[item[0]][item[1]]

    def __setitem__(self, key, value):
        if type(key) is tuple:
            self.board_matrix[key[0]][key[1]] = value

    @classmethod
    def from_fen(cls, fen_string: str) -> 'Board':
        """
        Initialise a Board object from a fen string
        More info here https://en.wikipedia.org/wiki/Forsyth%E2%80%93Edwards_Notation
        :param fen_string: see link above for format
        :return: Board object with the filled board matrix
        """
        # eat the parameters (nom nom nom)
        board_setup, *board_parameters = fen_string.split()
        active_color = board_parameters[0]
        castling_available = {
            'white': {
                'k': 'K' in board_parameters[1],
                'q': 'Q' in board_parameters[1]
            },
            'black': {
                'k': 'k' in board_parameters[1],
                'q': 'q' in board_parameters[1]
            }
        }
        en_passant_square = board_parameters[2]
        halfmove_clock = int(board_parameters[3])
        fullmove_number = int(board_parameters[4])

        board_matrix = [[None for _ in range(8)] for _ in range(8)]
        new_board = cls(board_matrix, active_color, castling_available,
                        en_passant_square, halfmove_clock, fullmove_number)

        row_num, col_num = 0, 0
        # we must reverse to get correct board position
        for row in board_setup.split('/')[::-1]:
            for token in row:
                if token.isdigit():
                    col_num += int(token) - 1
                else:
                    board_matrix[row_num][col_num] = LETTER_TYPE[token.lower()](
                        side='black' if token.islower() else 'white', board=new_board
                    )
                col_num += 1
            col_num = 0
            row_num += 1

        new_board.board_matrix = board_matrix
        return new_board

    @classmethod
    def from_start_pos(cls) -> 'Board':
        """
        Initiate a board at starting position
        :return: Board object
        >>> print(Board.from_start_pos())
        rnbqkbnr
        pppppppp
        --------
        --------
        --------
        --------
        PPPPPPPP
        RNBQKBNR
        """
        return cls.from_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")

    def move(self, move_string: str) -> Union['Piece', None]:
        """
        Moves a piece on the board
        BEWARE! this function is stupid and doesn't know how to play chess.
        It won't raise an error on an illegal move.
        :param move_string: position in str (ex: e2e4)
        :return: returns what was captured if there was a piece else None

        >>> b = Board.from_start_pos()
        >>> b.move('e2e4')
        >>> print(b)
        rnbqkbnr
        pppppppp
        --------
        --------
        ----P---
        --------
        PPPP-PPP
        RNBQKBNR
        """
        assert len(move_string) == 4
        departure, arrival = convert_notation(move_string[:2]), convert_notation(move_string[2:])
        piece = self[departure]
        self[departure] = None
        taken = self[arrival]
        self[arrival] = piece
        return taken


if __name__ == '__main__':
    starting_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    test_fen = "rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR w KQkq c6 0 2"
    b = Board.from_start_pos()
    b.move('b1d6')
    print(b[convert_notation('d6')].get_legal_moves(convert_notation('d6')))
    print(b)


