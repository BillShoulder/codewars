"""
    Yet another Priority Queue implementation.

    Based upon the heapq Priority Queue Implementation Notes: https://docs.python.org/3/library/heapq.html
"""

#######################################################################################################################
#
#   Import
#
#######################################################################################################################

from itertools import count
from heapq import heappush, heappop


#######################################################################################################################
#
#   PriorityQueue
#
#######################################################################################################################

class PriorityQueue:
    """ Yet another Priority Queue implementation. """
    REMOVED = None

    def __init__(self):
        self._pq_ = []
        self._entry_finder_ = {}
        self._counter_ = count()

    def add(self, item, priority=0):
        entry = [priority, next(self._counter_), item]
        try:
            existing_entry = self._entry_finder_[item]
            if not self.update_entry(existing_entry, entry):
                return
            self.remove(item)
        except KeyError: pass
        self._entry_finder_[item] = entry
        heappush(self._pq_, entry)

    def update_entry(self, existing_entry, entry):
        return True

    def remove(self, item):
        entry = self._entry_finder_.pop(item)
        entry[-1] = self.REMOVED

    def pop(self):
        while self._pq_:
            priority, count, item = heappop(self._pq_)
            if item is not self.REMOVED:
                del self._entry_finder_[item]
                return priority, item
