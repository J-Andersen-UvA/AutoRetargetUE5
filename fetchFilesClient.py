import socket

def send_message(message, host='localhost', port=8070, timeout=5):
    # Create a client socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.settimeout(timeout)  # Set socket timeout
    
    try:
        # Connect to the server
        client_socket.connect((host, port))
        
        # Send the message
        client_socket.sendall(message.encode())
        
        print("Message sent successfully:", message)
        
        # Receive the response
        response = client_socket.recv(1024)
        if response:
            print("Response received:", response.decode('utf-8'))
            # Further processing logic based on the response
            
    except socket.timeout:
        print("Timeout: No response received within", timeout, "seconds.")
    except Exception as e:
        print("Error:", e)
    
    finally:
        # Close the socket
        client_socket.close()

# Example usage
message = "fetch_files:/Game/"
send_message(message)
