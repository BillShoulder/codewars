""" Codewars kata: Shortest Knight Path. https://www.codewars.com/kata/shortest-knight-path/train/python """

#######################################################################################################################
#
#   Import
#
#######################################################################################################################

from pprint import pprint
from collections import deque
from string import ascii_uppercase
from itertools import product
from copy import deepcopy


#######################################################################################################################
#
#   coords_to_algebraic
#
#######################################################################################################################

def coords_to_algebraic(x, y):
    letters = ascii_uppercase[ascii_uppercase.index('A'):ascii_uppercase.index('H') + 1]
    return letters[x] + str(y + 1)


def coordslist_to_algebraic(thelist):
    return [coords_to_algebraic(item[0], item[1]) for item in thelist]


#######################################################################################################################
#
#   knight_moves
#
#######################################################################################################################

def knight_moves(x, y):
    """ Return a list of all valid knight moves from coordinates x, y. """
    moves = list(product([x - 1, x + 1], [y - 2, y + 2])) + list(product([x - 2, x + 2], [y - 1, y + 1]))
    return [(x, y) for x, y in moves if x >= 0 and y >= 0 and x < 8 and y < 8]


#######################################################################################################################
#
#   knight
#
#######################################################################################################################

def knight(p1, p2):
    distance = lambda s1, s2: abs(s1[0] - s2[0]) + abs(s1[1] - s2[1])
    letters = ascii_uppercase[ascii_uppercase.index('A'):ascii_uppercase.index('H') + 1]
    start = (letters.index(p1[0].upper()), int(p1[1]) - 1)
    end = (letters.index(p2[0].upper()), int(p2[1]) - 1)
    max_distance = distance(start, end) + 4
    queue = deque([[start]])
    visited = set()
    while len(queue) != 0:
        state = queue.pop()
        if state[-1] == end:
            return len(state) - 1
        visited.add(state[-1])
        for child in filter(lambda c: c not in visited and distance(c, end) <= max_distance, knight_moves(state[-1][0], state[-1][1])):
            new_state = deepcopy(state)
            new_state.append(child)
            queue.appendleft(new_state)


#######################################################################################################################
#
#   cool_knight
#
#######################################################################################################################

def cool_knight(p1, p2):
    """ Way cool solution: https://www.codewars.com/kata/reviews/549eec06d3a3b138290000b7/groups/58cbfff73b5c6092bf0002e8 """
    a, b = [('abcdefgh'.index(p[0]), int(p[1])) for p in [p1, p2]]
    x, y = sorted((abs(a[0] - b[0]), abs(a[1] - b[1])))[::-1]

    if (x, y) == (1, 0): return 3
    if (x, y) == (2, 2) or ((x, y) == (1, 1) and any(p in ['a1','h1','a8','h8'] for p in [p1, p2])): return 4
    
    delta = x - y
    
    return delta - 2*((delta-y)//(3 if y > delta else 4))    


#######################################################################################################################
#
#   __main__
#
#######################################################################################################################

if __name__ == "__main__":
    # print(knight('b7', 'a8'))
    print(knight('g2', 'h1'))













#######################################################################################################################
#
#   DA CRYPT
#
#######################################################################################################################

        # for child in filter(lambda c: c not in visited, knight_moves(state[-1][0], state[-1][1])):
        #     print(f"Considering: {child}")
        #     visited.append(child)
        #     state.append(child)
        #     queue.appendleft(state)