

def swap_case(s):
    listOfStrings = []
    for x in s:
        if (x.isupper()):
            x = x.lower()
            listOfStrings.append(x)
        else:
            x = x.upper()
            listOfStrings.append(x)

    return "".join(listOfStrings)


if __name__ == '__main__':
    s = input()
    result = swap_case(s)
