import socket
import threading

HOST = ''
PORT = 7755

# Dictionary to store connected clients
clients = {}

# Function to handle connected clients
def handle_client(client_socket, client_addr, name):
    try:
        while True:
            # Receive message from clients
            data = client_socket.recv(1024).decode()

            # If client wants to exit from the chat
            if data.lower() == "quit" or data.lower() == "exit":
                broadcast(f"{name} has left from chat room.")
                break

            # Broadcast message for all clients
            message = f"{name}: {data}"
            broadcast(message, sender_socket=client_socket)
    except Exception as e:
        print(f"Error handling client {client_addr}: {e}")

    finally:
        del clients[name]
        client_socket.close()

# Function to broadcast message to all clients except sender
def broadcast(message, sender_socket=None):
    for name, client_socket in clients.items():
        if client_socket != sender_socket:
            try:
                client_socket.send(message.encode())
            except Exception as e:
                print(f"Error broadcasting the message to {name}: {e}")

# Main function to start the server
def main():
    # create socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind socket
    server_socket.bind((HOST, PORT))

    # Listening for incoming connections
    server_socket.listen()
    print("Server listening for connections...")

    try:
        while True:
            # Accept incoming connection
            client_socket, client_addr = server_socket.accept()
            print(f"Connection from {client_addr}")

            # Receive client name
            name = client_socket.recv(1024).decode()

            # Add clients to dictionary
            clients[name] = client_socket

            # Start a new thread to handle clients
            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_addr, name))
            client_thread.start()

    except KeyboardInterrupt:
        print("Server shutting down...")
        server_socket.close()

if __name__ == "__main__":
    main()