import random
from . import *


class Ball(Rect):
    def __init__(self):
        super().__init__(600, 400, 30, 30)

        self.start_pos = (600, 400)

        self.speed_x = 4 * random.choice((-1, 1))
        self.speed_y = 4 * random.choice((-1, 1))

    def reset(self):
        self.x, self.y = self.start_pos
        self.speed_x *= random.choice((-1, 1))
        self.speed_y *= random.choice((-1, 1))
    
    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y
