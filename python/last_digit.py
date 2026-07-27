"""  Codewars kata: Last digit of a large number. https://www.codewars.com/kata/last-digit-of-a-large-number/train/python """

#######################################################################################################################
#
#   baseline_last_digit
#
#######################################################################################################################

def baseline_last_digit(n1, n2):
    return pow(n1, n2, mod=10)


#######################################################################################################################
#
#   last_digit
#
#######################################################################################################################

def sequence(digit):
    seq = sequence.cache.get(digit)
    if seq is None:
        next_digit = digit
        seq = []
        while True:
            next_digit = (next_digit * digit) % 10
            if next_digit in seq: break
            seq.append(next_digit)
        sequence.cache[digit] = seq
    return seq
sequence.cache = dict()
    

def last_digit(n1, n2):
    if n2 == 0: return 1
    if n1 == 0: return 0
    digit = n1 % 10
    if n2 == 1: return digit
    seq = sequence(digit)
    if len(seq) == 1: return seq[0]
    return seq[(n2 - 2) % len(seq)]     # n2 - 2 because we special-case the first two powers.



#######################################################################################################################
#
#   __main__
#
#######################################################################################################################

if __name__ == "__main__":
    for val in range(100):
        for n in range(24):
            last = last_digit(val, n)
            baseline = baseline_last_digit(val, n)
            print(last, baseline, f"last_digit({val}, {n})", last == baseline)
            assert last == baseline, f"last_digit({val}, {n})"
























#######################################################################################################################
#
#   DA CRYPT
#
#######################################################################################################################

# def sequence(digit):
#     seq = sequence.cache.get(digit)
#     if seq is None:
#         next_digit = digit
#         seq = []
#         while True:
#             next_digit *= digit
#             next_digit = next_digit % 10
#             if next_digit in seq:
#                 break
#             seq.append(next_digit)
#         sequence.cache[digit] = seq
#     return seq

# sequence.cache = dict()
