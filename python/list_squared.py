""" Codewars kata: Integers: Recreation One. https://www.codewars.com/kata/integers-recreation-one/train/python """

try:
    from math import sqrt, isqrt
except ImportError:
    # Python < 3.8
    from math import sqrt
    isqrt = lambda n: int(sqrt(n))

def factors(n):
    factors = {1, n}
    for i in range(2, isqrt(n) + 1):
        if n % i == 0:
            factors |= {i, n / i}
    return factors


def list_squared(m, n):
    result = []
    for test in range(m, n + 1):
        sum_squared = sum(d**2 for d in factors(test))
        square_root = sqrt(sum_squared)
        if square_root == int(square_root):
            result.append([test, int(sum_squared)])
    return result



if __name__ == "__main__":
    print(list_squared(1, 250))









