
import socket

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
    start_server()
# Simple TCP server that listens for connections and sends a greeting message.
# It binds to localhost on port 12345 and can handle up to 4 simultaneous connections.
# It uses the socket library to create a TCP socket, bind it to the specified address,
# and listen for incoming connections. When a client connects, it sends a greeting message
# and then closes the connection.
