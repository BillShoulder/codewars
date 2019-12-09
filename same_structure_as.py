""" Codewars kata: Nesting Structure Comparison. https://www.codewars.com/kata/520446778469526ec0000001/train/python """

#######################################################################################################################
#
#   Import
#
#######################################################################################################################


#######################################################################################################################
#
#   same_structure_as
#
#######################################################################################################################

def same_structure_as(original, other):
    if type(original) == type(other) == list:
        if len(original) != len(other) or not all(same_structure_as(a, b) for a, b in zip(original, other)): return False
    elif type(original) == list or type(other) == list: return False
    return True


#######################################################################################################################
#
#   __main__
#
#######################################################################################################################

if __name__ == "__main__":
    print(same_structure_as([1,[1,1]],[2,[2,2]]))               # should equal True

    print(same_structure_as([ 1, [ 1, 1 ] ], [ [ 2, 2 ], 2 ]))  # should equal False

    print(same_structure_as([ [ [ ], [ ] ] ], [ [ 1, 1 ] ] ))   # should equal False

    print(same_structure_as([1,[1,1]], [2,[2]]))                # should equal False

    print(same_structure_as([],1))                              # should equal False

    print(same_structure_as([1,'[',']'], ['[',']',1]))          # should equal True