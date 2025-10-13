import socket
import sys
import threading

def receive_messages(client_socket):
    try:
        while True:
            message = client_socket.recv(1024)
            if not message:
                print("\nConnection closed by the server.")
                break
            print(f"\nServer: {message.decode('utf-8').strip()}")
            print("Enter command (or 'exit' to quit): ", end='', flush=True)
    except ConnectionResetError:
        print("\nConnection lost.")
    finally:
        client_socket.close()
        sys.exit(0)


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python client.py HOST PORT NAME")
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
    print(f"Connected as {name}")

    threading.Thread(target=receive_messages, args=(client_socket,), daemon=True).start()

    while True:
        try:
            cmd = input("Enter command (or 'exit' to quit): ")
        except EOFError:
            break
        if cmd.lower() == 'exit':
            print("Exiting...")
            client_socket.close()
            sys.exit(0)
        client_socket.sendall(cmd.encode('utf-8'))
            
