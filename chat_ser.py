import socket as so
import select as sel
import sys 

HOST ='127.0.0.1'
PORT = 9898
SOCK_LIST =[]

def chat_server():
    server_socket  = so.socket(so.AF_INET,so.SOCK_STREAM)
    server_socket.setsockopt(so.SOL_SOCKET,so.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    SOCK_LIST.append(server_socket)
    RECEIVE_BUFFER = 4096
    print('chat server started on port -->'+str(PORT))
    while True:
        ready_read, ready_write, error = sel.select(SOCK_LIST,[],[], 0)
        for sock in ready_read:
            if sock == server_socket:
                client, address = server_socket.accept()
                SOCK_LIST.append(client)
                print('Client ', address, 'is connected...')
                broadcast(client, server_socket,"{} enter in chat room".format(address))
            else:
                try:
                    data = server_socket.recv(RECEIVE_BUFFER).decode()
                    if data:
                        broadcast(server_socket, sock,"{}".format(sock.getpeername()," Client Is Now Offline ..."))
                    else:
                        if sock == SOCK_LIST:
                            SOCK_LIST.remove(sock)
                except:
                    broadcast(server_socket, sock,"{}".format(sock.getpeername()," Client Now Offline ..."))
                    continue




def broadcast(client_socket, server_socket, message):
    print(message)
    for socket in SOCK_LIST:
        if socket != server_socket and socket != client_socket:
            try:
                socket.send(message)
            except:
                socket.close()
                if socket in SOCK_LIST:
                    SOCK_LIST.remove(socket)


if __name__ == "__main__":
    chat_server()