import random


class Point:

    x: int
    y: int

    def __init__(self, x, y):
        self.x = x
        self.y = y 
    
    def __eq__(self, value):
        if isinstance(value, Point):
            return self.x == value.x and self.y == value.y
        return False
    
    def __hash__(self):
        return hash((self.x, self.y))


def randPoint(x_lim, y_lim) -> Point:
    x = random.randint(0, x_lim-5)
    y = random.randint(0, y_lim-5)
    return Point(x,y)


class ShadedPoint(Point):

    symbol: str
    shaded: bool

    def __init__(self, x, y, symbol, shaded = False):
        super(). __init__(x,y)
        self.symbol = symbol
        self.shaded = shaded

    def __str__(self):
        return self.symbol