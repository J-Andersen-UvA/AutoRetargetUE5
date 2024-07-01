import socket
import os

def send_message(message, host='localhost', port=9999, timeout=5):
    # Create a client socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.settimeout(timeout)  # Set socket timeout
    data = ""
    try:
        # Connect to the server
        client_socket.connect((host, port))
        
        # Send the message
        client_socket.sendall(message.encode())
        
        print("Message sent successfully:", message)
        
        # Receive the response
        response = client_socket.recv(1024)
        if response:
            data = response.decode('utf-8')
            print("Response received:", data)
            # Further processing logic based on the response
            
    except socket.timeout:
        print("Timeout: No response received within", timeout, "seconds.")
    except Exception as e:
        print("Error:", e)
    
    finally:
        # Close the socket
        client_socket.close()
        return data

def send_file(file_path, host='localhost', port=9999, timeout=5):
    # Check if file exists
    if not os.path.isfile(file_path):
        print("File does not exist:", file_path)
        return

    file_name = os.path.basename(file_path)

    # Send the filename first
    msg = send_message(f"receive_fbx:{file_name}", host, port, timeout)
    if "Listening for file on" in msg:
        data = msg.split("Listening for file on ")[-1].split(":")
        host = data[0]
        port = int(data[1])
    else:
        print("Error:", msg)
        return

    # Create a client socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.settimeout(timeout)  # Set socket timeout

    try:
        # Connect to the server
        client_socket.connect((host, port))
        
        # Open the file and send its contents
        with open(file_path, 'rb') as file:
            while (file_data := file.read(1024)):
                try:
                    client_socket.sendall(file_data)
                except socket.error as e:
                    # Handle the connection reset by the server as end of file transfer
                    if e.errno == 10054:
                        print("Connection closed by the server.")
                        break
                    else:
                        raise  # Re-raise the exception if it's not the specific error

        print("File sent successfully:", file_path)
        
        # Receive the response
        # response = client_socket.recv(1024)
        # if response:
        #     print("Response received:", response.decode('utf-8'))
            # Further processing logic based on the response
            
    except socket.timeout:
        print("Timeout: No response received within", timeout, "seconds.")
    except Exception as e:
        print("Error:", e)
    
    finally:
        # Close the socket
        client_socket.close()

# Example usage
file_path = "C:/Users/VICON/Desktop/MathijsTestData/AnimNoMesh.FBX"  # Replace with your FBX file path

# Send the file
send_file(file_path)
