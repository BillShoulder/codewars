"""  Codewars kata: Conway's Game of Life - Unlimited Edition. https://www.codewars.com/kata/conways-game-of-life-unlimited-edition/train/python """

from collections import namedtuple
from pprint import pprint
from copy import deepcopy

Cell = namedtuple("Cell", "row col")


def neighbors(cells, cell):
    neighbors = 0
    start_row = max(cell.row - 1, 0)
    end_row = min(cell.row + 1, len(cells) - 1)
    start_col = max(cell.col - 1, 0)
    end_col = min(cell.col + 1, len(cells[0]) - 1)
    for r in range(start_row, end_row + 1):
        for c in range(start_col, end_col + 1):
            neighbors += cells[r][c]
    return neighbors - cells[cell.row][cell.col]


def get_generation(cells, generations):
    for x in range(generations):
        # Expand the matrix.
        for m in range(4):
            if 1 in cells[-1]: cells.append([0] * len(cells[-1]))
            cells = list(map(list, zip(*cells[::-1])))
        # Update each cell according to the number of neighbors.
        new_cells = deepcopy(cells)
        for idx_row in range(len(cells)):
            for idx_col in range(len(cells[-1])):
                count = neighbors(cells, Cell(row=idx_row, col=idx_col))
                if cells[idx_row][idx_col] == 1 and count not in range(2, 4):
                    new_cells[idx_row][idx_col] = 0
                elif cells[idx_row][idx_col] == 0 and count == 3:
                    new_cells[idx_row][idx_col] = 1
        cells = new_cells
    # Contract the matrix.
    for m in range(4):
        while cells and 1 not in cells[-1]: cells.pop() 
        cells = list(map(list, zip(*cells[::-1])))
    # All done.
    return cells




#######################################################################################################################
#
#   __main__
#
#######################################################################################################################

if __name__ == "__main__":
    # test = [[0, 0, 0, 0, 0],
    #         [0, 1, 0, 0, 0],
    #         [0, 0, 1, 1, 0],
    #         [0, 1, 1, 0, 0],
    #         [0, 0, 0, 0, 0]]

    # pprint(test)

    # print(neighbors(test, Cell(row=1, col=2)))

    # exit()



    start = [[1,0,0],
             [0,1,1],
             [1,1,0]]


    end   = [[0,1,0],
            [0,0,1],
            [1,1,1]]

    result = get_generation(start, 1)

    print(result)
    print(result == end)