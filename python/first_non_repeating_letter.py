""" Codewars kata: First non-repeating character """

from collections import Counter


def first_non_repeating_letter(string):
    counter = Counter(string.lower())
    return next((c for c in string if counter[c.lower()] == 1) , None)


if __name__ == "__main__":
    print(first_non_repeating_letter('stress'))