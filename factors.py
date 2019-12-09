""" Finding factors. """


#######################################################################################################################
#
#   Import
#
#######################################################################################################################

try:
    from math import sqrt, isqrt
except ImportError:
    # Python < 3.8
    isqrt = lambda n: int(sqrt(n))


#######################################################################################################################
#
#   factors_baseline
#
#######################################################################################################################

factors_baseline = lambda v: [d for d in range(1, v // 2 + 1) if v % d == 0] + [v]
    

#######################################################################################################################
#
#   factors
#
#######################################################################################################################

def factors(n):
    factors = {1, n}
    for i in range(2, isqrt(n) + 1):
        if n % i == 0:
            factors |= {i, n / i}
    return sorted(list(factors))


#######################################################################################################################
#
#   accel_asc
#
#######################################################################################################################

def accel_asc(n: int):
    """
    Generator returning partitions of an integer n, where n > 0.
    Highly-efficient, non-parameterized implementation.
    Source: http://jeromekelleher.net/generating-integer-partitions.html
    Comparative analysis: https://arxiv.org/abs/0909.2331
    """
    a = [0 for i in range(n + 1)]
    k = 1
    y = n - 1
    while k != 0:
        x = a[k - 1] + 1
        k -= 1
        while 2 * x <= y:
            a[k] = x
            y -= x
            k += 1
        l = k + 1
        while x <= y:
            a[k] = x
            a[l] = y
            yield a[:k + 2]
            x += 1
            y -= 1
        a[k] = x + y
        y = x + y - 1
        yield a[:k + 1]


#######################################################################################################################
#
#   partition
#
#######################################################################################################################

def partition(n: int, parts: int, part_min: int = 1, part_max: int = 0):
    """
    Generator returning partitions of an integer n, where n > 0.
    Adapted from: https://stackoverflow.com/a/18503391

    Parameters
    ----------
    n:          The number to be partitioned
    parts:      The number of parts into which n is to be partitioned
    part_min:   The minimum value for a partitioned part
    part_max:   The maximum value for a partitioned part

    Returns
    -------
    tuple(int): A conforming partition of n
    """
    if part_max is None:
        part_max = n
    if parts < 1:
        return
    if parts == 1:
        if n <= part_max and n >= part_min:
            yield (n, )
        return
    for i in range(part_min, part_max + 1):
        for result in partition(n - i, parts - 1, i, part_max):                
            yield result + (i, )


#######################################################################################################################
#
#   check_equivalence
#
#######################################################################################################################

def check_equivalence(fns, values):
    for value in values:
        first = None
        for fn in fns:
            result = fn(value)
            if first is None:
                first = result
            elif result != first:
                msg = f"{value}\n" + "".join(f"{fn.__name__}({value}): {fn(value)}\n" for fn in fns)
                raise ValueError(msg)


#######################################################################################################################
#
#   check_performance
#
#######################################################################################################################

def check_performance(fns, values, repetitions=1):
    from time import process_time as timer
    for fn in fns:
        start = timer()
        for n in range(repetitions):
            for value in values:
                fn(value)
        print(f"{fn.__name__}: {timer() - start}")


#######################################################################################################################
#
#   __main__
#
#######################################################################################################################

if __name__ == "__main__":
    for p in partition(1, 1):
        print(p)
    exit()

    fns = [factors_baseline, factors]
    values = [n for n in range(200, 5000)]
    check_equivalence(fns, values)
    check_performance(fns, values)