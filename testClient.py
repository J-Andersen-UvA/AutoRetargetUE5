import socket

def send_message(message, host='localhost', port=9999, timeout=5):
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
# message = "create_ik_rig:glassesGuyNew"
# send_message(message)
# save_path = f"/Game/IKRigs/glassesGuyNewIKRig.glassesGuyNewIKRig"
# send_message("asset_exists:" + save_path)
# fbx_file_path = "C:/Users/VICON/Desktop/MathijsTestData/glassesGuy.FBX"  # Replace with your FBX file path
# destination_path = '/Game/ImportedAssets/'  # Replace with your desired destination path in Unreal Engine
# message = f"import_fbx:{fbx_file_path},{destination_path}"
# unreal.log("SENDING: " + message)
# send_message(message)

# message = "retarget_ik_rigs:/Game/IKRigs/glassesGuyNewIKRig,/Game/IKRigs/NemuIKRig,TEST2"
# send_message(message)

# message = "fetch_ik_rigs:/Game/IKRigs"
# send_message(message)

# message = "fetch_retargets:/Game/Retargets"
# send_message(message)

# fbx_file_path = "C:/Users/VICON/Desktop/MathijsTestData/AnimNoMesh.FBX"  # Replace with your FBX file path
# destination_path = '/Game/ImportedAssets/'  # Replace with your desired destination path in Unreal Engine
# name = "testAnim2"
# message = f"import_fbx_animation:{fbx_file_path},{destination_path},{name}"
# send_message(message)

# message = "close_server:"
# send_message(message)

# message = "stop_server:"
# send_message(message)

# source_rig_path = '/Game/IKRigs/glassesGuyNewIKRig'
# target_rig_path = '/Game/IKRigs/NemuIKRig'
# anim_path = "/Game/Anims/APPEL_Anim"
# retargeter_path = "/Game/Retargets/glassesGuyToNemuRTG"
# message = (retargeter_path, anim_path)

export_path = "C:/Users/VICON/Desktop/tmp/testAnimExport/"  # Replace with your desired export path
animation_asset_path = "/Game/Anims/APPEL_Anim"
name = "appelAnimExported"
message = f"export_animation:{animation_asset_path},{export_path},{name}"
send_message(message)