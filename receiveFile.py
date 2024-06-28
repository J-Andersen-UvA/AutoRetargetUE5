import socket

def receive_file(filepath, host='localhost', port=9998, timeout=5):
    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to a specific address and port
    server_socket.bind((host, port))

    # Listen for incoming connections
    server_socket.listen(1)

    print('Waiting for a connection...')

    # Accept a connection from a client
    client_socket, client_address = server_socket.accept()
    print('Connected to:', client_address)

    # Receive the file data
    with open(filepath, 'wb') as file:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            file.write(data)

    print('File received successfully.')

    # Close the connection and the socket
    client_socket.close()
    server_socket.close()
