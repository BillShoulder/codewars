""" Codewars kata: Consecutive strings. https://www.codewars.com/kata/56a5d994ac971f1ac500003e """



def longest_consec2(strarr, k):
    return max(("".join([strarr[n] for n in range(i, i + k)]) for i in range(len(strarr) - k + 1)), key=len) if k in range(len(strarr) + 1) else ""



if __name__ == "__main__":
    result = longest_consec2(["zone", "abigail", "theta", "form", "libe", "zas"], 2)
    print(f"'{result}'")