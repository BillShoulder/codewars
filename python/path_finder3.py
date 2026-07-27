"""
Codewars kata: Path Finder #3: the Alpinist

https://www.codewars.com/kata/576986639772456f6f00030c/train/python
"""

#######################################################################################################################
#
#   Import
#
#######################################################################################################################

from collections import namedtuple

from priority_queue import PriorityQueue


#######################################################################################################################
#
#   Position
#
#######################################################################################################################

Position = namedtuple("Position", "x y")


#######################################################################################################################
#
#   Queue
#
#######################################################################################################################

class Queue(PriorityQueue):
    def update_entry(self, existing_entry, entry):
        return entry[0] < existing_entry[0]


#######################################################################################################################
#
#   path_finder
#
#######################################################################################################################

def path_finder(area):
    area = area.split()
    end = Position(x=len(area)-1, y=len(area)-1)
    bounds = range(len(area))
    pq = Queue()
    pq.add(Position(x=0, y=0))
    closed = set()
    while pq:
        cost, position = pq.pop()
        if position == end:
            return cost
        closed.add(position)
        next_positions = [Position(x=position.x-1, y=position.y),
                          Position(x=position.x+1, y=position.y),
                          Position(x=position.x, y=position.y-1),
                          Position(x=position.x, y=position.y+1)]
        for np in filter(lambda p: p.x in bounds and p.y in bounds and p not in closed, next_positions):
            pq.add(np, cost + abs(int(area[np.y][np.x]) - int(area[position.y][position.x])))
    raise Exception(f"No route to {end}")


#######################################################################################################################
#
#   __main__
#
#######################################################################################################################

if __name__ == "__main__":
    dodgy = "\n".join([
    "546",
    "019",
    "032"
    ])

    a = "\n".join([
    "000",
    "000",
    "000"
    ])

    b = "\n".join([
    "010",
    "010",
    "010"
    ])

    c = "\n".join([
    "010",
    "101",
    "010"
    ])

    d = "\n".join([
    "0707",
    "7070",
    "0707",
    "7070"
    ])

    e = "\n".join([
    "700000",
    "077770",
    "077770",
    "077770",
    "077770",
    "000007"
    ])

    f = "\n".join([
    "777000",
    "007000",
    "007000",
    "007000",
    "007000",
    "007777"
    ])

    g = "\n".join([
    "000000",
    "000000",
    "000000",
    "000010",
    "000109",
    "001010"
    ])

    assert path_finder(dodgy) == 7
    assert path_finder(a) == 0
    assert path_finder(b) == 2
    assert path_finder(c) == 4
    assert path_finder(d) == 42
    assert path_finder(e) == 14
    assert path_finder(f) == 0
    assert path_finder(g) == 4
