""" Codewars kata: String incrementer. https://www.codewars.com/kata/string-incrementer """


import re


def increment_string(strng):
    updated, updates = re.subn(r"\d+$", lambda m: f"{int(m[0]) + 1:}".zfill(len(m[0])), strng)
    return strng + "1" if updates == 0 else updated


if __name__== "__main__":
    result = increment_string("fred001")
    print(result)