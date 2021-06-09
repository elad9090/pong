import socket
import select

MAX_MSG_LENGTH = 1024
SERVER_PORT = 5555
SERVER_IP = '0.0.0.0'
def sendd(client, client_sockets, data):
    for i in client_sockets:
        if i!=client:
            i.send(str(data).encode())

def main():
    print( "Setting up server..." )
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_IP, SERVER_PORT))
    server_socket.listen()
    print( "Listening for clients..." )
    client_sockets = []
    while True:
        ready_to_read, ready_to_write, in_error = select.select([server_socket] + client_sockets, [], [])
        if len(ready_to_read)==1:
            for current_socket in ready_to_read:
                if current_socket is server_socket:
                    (client_socket, client_address) = current_socket.accept()
                    print( "New client joined!" ,client_address)
                    client_sockets.append(client_socket)
                else:
                    print("New data from client")
                    data =current_socket.recv(MAX_MSG_LENGTH).decode()
                    if data == "":
                        print("Connection closed", )
                        client_sockets.remove(current_socket)
                        current_socket.close()
                    else:
                        print(data)
                        sendd(current_socket, ready_to_read, data)
main()