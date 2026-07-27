"""
Codewars kata: 4 By 4 Skyscrapers

https://www.codewars.com/kata/5671d975d81d6c1c87000022/train/python
"""

#######################################################################################################################
#
#   Import
#
#######################################################################################################################

from collections import deque, namedtuple
from compatibility import cached_property


#######################################################################################################################
#
#   GridNode
#
#######################################################################################################################

class GridNode:
    GRID_DIM = 4
    GRID_SIZE = GRID_DIM ** 2
    GRID_VALUES = set(range(1, GRID_DIM + 1))

    Cell = namedtuple("Cell", "x y")
    CellClues = namedtuple("CellClues", "top left bottom right")

    def __init__(self, clues, grid):
        self.clues = clues
        self.grid = grid

    @cached_property
    def end(self):
        return len(self.grid) == self.GRID_SIZE

    def children(self):
        for value in self.next_values:
            if self.valid_next_value(value):
                yield GridNode(clues=self.clues, grid=self.grid + [value])

    @cached_property
    def next_values(self):
        """ Return a set containing values used in the row and colum corresponding to the next cell to be filled. """
        return self.GRID_VALUES - set(self.next_row_values) - set(self.next_col_values)

    def valid_next_value(self, value):
        """ Return True if using value as the next cell to be filled violates no constraints from clues; otherwise False. """
        return (self.valid_sequence(self.next_row_values + [value], self.next_clues.left, self.next_clues.right) and
               self.valid_sequence(self.next_col_values + [value], self.next_clues.top, self.next_clues.bottom))

    @cached_property
    def next_cell(self):
        """ A cell representing the next available position at which a value can be added to grid. """
        return self.cell_from_index(len(self.grid))

    @cached_property
    def next_row_values(self):
        """ A left to right ORDERED list of values in the row containing next_cell. """
        return [self.grid[self.index_from_cell(self.Cell(x, self.next_cell.y))] for x in range(self.next_cell.x)]

    @cached_property
    def next_col_values(self):
        """ A top to bottom ORDERED list of values in the column containing next_cell. """
        return [self.grid[self.index_from_cell(self.Cell(self.next_cell.x, y))] for y in range(self.next_cell.y)]

    @cached_property
    def next_clues(self):
        top = self.clues[self.next_cell.x]
        right = self.clues[self.GRID_DIM + self.next_cell.y]
        bottom = self.clues[3 * self.GRID_DIM - 1 - self.next_cell.x]
        left = self.clues[4 * self.GRID_DIM - 1 - self.next_cell.y]
        return self.CellClues(top=top, right=right, bottom=bottom, left=left)

    @classmethod
    def count_visible(cls, seq, max_height=0):
        """ Return tuple: (number of 'visible' items in seq, height of 'highest' visible item), from left to right. """
        visible = 0
        for height in seq:
            if height > max_height:
                max_height = height
                visible += 1
        return visible    

    @classmethod
    def valid_sequence(cls, seq, clue_start, clue_end):
        """ Return True if seq is valid, given clue_start, clue_end; otherwise False. """
        # If we haven't a clue, then it's all good.
        if not clue_start and not clue_end:
            return True
        available_values = cls.GRID_VALUES - set(seq)
        max_height = max(seq)
        # Valid from clue_start?
        if clue_start:
            visible_cout = cls.count_visible(seq)
            # Too many?
            extra_visible = 1 if any(v for v in available_values if v > max_height) else 0
            if visible_cout + extra_visible > clue_start:
                return False
            # Too few?
            extra_visible = sum(1 for v in available_values if v > max_height)
            if visible_cout + extra_visible < clue_start:
                return False        
        # Valid from right?
        if clue_end:
            max_available = max(available_values) if available_values else 0
            visible = cls.count_visible(seq=reversed(seq), max_height=max_available)
            # Too many?
            visible_min = 1 if max_available > max_height else visible + int(max_available != 0)
            if visible_min > clue_end:
                return False
            # Too few?
            visible_max = visible + len(available_values)
            if visible_max < clue_end:
                return False
        return True

    @classmethod
    def cell_from_index(cls, index):
        """ Convert index in self.grid into an (x, y) cell on an imaginary grid. """
        return cls.Cell(*reversed(divmod(index, cls.GRID_DIM)))

    @classmethod
    def index_from_cell(cls, cell):
        """ Convert cell coordinates on an imaginary grid to a corresponding index in self.grid """
        return cell.y * cls.GRID_DIM + cell.x


#######################################################################################################################
#
#   solve_puzzle
#
#######################################################################################################################

def solve_puzzle(clues):
    open_nodes = deque([GridNode(clues=clues, grid=[])])
    while open_nodes:
        node = open_nodes.pop()
        if node.end:
            print(node.grid)
            result = tuple(tuple(node.grid[n * GridNode.GRID_DIM : n * GridNode.GRID_DIM + GridNode.GRID_DIM]) for n in range(GridNode.GRID_DIM))
            return result
        open_nodes.extend(node.children())


#######################################################################################################################
#
#   __main__
#
#######################################################################################################################

if __name__ == "__main__":
    clues = ( 0, 0, 1, 2,   
        0, 2, 0, 0,   
        0, 3, 0, 0, 
        0, 1, 0, 0 )
    result = solve_puzzle(clues=clues)
    for r in result:
        print(r)






#######################################################################################################################
#
#   Most concise solution
#
#######################################################################################################################

from itertools import permutations, chain

def solve_puzzle_concise(clues):
    # https://www.codewars.com/kata/reviews/58b357af6f4276166d001c86/groups/58f211cf3e42b053e20000a8
    size = 4
    for poss in permutations(permutations(range(1, size+1), size), size):
        for i in range(size):
            if len(set(row[i] for row in poss)) < size:
                break
        else:
            cols_top = [[row[i] for row in poss] for i in range(size)]
            rows_right = [list(reversed(row)) for row in poss]
            cols_btm = [[row[i] for row in reversed(poss)] for i in reversed(range(size))]
            rows_left = list(reversed(poss))
            for i, row in enumerate(chain(cols_top, rows_right, cols_btm, rows_left)):
                if not clues[i]:
                    continue
                visible = 0
                for j, v in enumerate(row):
                    visible += v >= max(row[:j+1])
                if visible != clues[i]:
                    break
            else:
                return poss


