"""  Codewars kata: Conway's Game of Life - Unlimited Edition. https://www.codewars.com/kata/conways-game-of-life-unlimited-edition/train/python """

#######################################################################################################################
#
#   Import
#
#######################################################################################################################

from copy import deepcopy


#######################################################################################################################
#
#   get_generation
#
#######################################################################################################################

def neighbors(cells, idx_row, idx_col):
    start_row, end_row = max(idx_row-1, 0), min(idx_row+1, len(cells)-1)
    start_col, end_col = max(idx_col-1, 0), min(idx_col+1, len(cells[0])-1)
    return sum(sum(cells[r][start_col:end_col+1]) for r in range(start_row, end_row+1)) - cells[idx_row][idx_col]


#######################################################################################################################
#
#   get_generation
#
#######################################################################################################################

def get_generation(cells, generations):
    cells = deepcopy(cells)
    for _ in range(generations):
        # Expand the matrix.
        for _ in range(4):
            if 1 in cells[-1]: cells.append([0] * len(cells[-1]))
            cells = list(map(list, zip(*cells[::-1])))
        # Update each cell according to the number of neighbors.
        new_cells = deepcopy(cells)
        for idx_row in range(len(cells)):
            for idx_col in range(len(cells[-1])):
                count = neighbors(cells, idx_row, idx_col)
                if cells[idx_row][idx_col] == 1 and count not in range(2, 4):
                    new_cells[idx_row][idx_col] = 0
                elif cells[idx_row][idx_col] == 0 and count == 3:
                    new_cells[idx_row][idx_col] = 1
        cells = new_cells
    # Contract the matrix.
    for _ in range(4):
        while cells and 1 not in cells[-1]: cells.pop() 
        cells = list(map(list, zip(*cells[::-1])))
    # All done.
    return cells


#######################################################################################################################
#
#   get_generation_recursive
#
#######################################################################################################################

def get_generation_recursive(cells, generations):
    cells = deepcopy(cells) # Constraint that the input array should be fixed makes recursive approach inefficient.
    if generations == 0:
        # Contract the matrix.
        for _ in range(4):
            while cells and 1 not in cells[-1]: cells.pop() 
            cells = list(map(list, zip(*cells[::-1])))
        return cells
    # Expand the matrix.
    for _ in range(4):
        if 1 in cells[-1]: cells.append([0] * len(cells[-1]))
        cells = list(map(list, zip(*cells[::-1])))            
    # Update each cell according to the number of 'live' neighbors.
    new_cells = deepcopy(cells)
    for idx_row in range(len(cells)):
        for idx_col in range(len(cells[-1])):
            count = neighbors(cells, idx_row, idx_col)
            if cells[idx_row][idx_col] == 1 and count not in range(2, 4):
                new_cells[idx_row][idx_col] = 0
            elif cells[idx_row][idx_col] == 0 and count == 3:
                new_cells[idx_row][idx_col] = 1
    return get_generation(new_cells, generations - 1)


#######################################################################################################################
#
#   __main__
#
#######################################################################################################################

if __name__ == "__main__":
    start = [[1,0,0],
             [0,1,1],
             [1,1,0]]

    end   = [[0,1,0],
            [0,0,1],
            [1,1,1]]

    result = get_generation(start, 1)

    print(result)
    print(result == end)