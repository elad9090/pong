from . import *


class ClientDisconnectedException(BaseException):
    pass


class Player(Rect):
    def __init__(self, sck, address, gamemanager: 'GameManager'):
        super().__init__(0, 400, 140, 10)

        sck.settimeout(25)

        self.sck = sck
        self.address = address
        
        self.is_from_game = False
        self.is_player = False

        self.score = 0
        self.ready = False

        self.gamemanager = gamemanager

        self._append_prefix('{:15s}:{:5d}'.format(self.address[0], self.address[1]))

        self.print('< Start Communication >')

    def recv(self, n):
        try:
            data = self.sck.recv(n)
            if len(data) == 0:
                raise ClientDisconnectedException()

            while data[0] == b'<' or data[0] == 60:
                data = data[1:]
            return data
        except:
            self.print('< End Communication >')
            if self.is_from_game:
                self.gamemanager.call('on_quit', self)
            
            try:
                self.sck.close()
            except:
                pass

            raise

    def main(self):
        try:
            self.loop()
        except:
            pass
        finally:
            self.sck.close()

    def loop(self):
        data = self.recv(9)
        if data == b'connectst':
            self.sck.send(b'alive')
            return
        elif data != b'connected':
            self.sck.send(b'Invalid use of server!')
            return

        self.is_player = True

        if self.gamemanager.is_game_full():
            self.sck.send(b'Game is full')
            return

        self.is_from_game = True

        side = self.gamemanager.assign_player(self)
        self.sck.send(side.encode())

        while True:
            data = self.recv(9).decode().split(',')
            self.y = int(data[0])
            self.ready = data[1]

    def pickle(self):
        return f'{self.y},{self.ready},{self.score}'

