""" Codewars kata: Check and Mate?. https://www.codewars.com/kata/52fcc820f7214727bc0004b7/train/python """

"""
{
  'piece': string, # pawn, rook, knight, bishop, queen or king
  'owner': int,    # 0 for white or 1 for black
  'x': int,        # 0-7 where 0 is the leftmost column (or "A")
  'y': int,        # 0-7 where 0 is the top row (or "8" in the board below)
  'prevX': int,    # 0-7, presents this piece's previous x, only given if this is the piece that was just moved
  'prevY': int     # 0-7, presents this piece's previous y, only given if this is the piece that was just moved
}
"""

#######################################################################################################################
#
#   Import
#
#######################################################################################################################

from itertools import chain
from copy import deepcopy

from compatibility import cached_property
from chess import Square, Player, pawn_moves, rook_moves, knight_moves, bishop_moves, queen_moves, king_moves


#######################################################################################################################
#
#   get_square
#
#######################################################################################################################

def get_square(piece):
    return Square(piece["x"], piece["y"])


#######################################################################################################################
#
#   ChessPosition
#
#######################################################################################################################

class ChessPosition:
    
    def __init__(self, pieces, player):
        self.pieces = pieces
        self.player = player

    @cached_property
    def square_to_piece_map(self):
        return {get_square(piece): piece for piece in self.pieces}

    @cached_property
    def is_check(self):
        threats = []
        king_square = get_square(next(piece for piece in self.pieces if piece["owner"] == self.player and piece["piece"] == "king"))
        for piece in filter(lambda p: p["owner"] != self.player, self.pieces):
            if any(s for s in self.moves(piece) if s == king_square):
                threats.append(piece)
        return threats if threats else False

    @cached_property
    def is_mate(self):
        if not self.is_check:
            return False
        for piece in filter(lambda p: p["owner"] == self.player, self.pieces):
            piece_square = get_square(piece)
            for square in self.moves(piece):
                new_position = self.move(piece_square, square)
                new_position.player = self.player
                if not new_position.is_check:
                    return False
        return True 

    def move(self, start_square, end_square):
        pieces = deepcopy(self.pieces)
        piece = next(p for p in pieces if p["x"] == start_square.x and p["y"] == start_square.y)
        end_piece = None
        if self.occupant(start_square)["piece"] == "pawn" and start_square.x != end_square.x and self.occupant(end_square) is None:
            # Special case en passant.
            end_piece = self.occupant(Square(end_square.x, start_square.y))
        else:
            end_piece = next((p for p in pieces if p["x"] == end_square.x and p["y"] == end_square.y), None)
        if end_piece is not None:
            pieces.remove(end_piece)
        piece["x"] = end_square.x
        piece["y"] = end_square.y
        return ChessPosition(pieces=pieces, player=int(not self.player))

    def moves(self, piece):
        square_router = {"pawn":    self.pawn_moves,
                         "rook":    self.rook_moves,
                         "knight":  self.knight_moves,
                         "bishop":  self.bishop_moves,
                         "queen":   self.queen_moves,
                         "king":    self.king_moves}
        return square_router[piece["piece"]](piece)

    def pawn_moves(self, piece):
        def double_moved(piece):
            prevX = piece.get("prevX")
            prevY = piece.get("prevY")
            if prevX is None or prevY is None:
                return False
            return prevX == piece["x"] and abs(prevY - piece["y"]) == 2

        pawn_square = get_square(piece)
        squares = pawn_moves(pawn_square, piece["owner"])
        squares = set() if squares and self.occupied(squares[0][0]) else set(s for s in chain.from_iterable(squares) if not self.occupied(s))
        direction = 1 if piece["owner"] == Player.BLACK else -1
        # Capture
        for x in (-1, +1):
            # Diagonal
            square = Square(pawn_square.x + x, pawn_square.y + direction)
            occupant = self.occupant(square)
            if occupant is not None and occupant["owner"] != piece["owner"]:
                squares.add(square)
            # En passant
            square = Square(pawn_square.x + x, pawn_square.y)
            occupant = self.occupant(square)
            if occupant is not None and occupant["owner"] != piece["owner"] and occupant["piece"] == "pawn" and double_moved(occupant):
                squares.add(Square(square.x, square.y + direction))
        return squares

    def rook_moves(self, piece):
        squares = rook_moves(get_square(piece))
        squares = self.filter_blocked(squares, piece)
        return set(chain.from_iterable(squares))

    def knight_moves(self, piece):
        squares = knight_moves(get_square(piece))
        return set(s for s in chain.from_iterable(squares) if not self.occupied(s) or self.occupant(s)["owner"] != piece["owner"])

    def bishop_moves(self, piece):
        squares = bishop_moves(get_square(piece))
        squares = self.filter_blocked(squares, piece)
        return set(chain.from_iterable(squares))

    def queen_moves(self, piece):
        squares = queen_moves(get_square(piece))
        squares = self.filter_blocked(squares, piece)
        return set(chain.from_iterable(squares))

    def king_moves(self, piece):
        # TODO: castling
        squares = king_moves(get_square(piece))
        squares = self.filter_blocked(squares, piece)
        return set(chain.from_iterable(squares))

    def occupant(self, square):
        return self.square_to_piece_map.get(square)

    def occupied(self, square):
        return self.occupant(square) is not None

    def filter_blocked(self, squares, piece):
        # TODO: Avoid unnecessary duplication.
        squares = deepcopy(squares)
        for vector in squares:
            for idx, square in enumerate(vector):
                occupant = self.occupant(square)
                if occupant is None:
                    continue
                vector = vector[:idx] if occupant["owner"] == piece["owner"] else vector[:idx+1]
                break
        return filter(None, squares)


#######################################################################################################################
#
#   isCheck
#
#######################################################################################################################

def isCheck(pieces, player):
    return ChessPosition(pieces, player).is_check


#######################################################################################################################
#
#   isMate
#
#######################################################################################################################

def isMate(pieces, player):
    return ChessPosition(pieces, player).is_mate


#######################################################################################################################
#
#   __main__
#
#######################################################################################################################

if __name__ == "__main__":
    pieces = [
        {'piece': "king", 'owner': 1, 'x': 4, 'y': 0},
        {'piece': "king", 'owner': 0, 'x': 4, 'y': 7},
        {'piece': "pawn", 'owner': 0, 'x': 5, 'y': 6}
    ]

    print(f"Check: {isCheck(pieces, 0)}")
    print(f"Mate: {isMate(pieces, 0)}")
