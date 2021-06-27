from MainWindow import MainWindow

if __name__ == '__main__':

    from Game.Game import Game

    window = MainWindow()
    window.mainloop()


    if window.mode == 'SP':
        Game(False).loop()
    elif window.mode == 'MP':
        Game(True, window.address).loop()

