""" Codewars kata: Calculator. https://www.codewars.com/kata/5235c913397cbf2508000048 """

#######################################################################################################################
#
#   Import
#
#######################################################################################################################

import operator
import re


#######################################################################################################################
#
#   Calculator
#
#######################################################################################################################

class Calculator(object):

    re_num = r"(([-+])?(\d+)(\.\d+)?)"

    def _muldiv_(self, m):
        op = operator.mul if m.group("op") == "*" else operator.truediv
        return f"{op(float(m.group('n1')), float(m.group('n2'))):+}"

    def _evaluate_(self, thing):
        if type(thing) != str: thing = thing[1]
        subs = -1
        while subs != 0: thing, subs = re.subn(r"\(([^\(\)]*?)\)", self._evaluate_, thing)
        subs = -1
        while subs != 0: thing, subs = re.subn(rf"(?P<n1>{self.re_num})(?P<op>\*|\/)(?P<n2>{self.re_num})", self._muldiv_, thing)
        return str(sum(float(val[0]) for val in re.findall(self.re_num, thing)))

    def evaluate(self, thing):
        return float(self._evaluate_(thing.replace(" ", "")))


#######################################################################################################################
#
#   __main__
#
#######################################################################################################################

if __name__ == "__main__":
    result = Calculator().evaluate("2 / 2 + 3 * 4 - 6")

    print("result = {}".format(result))
