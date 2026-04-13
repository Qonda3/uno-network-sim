
import socket
import sys
import threading
from game_logic import make_game_state, card_str

clients = []
game_started = False
game = None

_state = {
    "client":[],
    "game": None,
    "started": False,
    "lock": threading.Lock()
}

def _send(sock, text):
    """Send a UTF-8 message; silently ignore broken pipes."""
    try:
        sock.sendall(text.encode("utf-8"))
    except OSError:
        pass

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
    for _, name in clients:
        game.hands[name] = [game.deck.draw() for _ in range(7)]
    top_card = game.deck.draw()
    game.discard.append(top_card)
    broadcast_msg(f"All players connected. Starting game! Top card: {top_card}")
    broadcast_hands()
    
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

def broadcast_hands():
    game = _state["game"]
    for sock, name in _state["clients"]:
        hand_str = ", ".join(card_str(c) for c in game["hands"][name])
        _send(sock, f"Your hand: {hand_str}\n")

def start_server(host, port, num_players):
    _state["game"] = make_game_state(num_players)
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind((host, port))
    srv.listen(num_players)
    print(f"Server started at {host}:{port} (waiting for {num_players} player(s))")
    while True:
        conn, addr = srv.accept()
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python server.py HOST PORT NUM_PLAYERS")
        print("Example: python server.py 0.0.0.0 9999 2")
        sys.exit(1)
    start_server(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))  

