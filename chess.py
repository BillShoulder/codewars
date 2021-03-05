""" Chess related functions. """

#######################################################################################################################
#
#   Import
#
#######################################################################################################################

from itertools import product
from collections import namedtuple
from enum import IntEnum


#######################################################################################################################
#
#   Global
#
#######################################################################################################################

BOARD = range(8)

Square = namedtuple("Square", "x y")

class Player(IntEnum):
    WHITE = 0
    BLACK = 1


#######################################################################################################################
#
#   pawn_moves
#
#######################################################################################################################

def pawn_moves(square, player):
    squares = pawn_moves.cache.get((square, player))
    if squares is not None:
        return squares
    direction = 1 if player == Player.BLACK else -1
    start_row = 1 if player == Player.BLACK else 6
    squares = [Square(square.x, square.y + direction)]
    if square.y == start_row:
        squares.append(Square(square.x, square.y + 2 * direction))
    pawn_moves.cache[(square, player)] = [squares]
    return pawn_moves.cache[(square, player)]
pawn_moves.cache = {}


#######################################################################################################################
#
#   rook_moves
#
#######################################################################################################################

def rook_moves(square):
    squares = rook_moves.cache.get(square)
    if squares is not None:
        return squares
    squares = [[Square(x, square.y) for x in range(square.x + 1, BOARD.stop)]]
    squares.append([Square(x, square.y) for x in range(square.x - 1, BOARD.start - 1, -1)])
    squares.append([Square(square.x, y) for y in range(square.y + 1, BOARD.stop)])
    squares.append([Square(square.x, y) for y in range(square.y - 1, BOARD.start - 1, -1)])
    rook_moves.cache[square] = list(filter(None, squares))
    return rook_moves.cache[square]
rook_moves.cache = {}


#######################################################################################################################
#
#   knight_moves
#
#######################################################################################################################

def knight_moves(square):
    squares = knight_moves.cache.get(square)
    if squares is not None:
        return squares
    squares = list(product([square.x - 1, square.x + 1], [square.y - 2, square.y + 2])) + list(product([square.x - 2, square.x + 2], [square.y - 1, square.y + 1]))
    squares = set(Square(x, y) for x, y in squares if x in BOARD and y in BOARD)
    knight_moves.cache[square] = [list(squares)]
    return knight_moves.cache[square]
knight_moves.cache = {}


#######################################################################################################################
#
#   bishop_moves
#
#######################################################################################################################

def bishop_moves(square):
    squares = bishop_moves.cache.get(square)
    if squares is not None:
        return squares
    deltas = [(x, y) for x in (-1, 1) for y in (-1, 1)]
    squares = []
    for delta in deltas:
        vector = []
        x, y = square.x, square.y
        while True:
            x += delta[0]
            y += delta[1]
            if x not in BOARD or y not in BOARD:
                break
            vector.append(Square(x, y))
        squares.append(vector)
    bishop_moves.cache[square] = list(filter(None, squares))
    return bishop_moves.cache[square]
bishop_moves.cache = {}


#######################################################################################################################
#
#   queen_moves
#
#######################################################################################################################

def queen_moves(square):
    return rook_moves(square) + bishop_moves(square) 


#######################################################################################################################
#
#   king_moves
#
#######################################################################################################################

def king_moves(square):
    squares = king_moves.cache.get(square)
    if squares is not None:
        return squares
    squares = [(x, y) for x in (-1, 0, 1) for y in (-1, 0, 1)]
    squares.remove((0, 0))
    squares = map(lambda s: (square.x + s[0], square.y + s[1]), squares)
    squares = [[Square(s[0], s[1])] for s in squares if s[0] in BOARD and s[1] in BOARD]
    king_moves.cache[square] = squares
    return king_moves.cache[square]
king_moves.cache = {}


if __name__ == "__main__":
    print(pawn_moves(Square(5, 6), player=Player.BLACK))


    # print(pawn_moves(Square(1, 6), Player.WHITE))
    # print(pawn_moves(Square(1, 6), Player.WHITE))
