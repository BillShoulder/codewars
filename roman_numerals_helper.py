"""  Codewars kata: Roman Numerals Helper. https://www.codewars.com/kata/51b66044bce5799a7f000003/train/python """

#######################################################################################################################
#
#   Import
#
#######################################################################################################################

from pprint import pprint
from collections import OrderedDict


#######################################################################################################################
#
#   RomanNumerals
#
#######################################################################################################################

class RomanNumerals:
    lettervals = OrderedDict({"M": 1000,
                              "D": 500,
                              "C": 100,
                              "L": 50,
                              "X": 10,
                              "V": 5,
                              "I": 1})

    substitutions = OrderedDict({"DCCCC":   "CM",
                                 "CCCC":    "CD",
                                 "LXXXX":   "XC",
                                 "XXXX":    "XL",
                                 "VIIII":   "IX",
                                 "IIII":    "IV"})

    @classmethod
    def to_roman(cls, integer: int):
        numerals = ""
        for letter, value in cls.lettervals.items():
            count, remainder = divmod(integer, value)
            numerals += letter * count
            integer = remainder
            if integer == 0: break
        for search, replace in cls.substitutions.items():
            numerals = numerals.replace(search, replace)
        return numerals 

    @classmethod
    def from_roman(cls, numerals: str):
        for replace, search in cls.substitutions.items():
            numerals = numerals.replace(search, replace)
        return sum(cls.lettervals[l] for l in numerals)


#######################################################################################################################
#
#   __main__
#
#######################################################################################################################

if __name__ == "__main__":
    print(RomanNumerals.to_roman(2008))
    print(RomanNumerals.from_roman('MMMMCM'))
