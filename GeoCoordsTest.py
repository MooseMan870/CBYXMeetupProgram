import operator
from decimal import Decimal as D


class UnmatchedLength(Exception):
    pass


def geo_coords(lat: float, lon: float, op: operator):
    x, y = str(lat), str(lon)
    decx = x.index('.')
    decy = y.index('.')
    x, y = list(x), list(y)
    # x, y after decimal length
    x_adl = len(x[decx+1:])
    y_adl = len(y[decy+1:])
    if int(''.join(x[decx+1:])) == 0 and int(''.join(y[decy + 1:])) == 0:
        return eval(''.join(x))*eval(''.join(y))
    x[decx] = ''
    y[decy] = ''
    x = eval(''.join(x))
    y = eval(''.join(y))
    main_dict = {1: (x, x_adl), 2: (y, y_adl)}
    if op == operator.mul:
        print(f"10: {main_dict[1][0]}, 20: {main_dict[2][0]}")
        ans = op(main_dict[1][0], main_dict[2][0])
        print(ans)
        test = list(str(ans))
        test.insert(round((main_dict[1][1]+main_dict[2][1])/x_adl), '.')
        return round(float(''.join(test)), round((x_adl+y_adl)/2))
    elif op == operator.truediv:
        return round(main_dict[1][0]/main_dict[2][0], round((x_adl+y_adl)/2))


def centroid(lst: list[tuple[int, int] | tuple[float, float]]):
    x_lst = []
    y_lst = []
    for i in lst:
        x_lst.append(i[0])
        y_lst.append(i[1])

    if len(x_lst) == len(y_lst):
        pass
    else:
        raise UnmatchedLength

    x_main = []
    y_main = []

    x_main = sum(x_lst)*(1/len(x_lst))
    y_main = sum(y_lst)*(1/len(y_lst))

    return x_main, y_main


def geo_coords_dm(lat: float, lon: float, op: operator):
    return op(D(str(lat)), D(str(lon)))


