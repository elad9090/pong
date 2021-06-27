from . import *
from threading import Thread, Event
import random


class OpThread(Thread):
    def __init__(self):
        super().__init__()
        self._kill = Event()

    def run(self):
        while True:
            manager.opponent.rect.y = random.randint(0, screen_height)
            if self._kill.wait(0.2):
                break

    def kill(self):
        self._kill.set()


class Game:
    def __init__(self, is_mp, address = None):
        global manager

        if is_mp and address is None:
            raise Exception('Address was not given!')

        self.mp = is_mp
        self.address = address
        if not is_mp:
            manager = GameManager()
        else:
            manager = GameManagerMP(address)

    def loop(self):
        if not self.mp:
            manager.p1Level()
        manager.run_game()
