def enough(cap, on, wait):
    return max(0, on + wait - cap)



if __name__ == "__main__":
    print(enough(100, 60, 50))
    print(enough(10, 5, 5))
    print(enough(20, 5, 5))
