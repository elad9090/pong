from . import *


class PickleMethodNotImplementedException(BaseException):
    pass


class Picklable(object):
    def pickle(self):
        raise PickleMethodNotImplementedException()


class Rect(ServerObject, Picklable):
    class _Pos:
        def __init__(self, x, y) :
            self.x = x
            self.y = y
        
        def __getitem__(self, i):
            if i == 0:
                return self.x
            elif i == 1:
                return self.y
            else:
                raise IndexError(i)

        def __setitem__(self, i, v):
            v = int(v)
            if i == 0:
                self.x = v
            elif i == 1:
                self.y = v
            else:
                raise IndexError(i)

        def __len__(self):
            return 2

        def __repr__(self):
            return f'_Pos[X: {self.x}; Y: {self.y}]'

    def __init__(self, x, y, h, w):
        ServerObject.__init__(self)
        Picklable.__init__(self)

        self.x = x
        self.y = y
        self.height = h
        self.width = w

    @property
    def top_left_pos(self):
        return Rect._Pos(self.x - self.width // 2, self.y - self.height // 2)

    @property
    def bottom_right_pos(self):
        def add_cords(a, b):
            for i in range(len(a)):
                a[i] += b[i]
            return a
        return add_cords(self.top_left_pos, (self.width, self.height))

    def check_collision(self, other: 'Rect'):
        """
        if not (issubclass(Rect, other.__class__) or type(other) == Rect):
            raise TypeError('%s is not of subclass of Rect!' % other.__name__)
        """

        mtl = self.top_left_pos
        otl = other.top_left_pos

        return mtl.x < otl.x + other.width and \
            mtl.x + self.width > otl.x and \
                mtl.y < otl.y + other.height and \
                    mtl.y + self.height > otl.y

    def __repr__(self):
        return f'Rect[X: {self.x}; Y: {self.y}; W: {self.width}, H: {self.height}, TLP: {self.top_left_pos}, BRP: {self.bottom_right_pos}]'

    def pickle(self):
        return f'{self.x},{self.y}'


if __name__ == '__main__':
    rect1 = Rect(20, 300, 140, 10)
    rect2 = Rect(10, 300, 140, 15)

    print(rect1, rect2)
    print(rect1.top_left_pos, rect2.top_left_pos)
    print(rect1.bottom_right_pos, rect2.bottom_right_pos)
    print(rect1.check_collision(rect2))
