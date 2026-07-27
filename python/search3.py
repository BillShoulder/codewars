""" Revised generic search algorithm implementation with specializations for breadth first and deapth first search. """

#######################################################################################################################
#
#   Import
#
#######################################################################################################################

from abc import ABC, abstractmethod, abstractproperty
from collections import deque

from compatibility import cached_property



#######################################################################################################################
#
#   State
#
#######################################################################################################################

class State(ABC):
    """ Abstract representation of a search state. """

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

    @abstractproperty
    def summary(self):
        """ Return a unique, hashable summary of this state. """
        pass


#######################################################################################################################
#
#   StateStream
#
#######################################################################################################################

class StateStream(ABC):
    """ Abstract representation of a stream of search states. """
    def __init__(self, state=None):
        self._state_ = state

    @cached_property
    def _stream_(self):
        """ State stream container. """
        return deque([self._state_]) if self._state_ is not None else deque()

    @property
    def empty(self):
        """ Returns True if the search stream is empty; otherwise False. """
        return True if len(self._stream_) == 0 else False

    @abstractmethod
    def pop(self):
        """ Remove and return a state from the state stream. """
        pass

    @abstractmethod
    def push(self, state):
        """ Add a state to the state stream. """
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
#   RankedStateStream
#
#######################################################################################################################

class RankedStateStream(StateStream):
    """ State stream specialized for ranked search. """

    def pop(self):
        index, item = max(enumerate(self._stream_), key=lambda tup: tup[1].score)
        del self._stream_[index]
        return item

    def push(self, state):
        self._stream_.appendleft(state)


#######################################################################################################################
#
#   BreadthFirstStateStream
#
#######################################################################################################################

class BreadthFirstStateStream(StateStream):
    """ State stream specialized for breadth first search. """
    def pop(self):
        return self._stream_.pop()

    def push(self, state):
        self._stream_.appendleft(state)


#######################################################################################################################
#
#   SearchManager
#
#######################################################################################################################

class SearchManager:
    """ Generic class for managing searches. """
    def __init__(self, state_stream):
        self._state_stream_ = state_stream
        self._visited_ = set()

    def resolutions(self):
        """ Yield successive states that satisfy the end condition. """
        iterations = 0
        self._visited_ = set()
        while not self._state_stream_.empty:
            iterations += 1
            state = self._state_stream_.pop()
            self.visit(state)
            if state.end:
                yield state
            for new_state in state.next():
                if not self.visited(new_state):
                    self._state_stream_.push(new_state)

    def resolution(self):
        """ Return the first state model that satisfies the end condition, or None if no such model exists. """
        return next(iter(self.resolutions()), None)

    def visit(self, state):
        """ Note that state has been explored. """
        self._visited_.add(state.summary)

    def visited(self, state):
        """ Returns True if state has been explored; otherwise False. """
        return state.summary in self._visited_

    