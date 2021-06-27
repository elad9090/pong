import socket
import threading
from modules import GameManager, Player

# print(all(modules))


def main():
    manager = GameManager()

    server = socket.socket()
    server.bind(('0.0.0.0', 80))
    server.listen(0)

    threading.Thread(target=manager.game_loop).start()

    while True:
        sck, address = server.accept()
        p = Player(sck, address, manager)
        threading.Thread(target=p.main).start()


main()