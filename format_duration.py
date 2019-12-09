""" Codewars kata: Human readable duration format. https://www.codewars.com/kata/human-readable-duration-format/train/python """

#######################################################################################################################
#
#   Import
#
#######################################################################################################################

from collections import OrderedDict


#######################################################################################################################
#
#   format_duration
#
#######################################################################################################################

durations = OrderedDict({"year":    31536000,
                         "day":     86400,
                         "hour":    3600,
                         "minute":  60,
                         "second":  1})

def format_duration(seconds):
    if seconds == 0: return "now"
    result = ""
    for name, divisor in durations.items():
        count, seconds = divmod(seconds, divisor)
        if count > 0: result += f"{count} {name}{'s' if count > 1 else ''}{', ' if seconds else ''}"
        if seconds == 0: break
    return " and ".join(result.rsplit(", ", 1))


#######################################################################################################################
#
#   __main__
#
#######################################################################################################################

if __name__ == "__main__":
    print(format_duration(1))