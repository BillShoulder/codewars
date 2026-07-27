"""  Codewars kata: Sudoku Solver. https://www.codewars.com/kata/sudoku-solver/train/python """

#######################################################################################################################
#
#   Import
#
#######################################################################################################################

from abc import ABC, abstractmethod, abstractproperty
from functools import cached_property
from collections import deque
from copy import deepcopy
from collections import namedtuple


#######################################################################################################################
#
#   State
#
#######################################################################################################################

class State(ABC):
    """ Abstract representation of a search state. """
    def __init__(self, model):
        self.model = model

    @abstractmethod
    def next(self):
        """ Yield all valid states obtainable from this state. """
        pass

    @abstractproperty
    def valid(self):
        """ Returns True if model is valid; otherwise False. """
        pass

    @abstractproperty
    def end(self):
        """ Returns True if this represents an end state; otherwise False. """
        pass


#######################################################################################################################
#
#   StateStream
#
#######################################################################################################################

class StateStream(ABC):
    """ Abstract representation of a stream of search states. """
    def __init__(self, state=None):
        self._stream_ = deque([state]) if state is not None else deque()

    @property
    def empty(self):
        return True if len(self._stream_) == 0 else False

    @abstractmethod
    def pop(self):
        pass

    @abstractmethod
    def push(self, state):
        pass


#######################################################################################################################
#
#   DepthFirstStateStream
#
#######################################################################################################################

class DepthFirstStateStream(StateStream):
    """ State stream specialized for depth first search. """
    def pop(self):
        return self._stream_.pop()

    def push(self, state):
        self._stream_.append(state)


#######################################################################################################################
#
#   SearchManager
#
#######################################################################################################################

class SearchManager:
    """ Generic class for managing searches. """
    def __init__(self, state_stream):
        self._state_stream_ = state_stream

    def resolutions(self):
        """ Yield successive state models that satisfy the end condition. """
        while not self._state_stream_.empty:
            state = self._state_stream_.pop()
            for new_state in state.next():
                self._state_stream_.push(new_state)
                if new_state.end:
                    yield new_state.model

    def resolution(self):
        """ Return the first state model that satisfies the end condition, or None if no such model exists. """
        return next(iter(self.resolutions()), None)


#######################################################################################################################
#
#   SudokoState
#
#######################################################################################################################

class SudokoState(State):
    all_digits = frozenset(range(1, 10))

    NextZero = namedtuple("NextZero", "row row_idx col col_idx")

    def __str__(self):
        return "\n".join(str(r) for r in self.model)

    def next(self):
        for digit in self.next_valid_digits:
            new_model = deepcopy(self.model)
            new_model[self.next_zero.row_idx][self.next_zero.col_idx] = digit
            new_state = SudokoState(new_model)
            if new_state.valid:
                yield SudokoState(new_model)            

    @cached_property
    def next_zero(self):
        for row_idx, row in enumerate(self.model):
            try:
                col_idx = row.index(0)
                col = tuple(self.model[n][col_idx] for n in range(len(self.model)))
                return self.NextZero(row=row, row_idx=row_idx, col=col, col_idx=col_idx)
            except ValueError: pass
        raise ValueError("No more zeros any more.")

    @cached_property
    def next_valid_digits(self):
        return self.all_digits - self.digits_in_next_column - self.digits_in_next_row - self.digits_in_next_box

    @cached_property
    def digits_in_next_row(self):
        return frozenset(n for n in self.next_zero.row if n != 0)

    @cached_property
    def digits_in_next_column(self):
        return frozenset(n for n in self.next_zero.col if n != 0)

    @cached_property
    def digits_in_next_box(self):
        digits = set()
        rbs = (self.next_zero.row_idx // 3) * 3
        cbs = (self.next_zero.col_idx // 3) * 3
        for r in range(rbs, rbs + 3):
            for c in range(cbs, cbs + 3):
                if self.model[r][c] != 0:
                    digits.add(self.model[r][c])
        return frozenset(digits)

    @cached_property
    def valid(self):
        """ True if model is valid; otherwise False. """
        return len(self._totals_) <= 1

    @cached_property
    def end(self):
        """ True if model represents an end state; otherwise False. """
        return next((row for row in self.model if 0 in row), None) is None and self.valid

    @cached_property
    def _rotated_model_(self):
        return list(zip(*self.model[::-1]))

    @cached_property
    def _merged_rotated_model_(self):
        return self.model + self._rotated_model_

    @cached_property
    def _totals_(self):
        return set(sum(row) for row in filter(lambda r: 0 not in r, self._merged_rotated_model_))

    @cached_property
    def total(self):
        return next(iter(self._totals_)) if len(self._totals_) == 1 else None


#######################################################################################################################
#
#   sudoku
#
#######################################################################################################################

def sudoku(puzzle):
    """return the solved puzzle as a 2d array of 9 x 9"""
    search_manager = SearchManager(DepthFirstStateStream(SudokoState(puzzle)))
    return search_manager.resolution()


#######################################################################################################################
#
#   __main__
#
#######################################################################################################################

if __name__ == "__main__":

    solution = [[5,3,4,6,7,8,9,1,2],
                [6,7,2,1,9,5,3,4,8],
                [1,9,8,3,4,2,5,6,7],
                [8,5,9,7,6,1,4,2,3],
                [4,2,6,8,5,3,7,9,1],
                [7,1,3,9,2,4,8,5,6],
                [9,6,1,5,3,7,2,8,4],
                [2,8,7,4,1,9,6,3,5],
                [3,4,5,2,8,6,1,7,9]]

    puzzle = [[5,3,0,0,7,0,0,0,0],
            [6,0,0,1,9,5,0,0,0],
            [0,9,8,0,0,0,0,6,0],
            [8,0,0,0,6,0,0,0,3],
            [4,0,0,8,0,3,0,0,1],
            [7,0,0,0,2,0,0,0,6],
            [0,6,0,0,0,0,2,8,0],
            [0,0,0,4,1,9,0,0,5],
            [0,0,0,0,8,0,0,7,9]]

    result = sudoku(puzzle)
    print(result == solution)










































#######################################################################################################################
#
#   DA CRYPT
#
#######################################################################################################################

# class SudokoState(State):
#     def next(self):
#         assert self.valid, f"Trying to determine children for invalid state:\n{str(self)}"
#         assert not self.end, f"Trying to determine children for end state:\n{str(self)}"
#         # Work on the most complete row containing some zeros.
#         best_row = min(filter(lambda r: 0 in r, self.model), key=lambda r: r.count(0))
#         best_row_idx = self.model.index(best_row)
#         best_row_total = sum(best_row)
#         # Is it possible to generate a valid row?
#         zero_indices = [idx for idx, val in enumerate(best_row) if val == 0]
#         zero_count = len(zero_indices)
#         target_start = self.total - best_row_total if self.total is not None else zero_count
#         target_end = target_start + 1 if self.total is not None else zero_count * 9 + 1
#         # print(f"best_row_idx: {best_row_idx}, best_row: {best_row}")
#         # print(f"target_range: {target_start}, {target_end}")
#         for target in range(target_start, target_end):
#             # print(f"target: {target}")
#             for part in partition(target, parts=zero_count, part_min=1, part_max=9):
#                 # print(f"part: {part}")
#                 new_model = deepcopy(self.model)
#                 for count, zero_index in enumerate(zero_indices):
#                     new_model[best_row_idx][zero_index] = part[count]
#                 new_state = SudokoState(new_model)
#                 # print(new_state)
#                 if new_state.valid: yield new_state

#     def __str__(self):
#         return "\n".join(str(r) for r in self.model)

#     @cached_property
#     def valid(self):
#         """ True if model is valid; otherwise False. """
#         return len(self._totals_) <= 1

#     @cached_property
#     def end(self):
#         """ True if model represents an end state; otherwise False. """
#         return next((row for row in self.model if 0 in row), None) is None and self.valid

#     @cached_property
#     def _rotated_model_(self):
#         """ The model array rotated 90 degrees. """
#         return list(zip(*self.model[::-1]))

#     @cached_property
#     def _merged_rotated_model_(self):
#         """  """
#         return self.model + self._rotated_model_

#     @cached_property
#     def _totals_(self):
#         return set(sum(row) for row in filter(lambda r: 0 not in r, self._merged_rotated_model_))

#     @cached_property
#     def total(self):
#         return next(iter(self._totals_)) if len(self._totals_) == 1 else None

#     @cached_property
#     def _shortest_row_(self):
#         return min(enumerate(solution), key=lambda tup: tup[1].count(0))




#######################################################################################################################
#
#   SudokoState
#
#######################################################################################################################

# class SudokoState(State):
#     def next(self):
#         assert self.valid, f"Trying to determine children for invalid state:\n{str(self)}"
#         assert not self.end, f"Trying to determine children for end state:\n{str(self)}"
#         # Work on the most complete row containing some zeros.
#         best_row_idx, best_row = min(enumerate(filter(lambda r: 0 in r, self.model)), key=lambda tup: tup[1].count(0))
#         best_row_total = sum(best_row)
#         # Is it possible to generate a valid row?
#         zero_indices = [idx for idx, val in enumerate(best_row) if val == 0]
#         zero_count = len(zero_indices)
#         target_start = self.total - best_row_total if self.total is not None else zero_count
#         target_end = target_start + 1 if self.total is not None else zero_count * 9 + 1
#         print(f"best_row_idx: {best_row_idx}, best_row: {best_row}")
#         print(f"target_range: {target_start}, {target_end}")
#         for target in range(target_start, target_end):
#             print(f"target: {target}")
#             for part in partition(target, parts=zero_count, part_min=1, part_max=9):
#                 print(f"part: {part}")
#                 new_model = deepcopy(self.model)
#                 for count, zero_index in enumerate(zero_indices):
#                     new_model[best_row_idx][zero_index] = part[count]
#                 new_state = SudokoState(new_model)
#                 print(new_state)
#                 if new_state.valid: yield new_state

#     def __str__(self):
#         return "\n".join(str(r) for r in self.model)

#     @cached_property
#     def valid(self):
#         """ True if model is valid; otherwise False. """
#         return len(self._totals_) <= 1

#     @cached_property
#     def end(self):
#         """ True if model represents an end state; otherwise False. """
#         return next((row for row in self.model if 0 in row), None) is None and self.valid

#     @cached_property
#     def _rotated_model_(self):
#         """ The model array rotated 90 degrees. """
#         return list(zip(*self.model[::-1]))

#     @cached_property
#     def _merged_rotated_model_(self):
#         """  """
#         return self.model + self._rotated_model_

#     @cached_property
#     def _totals_(self):
#         return set(sum(row) for row in filter(lambda r: 0 not in r, self._merged_rotated_model_))

#     @cached_property
#     def total(self):
#         return next(iter(self._totals_)) if len(self._totals_) == 1 else None

#     @cached_property
#     def _shortest_row_(self):
#         return min(enumerate(solution), key=lambda tup: tup[1].count(0))





    # def next(self):
    #     """ Yield all valid states obtainable from this state. """
    #     # The next states are valid states with the next zero in the matrix filled with values from 1-9.
    #     for row_idx, row in enumerate(self.model):
    #         try:
    #             col_idx = row.index(0)
    #             for n in range(1, 10):
    #                 new_model = deepcopy(self.model)
    #                 new_model[row_idx][col_idx] = n
    #                 new_state = SudokoState(new_model)
    #                 if new_state.valid: yield new_state
    #             break
    #         except ValueError: pass