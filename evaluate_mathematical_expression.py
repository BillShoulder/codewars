""" Codewars kata: Evaluate mathematical expression. https://www.codewars.com/kata/52a78825cdfc2cfc87000005/train/python """

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

    def _float_to_string_(self, f, p=40):
        # decimal.Decimal would let us avoid these shenanigans, but it's not available.
        result = f"{f:+1.{p}f}"
        if "." in result:
            result = result.rstrip("0")
            if result[-1] == ".": result += "0"
        return result

    def _muldiv_(self, m):
        op = operator.mul if m.group("op") == "*" else operator.truediv
        return self._float_to_string_(op(float(m.group('n1')), float(m.group('n2'))))

    def _subber_(self, search, replace, target):
        subs = -1
        while subs != 0:
            target, subs = re.subn(search, replace, target, count=1)
            target = target.replace("--", "+")
            target = target.replace("-+", "-")
        return target

    def _evaluate_(self, thing):
        if type(thing) != str:
            thing = thing[1]
        thing = self._subber_(r"\(([^\(\)]*?)\)", self._evaluate_, thing)
        thing = self._subber_(rf"(?P<n1>{self.re_num})(?P<op>\*|\/)(?P<n2>{self.re_num})", self._muldiv_, thing)
        return self._float_to_string_(sum(float(val[0]) for val in re.findall(self.re_num, thing)))

    def evaluate(self, thing):
        return float(self._evaluate_(thing.replace(" ", "")))


def calc(expression):
    return Calculator().evaluate(expression)


#######################################################################################################################
#
#   __main__
#
#######################################################################################################################

if __name__ == "__main__":
    print(f"result = {calc('-(-13) - (84 + 51 * (40)) * (5 / ((((83 * -32)))) / -93)')}") # 12.957005441119316
