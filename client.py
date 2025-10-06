import socket
import sys


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python client.py HOST PORT")
        sys.exit(1)

    host = sys.argv[1]
    port = int(sys.argv[2])
    name = sys.argv[3]

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    
    message = client_socket.recv(1024)
    data = message.decode('utf-8').strip()

    if data == "Hello, Client!":
        client_socket.sendall(name.encode('utf-8'))
    else:
        print("Unexpected message from server")

    print(f"Received from server: {data}")

    while True:
        try:
            cmd = input("Enter command (or 'exit' to quit): ")
        except EOFError:
            break
        if cmd.lower() == 'exit':
            print("Exiting...")
            client_socket.close()
            sys.exit(0)
            

