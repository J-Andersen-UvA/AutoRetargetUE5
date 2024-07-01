import socket

def send_message_and_receive_file(message, host='localhost', port=9999, timeout=5, output_file_path="C:/Users/VICON/Desktop/tmp/test/testAnimImported.FBX"):
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
                try:
                    # Receive data from the server
                    data = client_socket.recv(4096)  # Adjust buffer size as needed
                    if not data:
                        break  # No more data to receive
                    output_file.write(data)
                except socket.error as e:
                    # Handle the connection reset by the server as end of file transfer
                    if e.errno == 10054:
                        print("Connection closed by the server.")
                        break
                    else:
                        raise  # Re-raise the exception if it's not the specific error
        
        print(f"File received and saved as: {output_file_path}")
        
    except socket.timeout:
        print("Timeout: No response received within", timeout, "seconds.")
    except Exception as e:
        print("Error:", e)
    
    finally:
        # Close the socket
        client_socket.close()

# send_message_and_receive_file("export_fbx_animation:/Game/Anims/APPEL_Anim,C:/Users/VICON/Desktop/tmp/testAnimExport/,appelAnimExported")

source_mesh_path = '/Game/SkeletalMeshes/glassesGuyNew/glassesGuyNew'
target_mesh_path = '/Game/SkeletalMeshes/Nemu/Nemu'
anim_path = "/Game/Anims/APPEL_Anim"
send_message_and_receive_file(f"rig_retarget_send:{source_mesh_path},{target_mesh_path},{anim_path}")
