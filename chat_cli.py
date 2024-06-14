from os import read
import socket
import select as sel
import sys

SOCK_LIST=[sys.stdin]

def client_chat():
    if len(sys.argv) <3:
        print("Usage : {} host port".format(sys.argv[0]))
        sys.exit(-1)
    host = sys.argv[0]
    port = int(sys.argv[1])

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.settimeout(5)

    try:
        client_socket.connect((host, port))
    except:
        print(f"Cannot reach the {host}:{port}")
        sys.exit(-1)

    print("Connected to host --> You can start sending messages...")
    sys.stdout.write("> ")
    sys.stdout.flush()

    while True:
        ready_read, ready_write, error = sel.select(SOCK_LIST, [], [])
        for sock in ready_read:
          if sock == client_socket:
              data = client_socket.recv(4096).decode()
              if not data:
                  print("Chat Disconnected...") 
                  sys.exit()
              else:
                #   sys.stdout.write(data)
                  print(data)
                #   sys.stdout.write("> ")
                  print("> ")
                #   sys.stdout.flush()
          else:
              msg = sys.stdin.readline()
              client_socket.send(msg.encode())
              print("> ")
              sys.stdout.flush()

if __name__ == "__main__":
     client_chat()
