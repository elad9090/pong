import socket
play=True
while play:
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.connect(("127.0.0.1", 5555))
    msg=input("what?")
    my_socket.send(msg.encode())
    data = my_socket.recv(1024).decode()
    print("The server sent " + data)
    if data=="stop":
        my_socket.close()