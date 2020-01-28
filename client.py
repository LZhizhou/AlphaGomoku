import socket

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 12344        # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while True:
        i = input()
        s.send(str.encode(i))
