import math
import timeit

def str_cat(x:int, y:int) -> int:
    return int(str(x) + str(y))

def int_cat(x:int, y:int) -> int:
    return x*10**(math.floor(math.log10(y))+1) + y


print(timeit.timeit(lambda: int_cat(1238381, 9992999), number=1000000))
print(timeit.timeit(lambda: str_cat(2321843, 9129399), number=1000000))


for x in range(1, 1000):
    for y in range(1, 10000):
        if int_cat(x, y) != str_cat(x, y):
            print(x, y)
            raise ValueError(x, y)