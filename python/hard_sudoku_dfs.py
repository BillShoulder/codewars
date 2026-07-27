""" Codewars kata: Hard Sudoku Solver. https://www.codewars.com/kata/hard-sudoku-solver-1/train/python """

"""
This implementation pushes brute-force, depth-first search about as far as I can take it.

Doesn't meet the performance criteria for the kata.
"""

#######################################################################################################################
#
#   Import
#
#######################################################################################################################

from collections import namedtuple
from itertools import chain
from pprint import pprint

from search import State, DepthFirstStateStream, SearchManager
from compatibility import cached_property


#######################################################################################################################
#
#   SudokoState
#
#######################################################################################################################

class SudokoState(State):
    class InvalidSquare(ValueError): pass

    all_digits = frozenset(range(1, 10))

    NextZero = namedtuple("NextZero", "row row_idx col col_idx")

    def __str__(self):
        return "\n".join(str(r) for r in self.model)

    def next(self):
        if self.next_zero is not None:
            for digit in self.next_digits:
                new_model = [row[:] for row in self.model]
                new_model[self.next_zero.row_idx][self.next_zero.col_idx] = digit
                yield SudokoState(new_model)

    @cached_property
    def next_zero(self):
        for row_idx, row in enumerate(self.model):
            try:
                col_idx = row.index(0)
                col = tuple(self.model[n][col_idx] for n in range(len(self.model)))
                return self.NextZero(row=row, row_idx=row_idx, col=col, col_idx=col_idx)
            except ValueError: pass
        return None

    @cached_property
    def zero_row_sum(self):
        return sum(self.next_zero.row)

    @cached_property
    def zero_row_count(self):
        return self.next_zero.row.count(0)

    @cached_property
    def zero_col_sum(self):
        return sum(self.next_zero.col)

    @cached_property
    def zero_col_count(self):
        return self.next_zero.col.count(0)

    @cached_property
    def next_digits(self):
        return self.all_digits - set(self.next_zero.col) - set(self.next_zero.row) - self.digits_in_next_box
        
    @cached_property
    def digits_in_next_box(self):
        rbs = (self.next_zero.row_idx // 3) * 3
        cbs = (self.next_zero.col_idx // 3) * 3
        return set(chain.from_iterable([self.model[row][cbs:cbs + 3] for row in range(rbs, rbs + 3)]))

    @cached_property
    def total(self):
        total = None
        for row in self.model:
            if 0 not in row:
                t = sum(row)
                if total is None: total = t
                elif t != total: raise InvalidSquare
        for row in zip(*self.model[::-1]):
            if 0 not in row:
                t = sum(row)
                if total is None: total = t
                elif t != total: raise InvalidSquare       
        return total

    @cached_property
    def valid(self):
        try:
            self.total
        except self.InvalidSquare:
            return False
        return True

    @cached_property
    def end(self):
        return not any(row for row in self.model if 0 in row)


#######################################################################################################################
#
#   sudoku_solver
#
#######################################################################################################################

def sudoku_solver(puzzle):
    # Check the groundrules.
    if len(puzzle) != 9 or any(r for r in puzzle if len(r) != 9) or any(c for c in chain.from_iterable(puzzle) if c not in range(10)):
        raise ValueError("Invalid grid!")
    # The minimum of givens required to create a unique (with no multiple solutions) sudoku game is 17.
    given =  len([c for c in chain.from_iterable(puzzle) if c != 0])
    print(f"Given values: {given}")
    if given < 17: raise ValueError("No unique solution")
    # Seek solutions.
    search_manager = SearchManager(DepthFirstStateStream(SudokoState(puzzle)))
    return search_manager.resolution()


#######################################################################################################################
#
#   __main__
#
#######################################################################################################################

if __name__ == "__main__":
    from timeit import default_timer
    from statistics import pstdev, mean

    puzzle = [[0, 0, 6, 1, 0, 0, 0, 0, 8], 
            [0, 8, 0, 0, 9, 0, 0, 3, 0], 
            [2, 0, 0, 0, 0, 5, 4, 0, 0], 
            [4, 0, 0, 0, 0, 1, 8, 0, 0], 
            [0, 3, 0, 0, 7, 0, 0, 4, 0], 
            [0, 0, 7, 9, 0, 0, 0, 0, 3], 
            [0, 0, 8, 4, 0, 0, 0, 0, 6], 
            [0, 2, 0, 0, 5, 0, 0, 8, 0], 
            [1, 0, 0, 0, 0, 2, 5, 0, 0]]

    solution = [[3, 4, 6, 1, 2, 7, 9, 5, 8], 
                [7, 8, 5, 6, 9, 4, 1, 3, 2], 
                [2, 1, 9, 3, 8, 5, 4, 6, 7], 
                [4, 6, 2, 5, 3, 1, 8, 7, 9], 
                [9, 3, 1, 2, 7, 8, 6, 4, 5], 
                [8, 5, 7, 9, 4, 6, 2, 1, 3], 
                [5, 9, 8, 4, 1, 3, 7, 2, 6],
                [6, 2, 4, 7, 5, 9, 3, 8, 1],
                [1, 7, 3, 8, 6, 2, 5, 9, 4]]


    test = [[0, 0, 6, 1, 0, 0, 0, 0, 8], 
            [0, 8, 0, 0, 9, 0, 0, 0, 0], 
            [2, 0, 0, 0, 0, 5, 4, 0, 0], 
            [0, 0, 0, 0, 0, 1, 0, 0, 0], 
            [0, 3, 0, 0, 7, 0, 0, 4, 0], 
            [0, 0, 7, 9, 0, 0, 0, 0, 3], 
            [0, 0, 0, 4, 0, 0, 0, 0, 6], 
            [0, 2, 0, 0, 5, 0, 0, 8, 0], 
            [1, 0, 0, 0, 0, 2, 0, 0, 0]]


    samples = 10
    repetitions = 1

    print("Start")
    times = []
    for _ in range(samples):
        start = default_timer()
        for _ in range(repetitions):
            result = sudoku_solver(test)
            pprint(result)
            for row in result: print(sum(row))
            for row in zip(*result[::-1]): print(sum(row))
            # assert result == solution, "You done goofed."
        times.append(default_timer() - start)

    print(f"Avg: {mean(times)}, pstdev: {pstdev(times)}")
    

