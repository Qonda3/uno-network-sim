import socket

if __name__ == "__main__":
    HOST = '127.0.0.1'  # The server's hostname or IP address
    PORT = 12345        # The port used by the server

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((HOST, PORT))
        response = client.recv(1024)
        print(f"Received from server: {response.decode()}")
# Simple TCP client that connects to a server and receives a greeting message.
# It connects to localhost on port 12345, receives a message from the server,   
# and then closes the connection.
# It uses the socket library to create a TCP socket and connect to the specified address.
