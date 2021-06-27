screen_width, screen_height = 1200, 800


class ServerObject:
    def __init__(self):
        self.__console_prefix = [self.__class__.__name__]

    def _append_prefix(self, prefix):
        self.__console_prefix.append(prefix)
    
    def print(self, *args, **kwargs):
        print(*list(f'[{x}]' for x in self.__console_prefix), *args, **kwargs)


from .Rect import Rect
from .Ball import Ball
from .Player import Player
from .GameManager import GameManager