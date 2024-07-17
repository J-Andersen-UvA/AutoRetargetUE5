import socket
import sys

def main():
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <host> <port>")
        sys.exit(1)

    host = sys.argv[1]
    port = int(sys.argv[2])

    # Create a socket object
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    server_address = (host, port)
    sock.connect(server_address)

    # Check if the connection is made
    if sock.fileno() != -1:
        print("Connection made")

    # Send a test message
    message = 'This is a test message'
    sock.sendall(message.encode())

    # Receive the response
    response = sock.recv(1024)
    print("Received:", response.decode())

    # Close the socket
    sock.close()

if __name__ == "__main__":
    main()
