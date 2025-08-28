from player import *

player = Player()
player.initialize_board()

while True:
    player.update_board()
    for i in range(6):
        print("")
    if player.board.print_success():
        break