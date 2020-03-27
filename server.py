import socket
import threading
import re
import time
from game import Game
from board import Board, Color

# define threads[0] BLACK
# define threads[1] WHITE

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 12344        # Port to listen on (non-privileged ports are > 1023)
BOARD_SIZE = 7
board = Board(BOARD_SIZE)
game = Game(board_size=BOARD_SIZE, wait_click=False)
ALPHA = "abcdefghijklmnopqrstvwxyz"


def is_legal_command(command):
    command_list = re.split(r'\s+', command)
    print(command_list)
    if len(command_list) == 2:
        if command_list[0].lower() == "play":
            pos = re.findall(r"[^\W\d_]+|\d+", command_list[1])
            if len(pos) == 2 and pos[0].isalpha() and len(pos[0]) == 1 and pos[0].lower() in ALPHA[:BOARD_SIZE] and pos[1].isdigit() and int(pos[1]) <= BOARD_SIZE:
                return (ALPHA.find(pos[0]), int(pos[1])-1)
    return None


class ClientThread (threading.Thread):
    def __init__(self, connection, color):
        threading.Thread.__init__(self)
        
        self.connection = connection
        self.color = color

    def run(self):
        while True:
            data = self.connection.recv(1024)
            if not data:
                return
            if board.current_player.value == self.color:
                command = data.decode('ascii')
                coord = is_legal_command(command)
                if coord:
                    player = board.play_stone(coord)
                    game.draw_stone(game.coord_to_pos(coord), player)
                    if board.end:
                        game.show_result(board.winner)

# class GameThread(threading.Thread):
#     def __init__(self):
#         threading.Thread.__init__(self)
#     def run(self):
#         game.draw()
#         while True:
#             game.wait_event(False)

if __name__ == '__main__':

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        threads = []
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        for i in range(1, 3):
            conn, addr = server_socket.accept()
            client = ClientThread(conn, i)
            threads.append(client)
            client.start()
        game.draw()
        game_continue = True
        while game_continue:
            game_continue = game.wait_event(False)
        # game_thread = GameThread()
        # game_thread.run()
        # threads.append(game_thread)
        for i in threads:
            i.join()
