
import socket
import sys
import threading

import client

clients = []
game_started = False
game = None

class GameState:
    def __init__(self, players):
        self.num_players = num_players
        self.players = []
        self.hands = []
        self.deck = []
        self.discard = []
        self.turn_index = 0

def handle_client(client_socket, addr):
    global clients, game_started
    print(f"Connection from {addr} has been established!")
    client_socket.sendall(b"Hello, Client!")
    name = client_socket.recv(1024).decode('utf-8').strip()
    if not name:
        print("No name received, closing connection.")
        client_socket.close()
        return
    print(f"Client {addr} identified as {name}")
    clients.append((client_socket, name))
    broadcast_msg(f"{name} has joined the game.", client_socket)

    if len(clients) == num_players and not game_started:
        game_started = True
        broadcast_msg("All players connected. Game will start soon.")
    
    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            message = data.decode('utf-8').strip()
            if message.upper() == "STATE":
                client_socket.sendall(f"Players: {len(game.players)}/{game.num_players}\n".encode("utf-8"))
            print(f"Received from {name}: {message}")
            broadcast_msg(f"{name}: {message}", client_socket)
    except ConnectionResetError:
        print(f"Connection with {name} lost.")
    finally:
        print(f"Connection with {name} closed.")
        clients = [c for c in clients if c[0] != client_socket]
        broadcast_msg(f"{name} has left the game.")
        client_socket.close()

def broadcast_msg(message, sender_socket=None):
    for client, name in clients:
        if client != sender_socket:
            try:
                client.sendall(message.encode('utf-8'))
            except:
                print(f"Could not send message to {name}, connection broken.")

def start_server(host, port, num_players):
    global game
    game = GameState(num_players)
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

