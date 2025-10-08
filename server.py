
import socket
import sys
import threading

def handle_client(client_socket, addr):
    print(f"Connection from {addr} has been established!")
    client_socket.sendall(b"Hello, Client!")
    name = client_socket.recv(1024).decode('utf-8').strip()
    print(f"Client {addr} identified as {name}")
    try:
        while True:
            message = client_socket.recv(1024)
            if not message:
                break
            print(f"Received from {name}: {message.decode('utf-8').strip()}")
            client_socket.sendall(b"Message received")
    except ConnectionResetError:
        print(f"Connection with {name} lost.")
    finally:
        client_socket.close()
        print(f"Connection with {name} closed.")
        


def start_server(host, port, num_players):
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind((host, port))
    srv.listen(4)
    print(f"Server started at {host}:{port}")
    while True:
        client, addr = srv.accept()
        threading.Thread(target=handle_client, args=(client, addr), daemon=True).start()

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python server.py HOST PORT NUM_PLAYERS")
        print("Example: python server.py 0.0.0.0 9999 2")
        sys.exit(1)
    host = sys.argv[1]
    port = int(sys.argv[2])
    num_players = int(sys.argv[3])
    start_server(host, port, num_players)

## Example usage:
# python server.py 0.0.0.0 9999 2
# This starts the server on all interfaces at port 9999, expecting 2 players
# Clients can connect using:
# python client.py 127.0.0.1 9999 Player1   

