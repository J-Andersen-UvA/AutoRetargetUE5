import socket
import unreal

def send_message(message, host='localhost', port=9999):
    # Create a client socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # Connect to the server
        client_socket.connect((host, port))
        
        # Send the message
        client_socket.sendall(message.encode())
        
        print("Message sent successfully:", message)
    
    except Exception as e:
        print("Error:", e)
    
    finally:
        # Close the socket
        client_socket.close()

# Example usage
# message = "create_ik_rig:Nemu"
# send_message(message)
# save_path = f"/Game/IKRigs/glassesGuyNewIKRig.glassesGuyNewIKRig"
# send_message("asset_exists:" + save_path)
fbx_file_path = "C:/Users/VICON/Desktop/MathijsTestData/glassesGuy.FBX"  # Replace with your FBX file path
destination_path = '/Game/ImportedAssets/'  # Replace with your desired destination path in Unreal Engine
message = f"import_fbx:{fbx_file_path},{destination_path}"
unreal.log("SENDING: " + message)
send_message(message)