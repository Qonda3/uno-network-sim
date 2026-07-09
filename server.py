
import socket
import sys
import threading
from game_logic import (
    make_game_state, card_str, deal_hands, draw_card, add_player,
    current_player_name, is_valid_play, parse_card, advance_turn,
)

clients = []
game_started = False
game = None

_state = {
    "clients":[],
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

def handle_play(client_sock, name, tokens):
    game = _state["game"]

    if current_player_name(game) != name:
        _send(client_sock, "It's not your turn.\n")
        return False

    card = parse_card(tokens)
    if card is None:
        _send(client_sock, "Invalid card. Try: PLAY <Color> <Value>\n")
        return False

    hand = game["hands"][name]
    if card not in hand:
        _send(client_sock, "You don't have that card.\n")
        return False
    
    top_card = game["discard"][-1]
    if not is_valid_play(top_card, card):
        _send(client_sock, f"Can't play {card_str(card)} on {card_str(top_card)}.\n")
        return False

    hand.remove(card)
    game["discard"].append(card)
    broadcast_msg(f"{name} played {card_str(card)}.\n")

    color, value = card

    if value == "Reverse":
        game["direction"] *= -1
        advance_turn(game, 1)
        # In a 2-player game, Reverse acts like Skip
        if len(game["players"]) == 2:
            advance_turn(game, 1)

    elif value == "Skip":
        advance_turn(game, 2)

    elif value == "Draw Two":
        advance_turn(game, 1)
        victim = current_player_name(game)
        game["hands"][victim].extend(draw_card(game["deck"]) for _ in range(2))
        broadcast_msg(f"{victim} draws 2 cards.\n")
        advance_turn(game, 1)

    elif value == "Wild Draw Four":
        advance_turn(game, 1)
        victim = current_player_name(game)
        game["hands"][victim].extend(draw_card(game["deck"]) for _ in range(4))
        broadcast_msg(f"{victim} draws 4 cards.\n")
        advance_turn(game, 1)

    else:
        advance_turn(game, 1)

    next_player = current_player_name(game)
    broadcast_msg(f"It's {next_player}'s turn.\n")
    return True

def handle_draw(client_sock, name):
    game = _state["game"]

    if current_player_name(game) != name:
        _send(client_sock, "It's not your turn.\n")
        return

    if not game["deck"]:
        _send(client_sock, "Deck is empty, cannot draw.\n")
        return

    card = draw_card(game["deck"])
    game["hands"][name].append(card)
    _send(client_sock, f"You drew {card_str(card)}.\n")

    advance_turn(game, 1)
    broadcast_msg(f"{name} drew a card.\n", exclude_sock=client_sock)
    next_player = current_player_name(game)
    broadcast_msg(f"It's {next_player}'s turn.\n")

def handle_client(client_sock, addr):
    print(f"Connection from {addr} established.")

    # Handshake: send greeting, receive player name
    _send(client_sock, "Hello, Client!")
    raw = client_sock.recv(1024)
    if not raw:
        client_sock.close()
        return
    name = raw.decode("utf-8").strip()
    if not name:
        print("No name received — closing connection.")
        client_sock.close()
        return

    print(f"Client {addr} identified as {name!r}")
    game = _state["game"]
    num_players = game["num_players"]

    with _state["lock"]:
        add_player(game, client_sock, name)
        _state["clients"].append((client_sock, name))
        broadcast_msg(f"{name} has joined the game.\n", exclude_sock=client_sock)
        # Start only once under the lock so no double-start race
        if len(_state["clients"]) == num_players and not _state["started"]:
            _state["started"] = True
            _start_game()

    try:
        while True:
            data = client_sock.recv(1024)
            if not data:
                break
            message = data.decode("utf-8").strip()
            parts = message.split()

            if not parts:
                continue

            command = parts[0].upper()

            if command == "STATE":
                top = game["discard"][-1]
                _send(
                    client_sock,
                    f"Players: {len(game['players'])}/{num_players} | "
                    f"Top card: {card_str(top)} | "
                    f"Turn: {current_player_name(game)}\n",
                )
            elif command == "HAND":
                hand_str = ", ".join(card_str(c) for c in game["hands"][name])
                _send(client_sock, f"Your hand: {hand_str}\n")
            elif command == "PLAY":
                handle_play(client_sock, name, parts[1:])
            elif command == "DRAW":
                handle_draw(client_sock, name)
            else:
                print(f"[{name}] {message}")
                broadcast_msg(f"{name}: {message}\n", exclude_sock=client_sock)
        print(f"Connection with {name} lost.")
    finally:
        print(f"Connection with {name} closed.")
        with _state["lock"]:
            _state["clients"] = [
                c for c in _state["clients"] if c[0] is not client_sock
            ]
        broadcast_msg(f"{name} has left the game.\n")
        client_sock.close()

def broadcast_msg(message, exclude_sock=None):
    for sock, name in _state["clients"]:
        if sock != exclude_sock:
            _send(sock, message)

def broadcast_hands():
    game = _state["game"]
    for sock, name in _state["clients"]:
        hand_str = ", ".join(card_str(c) for c in game["hands"][name])
        _send(sock, f"Your hand: {hand_str}\n")

def _start_game():
    game = _state["game"]
    deal_hands(game)
    top_card = draw_card(game["deck"])
    game["discard"].append(top_card)
    broadcast_msg(
        f"All players connected. Starting game! Top card: {card_str(top_card)}\n"
    )
    broadcast_hands()
    broadcast_msg(f"It's {current_player_name(game)}'s turn.\n")

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

