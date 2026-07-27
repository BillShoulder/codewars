""" Codewars kata: Sum of Intervals. https://www.codewars.com/kata/sum-of-intervals/train/python """



import sys

def sum_of_intervals(intervals):
    intervals.sort()
    end = -sys.maxsize
    count = 0
    for interval in intervals:
        start = max(interval[0], end)
        end = max(interval[1], end)
        count += (end - start)
    return count



if __name__ == "__main__":
    result = sum_of_intervals([(1, 5)])
    print(result)
    result = sum_of_intervals([(1,5), (10, 20), (1, 6), (16, 19), (5, 11)])
    print(result)