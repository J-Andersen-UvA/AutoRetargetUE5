import socket

def send_message_and_receive_file(message, host='localhost', port=9999, timeout=5, output_file_path="received_file.fbx"):
    # Create a client socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.settimeout(timeout)  # Set socket timeout
    
    try:
        # Connect to the server
        client_socket.connect((host, port))
        
        # Send the message
        client_socket.sendall(message.encode())
        
        print("Message sent successfully:", message)
        
        # Open a file to write the received data
        with open(output_file_path, 'wb') as output_file:
            while True:
                # Receive data from the server
                data = client_socket.recv(4096)  # Adjust buffer size as needed
                if not data:
                    break  # No more data to receive
                output_file.write(data)
        
        print(f"File received and saved as: {output_file_path}")
        
    except socket.timeout:
        print("Timeout: No response received within", timeout, "seconds.")
    except Exception as e:
        print("Error:", e)
    
    finally:
        # Close the socket
        client_socket.close()

send_message_and_receive_file("export_fbx_animation:/Game/Anims/APPEL_Anim,C:/Users/VICON/Desktop/tmp/testAnimExport/,appelAnimExported")
# send_message_and_receive_file("send_file:C:/Users/VICON/Desktop/tmp/testAnimExport/appelAnimExported.fbx")
