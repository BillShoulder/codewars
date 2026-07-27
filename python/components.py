"""
Codewars kata: Count Connectivity Components

https://www.codewars.com/kata/5856f3ecf37aec45e6000091/train/python
"""

#######################################################################################################################
#
#   Import
#
#######################################################################################################################

from collections import namedtuple, Counter
from itertools import chain


#######################################################################################################################
#
#   Grid
#
#######################################################################################################################

class Grid:
    Cell = namedtuple("Cell", "x y")

    @property
    def width(self):
        return int((len(self._grid_[0]) - 1) / 2)

    @property
    def height(self):
        return int((len(self._grid_) - 1) / 2)

    def __init__(self, grid):
        grid = grid.split("\n")
        row_range = range(len(grid[0]))
        for idx, row in enumerate(grid):
            grid[idx] = "".join(row[i] for i in row_range if (i + 1) % 3 != 0)
        self._grid_ = grid

    def __iter__(self):
        for x in range(self.width):
            for y in range(self.height):
                yield self.Cell(x, y)

    def neighbors(self, cell):
        gridx = cell.x * 2 + 1
        gridy = cell.y * 2 + 1
        neighbors = set([cell])
        for n in (-1, 1):
            if self._grid_[gridy][gridx + n] == " ":
                neighbors.add(self.Cell(cell.x + n, cell.y))
            if self._grid_[gridy+n][gridx] == " ":
                neighbors.add(self.Cell(cell.x, cell.y + n))
        return neighbors


#######################################################################################################################
#
#   components
#
#######################################################################################################################

def components(grid):
    bucket_list = []
    grid = Grid(grid)
    for cell in grid:
        neighbors = grid.neighbors(cell)
        buckets = [b for b in bucket_list if any(c for c in neighbors if c in b)]
        if len(buckets) == 0:
            bucket_list.append(neighbors)
        elif len(buckets) == 1:
            buckets[0] |= neighbors
        else:
            bucket_list = [b for b in bucket_list if b not in buckets[1:]]
            buckets[0].update(chain.from_iterable(buckets[1:]))
            buckets[0] |= neighbors
    length_counter = Counter([len(bucket) for bucket in bucket_list])
    return sorted([(k, v) for k, v in length_counter.items()], reverse=True)


#######################################################################################################################
#
#   __main__
#
#######################################################################################################################

if __name__ == "__main__":
    test1 = '''\
+--+--+--+--+--+--+--+--+--+--+
|  |     |     |     |  |  |  |
+--+--+  +--+  +--+--+--+  +--+
|  |  |  |  |     |           |
+--+  +--+--+--+--+  +--+  +  +
|  |     |  |  |        |  |  |
+--+--+  +--+--+--+--+  +--+  +
|  |  |  |  |              |  |
+  +--+  +--+--+  +--+--+--+--+
|     |  |        |  |  |  |  |
+--+  +--+--+--+--+--+--+--+  +
|  |  |        |  |  |     |  |
+  +--+  +--+--+--+  +--+--+--+
|     |  |  |     |  |  |  |  |
+--+--+--+--+  +  +--+--+--+--+
|     |     |        |        |
+--+  +--+--+--+  +--+--+--+--+
|  |  |     |     |  |  |     |
+--+  +--+  +--+--+--+--+  +--+
|  |        |     |     |  |  |
+--+--+--+--+--+--+--+--+--+--+'''

    assert components(test1) == [(19, 1), (8, 1), (7, 1), (5, 1), (4, 3), (3, 4), (2, 7), (1, 23)]
