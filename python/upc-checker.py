def checkupc(code):
    """ function that will validate if a given UPC code checksums """

    upc = [int(c) for c in str(code)]

    if len(upc) == 13:
        #upc.reverse()
        digit_code = (sum(upc[0:-1:2])) + (sum(upc[1:-1:2]) * 3)
        check = digit_code % 10
        return (10 - check) == upc[-1]
    elif len(upc) == 12:
        #upc.reverse()
        digit_code = (sum(upc[0:-1:2]) * 3) + (sum(upc[1:-1:2]))
        check = digit_code % 10
        return (10 - check) == upc[-1]
