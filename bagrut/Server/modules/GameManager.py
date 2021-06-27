from . import *

from time import sleep
from datetime import datetime


def pickle_data(o):
    if o is None:
        return 'null'
    return o.pickle()


class GameManager(ServerObject):
    def __init__(self):
        ServerObject.__init__(self)

        self.p1: Player = None
        self.p2: Player = None
        self.ball: Ball = Ball()

        self.__events = {}

        def on_quit(player):
            if self.p1 == player:
                self.p1 = None
            elif self.p2 == player:
                self.p2 = None
            self.reset_game()

        self.add_event_handler('on_quit', on_quit)

    @property
    def players(self):
        return (self.p1, self.p2)

    def reset_game(self):
        self.ball.reset()

        if self.p1:
            self.p1.score = 0

        if self.p2:
            self.p2.score = 0

    def add_event_handler(self, event, callback):
        if not event in self.__events.keys():
            self.__events[event] = []
        self.__events[event].append(callback)

    def call(self, event, *args, **kwargs):
        if event not in self.__events.keys():
            return
        
        for h in self.__events[event]:
            h(*args, **kwargs)

    def are_both_ready(self):
        return self.p1 and self.p2 and self.p1.ready and self.p2.ready

    def is_game_full(self):
        return None not in (self.p1, self.p2)

    def assign_player(self, player):
        if self.p1 is None:
            self.p1 = player
            player.x = screen_width - 20
            return 'p1'
        
        self.p2 = player
        player.x = 20
        return 'p2'

    def game_loop(self):
        def check_collisions():
            if self.p1.check_collision(self.ball) or self.p2.check_collision(self.ball):
                self.ball.speed_x *= -1
                return 'paddle'
            
            if self.ball.top_left_pos.y <= 0 or self.ball.bottom_right_pos.y >= screen_height:
                self.ball.speed_y *= -1
                return None

            if self.ball.top_left_pos.x <= 0:
                return self.p1

            if self.ball.bottom_right_pos.x >= screen_width:
                return self.p2


        reset_flag = False
        sound_to_play = 0
        winner = "null"
        winner_time = -1
        while True:
            pickled_data = ';'.join((pickle_data(self.p1), pickle_data(self.p2), pickle_data(self.ball), str(sound_to_play), str(winner)))
            margined_data = '<' * (64 - len(pickled_data)) + pickled_data
            encoded_data = margined_data.encode()

            for p in self.players:
                if p:
                    p.sck.send(encoded_data)

            sound_to_play = 0
            winner = "null"

            if self.are_both_ready():
                if reset_flag:
                    self.reset_game()
                    reset_flag = False
                
                coll = check_collisions()

                if coll:
                    if type(coll) == Player:
                        coll.score += 1
                        sound_to_play = 2
                        self.print('Player:', self.p2 if coll is self.p1 else self.p1)
                        self.print('Ball:', self.ball)

                        self.ball.reset()
                    else:
                        sound_to_play = 1

                if self.p1.score == 7 or self.p2.score == 7:
                    if self.p1.score == 7:
                        winner= b'p1'
                    else:
                        winner=b'p2'
                    self.p1.ready = False
                    self.p2.ready = False
                    reset_flag = True
                
                self.ball.update()
            
            sleep(0.005)


