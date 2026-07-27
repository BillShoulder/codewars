""" Codewars kata: Hard Sudoku Solver. https://www.codewars.com/kata/hard-sudoku-solver-1/train/python """

#######################################################################################################################
#
#   Import
#
#######################################################################################################################

from copy import deepcopy
from itertools import chain
from collections import namedtuple
import numpy as np

from search import State, DepthFirstStateStream, SearchManager
from compatibility import cached_property


#######################################################################################################################
#
#   SudokoState
#
#######################################################################################################################

class SudokoState(State):
    class InvalidSquare(ValueError): pass

    NextZero = namedtuple("NextZero", "row col")

    all_digits = frozenset(range(1, 10))

    def __str__(self):
        return "\n".join(str(r) for r in self.model)

    def next(self):
        if self.next_zero is not None:
            for digit in filter(self.digit_valid, self.next_digits):
                new_model = np.copy(self.model)
                new_model[self.next_zero.row][self.next_zero.col] = digit
                yield SudokoState(new_model)

    def digit_valid(self, digit):
        if self.total is not None:
            col_total = self.zero_col_sum + digit
            if col_total > self.total: return False
            elif self.zero_col_count == 1 and col_total != self.total: return False
            row_total = self.zero_row_sum + digit
            if self.zero_row_sum + digit > self.total: return False
            elif self.zero_row_count == 1 and row_total != self.total: return False
        return True

    @cached_property
    def next_zero(self):
        result = np.argwhere(self.model==0)
        return None if result[0].size == 0 else self.NextZero(row=result[0][0], col=result[0][1])

    @cached_property
    def zero_row(self):
        return self.model[self.next_zero.row]

    @cached_property
    def zero_col(self):
        return self.model[:,self.next_zero.col]

    @cached_property
    def zero_row_sum(self):
        return np.sum(self.zero_row)

    @cached_property
    def zero_row_count(self):
        return np.count_nonzero(self.zero_row==0)

    @cached_property
    def zero_col_sum(self):
        return np.sum(self.zero_col)

    @cached_property
    def zero_col_count(self):
        return np.count_nonzero(self.zero_col==0)

    @cached_property
    def next_digits(self):
        return self.all_digits - set(self.zero_row) - set(self.zero_col) - self.digits_in_next_box
        
    @cached_property
    def digits_in_next_box(self):
        digits = set()
        rbs = (self.next_zero.row // 3) * 3
        cbs = (self.next_zero.col // 3) * 3
        for r in range(rbs, rbs + 3):
            for c in range(cbs, cbs + 3):
                digits.add(self.model[r][c])
        return digits

    @cached_property
    def total(self):
        total = None
        for row in self.model:
            if 0 not in row:
                t = np.sum(row)
                if total is None: total = t
                elif t != total: raise InvalidSquare
        for row in np.rot90(self.model):
            if 0 not in row:
                t = np.sum(row)
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
        return 0 not in self.model


#######################################################################################################################
#
#   sudoku_solver
#
#######################################################################################################################

def sudoku_solver(puzzle):
    puzzle = np.array(puzzle)
    # Check the groundrules.
    if len(puzzle) != 9 or any(r for r in puzzle if len(r) != 9) or any(c for c in chain.from_iterable(puzzle) if c not in range(10)):
        raise ValueError("Invalid grid!")
    # The minimum of givens required to create a unique (with no multiple solutions) sudoku game is 17.
    if len([c for c in chain.from_iterable(puzzle) if c != 0]) < 17:
        raise ValueError("No unique solution")
    # Seek solutions.
    search_manager = SearchManager(DepthFirstStateStream(SudokoState(puzzle)))
    solution_iterator = iter(search_manager.resolutions())
    solution = next(solution_iterator, None)
    # print(solution)
    # if solution is None or next(solution_iterator, None) is not None:
    #     raise ValueError("No unique solution")
    return np.ndarray.tolist(solution)


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


    test = [[5, 4, 0, 1, 2, 0, 9, 5, 0], 
                [0, 8, 0, 6, 9, 4, 1, 3, 2], 
                [2, 1, 9, 3, 0, 5, 4, 6, 7], 
                [4, 6, 2, 5, 3, 1, 8, 7, 9], 
                [9, 3, 1, 2, 7, 8, 6, 4, 5], 
                [8, 5, 7, 0, 4, 6, 2, 1, 3], 
                [5, 9, 8, 4, 1, 3, 7, 2, 6],
                [6, 2, 4, 7, 5, 9, 3, 8, 1],
                [1, 7, 3, 8, 0, 2, 5, 9, 4]]




    # npthing = np.array(solution)
    # zero = np.where(npthing==0)
    # print(zero[0].size)
    # print(zero[0][0], zero[1][0])
    # exit()

    # result = sudoku_solver(puzzle)
    # assert result == solution, "You done goofed."
    # exit()

    # state = SudokoState(np.array(test))
    # print(state.zero_row)
    # print(state.zero_row_count)
    # print(state.zero_row_sum)
    # print()
    # print(state.zero_col)
    # print(state.zero_col_count)
    # print(state.zero_col_sum)

    # exit()


    # result = sudoku_solver(puzzle)
    # assert result == solution, "You done goofed."
    # exit()


    samples = 10
    repetitions = 10

    print("Start")
    times = []
    for _ in range(samples):
        start = default_timer()
        for _ in range(repetitions):
            result = sudoku_solver(puzzle)
            assert result == solution, "You done goofed."
        times.append(default_timer() - start)

    print(f"Avg: {mean(times)}, pstdev: {pstdev(times)}")
    

