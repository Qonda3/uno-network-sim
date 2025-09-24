
import socket
import sys

HOST = '127.0.0.1'
PORT = 12345
def start_server():
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind((HOST, PORT))
    srv.listen(4)
    print(f"Server started at {HOST}:{PORT}")
    while True:
        client, addr = srv.accept()
        print(f"Connection from {addr}")
        client.sendall(b"Hello, Client!")
        client.close()
if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python server.py HOST PORT NUM_PLAYERS")
        print("Example: python server.py 0.0.0.0 9999 2")
        sys.exit(1)
    host = sys.argv[1]
    port = int(sys.argv[2])
    num_players = int(sys.argv[3])
    start_server()

