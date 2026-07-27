"""  Codewars kata: Pyramid Slide Down. https://www.codewars.com/kata/pyramid-slide-down/train/python """

#######################################################################################################################
#
#   Import
#
#######################################################################################################################

from pprint import pprint


#######################################################################################################################
#
#   longest_slide_down
#
#######################################################################################################################

def longest_slide_down(pyramid):
    for row in range(len(pyramid) -2, -1, -1):
        pyramid[row] = [val + max(pyramid[row + 1][idx], pyramid[row + 1][idx + 1]) for idx, val in enumerate(pyramid[row])]
    return pyramid[0][0]


#######################################################################################################################
#
#   __main__
#
#######################################################################################################################

if __name__ == "__main__":
    tiny = [[3], [7, 4]]

    small = [[3], [7, 4], [2, 4, 6], [8, 5, 9, 3]]

    med =  [[75],
            [95, 64],
            [17, 47, 82],
            [18, 35, 87, 10],
            [20,  4, 82, 47, 65],
            [19,  1, 23, 75,  3, 34],
            [88,  2, 77, 73,  7, 63, 67],
            [99, 65,  4, 28,  6, 16, 70, 92],
            [41, 41, 26, 56, 83, 40, 80, 70, 33],
            [41, 48, 72, 33, 47, 32, 37, 16, 94, 29],
            [53, 71, 44, 65, 25, 43, 91, 52, 97, 51, 14],
            [70, 11, 33, 28, 77, 73, 17, 78, 39, 68, 17, 57],
            [91, 71, 52, 38, 17, 14, 91, 43, 58, 50, 27, 29, 48],
            [63, 66,  4, 68, 89, 53, 67, 30, 73, 16, 69, 87, 40, 31],
            [ 4, 62, 98, 27, 23,  9, 70, 98, 73, 93, 38, 53, 60,  4, 23]]

    pprint(longest_slide_down(tiny))










#######################################################################################################################
#
#   longest_slide_down
#   Too slow
#
#######################################################################################################################

# def longest_slide_down(pyramid):
#     # Too slow!
#     if len(pyramid) == 1: return pyramid[0][0]
#     return pyramid[0][0] + max(longest_slide_down([r[:-1] for r in pyramid][1:]), longest_slide_down([r[1:] for r in pyramid][1:]))


# def _longest_slide_down_(pyramid, top_row, top_col):
#     if top_row == len(pyramid): return 0
#     return pyramid[top_row][top_col] + max(_longest_slide_down_(pyramid, top_row+1, top_col), _longest_slide_down_(pyramid, top_row+1, top_col+1))


# def longest_slide_down(pyramid):
#     return _longest_slide_down_(pyramid, 0, 0)


# def longest_slide_down(pyramid):
#   # Good
#     while len(pyramid) != 1:
#         bottom = pyramid.pop()
#         for idx, val in enumerate(pyramid[-1]):
#             pyramid[-1][idx] += max(bottom[idx], bottom[idx+1])
#     return pyramid[0][0]


# def longest_slide_down(pyramid):
#     # Better
#     while len(pyramid) != 1:
#         bottom = pyramid.pop()
#         pyramid[-1] = [val + max(bottom[idx], bottom[idx + 1]) for idx, val in enumerate(pyramid[-1])]
#     return pyramid[0][0]