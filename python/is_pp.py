""" Codewars kata: What's a Perfect Power anyway? https://www.codewars.com/kata/whats-a-perfect-power-anyway """


from math import log, isqrt, isclose


def is_prime(n):
    """ Use sympy if performance matters - or C++) """
    print(f"is_prime: {n}")
    return False if (n > 2 and not(n & 1)) else all(n % i for i in range(3, int(isqrt(n)) + 1, 2))


def next_prime(value):
    """ Use sympy if performance matters - or C++) """
    print(f"next_prime: {value}")
    value += 1 if not value & 1 else 2
    while not is_prime(value):
        value += 2
    return value


def isPP(n):
    for base in range(2, isqrt(n) + 1):
        power = log(n) / log(base)
        rounded_power = round(power)
        if isclose(power, rounded_power):
            return [base, rounded_power]
    return None


if __name__ == "__main__":
    pp = [4, 8, 9, 16, 25, 27, 32, 36, 49, 64, 81, 100, 121, 125, 128, 144, 169, 196, 216, 225, 243, 256, 289, 324, 343, 361, 400, 441, 484]
    for item in pp:
        print(item, isPP(item))
