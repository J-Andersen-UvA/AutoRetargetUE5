import unreal
import socket
import threading
import ikRigCreator
import IKRetargeter
import simpleQueue
import skeletalMeshImporter
import fetchUEInfo
import animationImporter
import functools

class Retargeter:
    def __init__(self):
        self.socket = None
        self.running = False
        self.slate_post_tick_handle = None
        self.queue = simpleQueue.Queue()
        self.current_connection = None
        self.rigs = []
        self.retargets = []
    
    def start(self, port=9999):
        self.running = True
        # Start the server socket in a separate thread
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(('localhost', port))
        self.socket.listen(1)
        print("Retargeter started. Listening on port", port)
        
        # Register Slate post-tick callback
        self.slate_post_tick_handle = unreal.register_slate_post_tick_callback(self.on_slate_post_tick)

        # Start listening for clients in a separate daemon thread
        listen_thread = threading.Thread(target=self.listen_clients, daemon=True)
        listen_thread.start()
    
    def stop(self):
        self.running = False
        # Close the server socket
        if self.socket:
            self.socket.close()
            self.socket = None  # Set socket to None after closing
        print("Retargeter stopped.")
        
        # Unregister Slate post-tick callback
        if self.slate_post_tick_handle:
            unreal.unregister_slate_post_tick_callback(self.slate_post_tick_handle)
    
    def on_slate_post_tick(self, delta_time):
        if (self.queue.size() > 0):
            func, args = self.queue.dequeue()
            unreal.log(f"Calling function {func.__name__} with arguments: {args}")

            if func == fetchUEInfo.fetch_ik_rigs:
                result = func(args)
                self.rigs = result
            elif func == fetchUEInfo.fetch_retargets:
                result = func(args)
                self.retargets = result
            else:
                result = func(*args)

            unreal.log("Result: " + str(result))
            self.send_response(self.current_connection, str(result))
        pass
    
    def import_fbx(self, args):
        args = args.split(',')

        if len(args) < 2:
            self.send_response(self.current_connection, "Invalid message format, missing arguments. Expecting: fbx_file_path, destination_path")
            raise ValueError("Invalid message format, missing arguments. Expecting: fbx_file_path, destination_path")

        # Import FBX file into Unreal Engine
        print("Importing FBX file:", args[0])
        self.queue.enqueue(skeletalMeshImporter.import_fbx, [args[0], args[1]])
    
    def import_fbx_animation(self, args):
        args = args.split(',')

        if len(args) < 3:
            self.send_response(self.current_connection, "Invalid message format, missing arguments. Expecting: fbx_file_path, destination_path, name, skeleton_path (optional)")
            raise ValueError("Invalid message format, missing arguments. Expecting: fbx_file_path, destination_path, name, skeleton_path (optional)")

        # Import FBX animation file into Unreal Engine
        print("Importing FBX animation file:", args[0])
        self.queue.enqueue(animationImporter.import_fbx_animation, args)

    def create_ik_rig(self, mesh_name):
        # Create IK rig for the given mesh
        print("Going to create IK Rig for:", mesh_name)
        self.queue.enqueue(ikRigCreator.createIKRig, [mesh_name])

    def retarget_ik_rigs(self, args):
        args = args.split(',')
        if len(args) < 3:
            self.send_response(self.current_connection, "Invalid message format, missing arguments. Expecting: source_rig_path, target_rig_path, rtg_name")
            raise ValueError("Invalid message format, missing arguments. Expecting: source_rig_path, target_rig_path, rtg_name")

        source_rig_path = args[0]
        target_rig_path = args[1]
        rtg_name = args[2]

        print("Retargeting IK rigs:", source_rig_path, target_rig_path)
        self.queue.enqueue(IKRetargeter.create_retargeter, [source_rig_path, target_rig_path, rtg_name])

    def fetch_ik_rigs(self, args):
        args = args.split(',')
        if len(args) < 1:
            self.send_response(self.current_connection, "Invalid message format, missing arguments. Expecting: paths to folders to be searched for IK rigs.")
            raise ValueError("Invalid message format, missing arguments. Expecting: paths to folders to be searched for IK rigs.")

        print("Fetching IK rigs")
        print(args)
        self.queue.enqueue(fetchUEInfo.fetch_ik_rigs, args)

    def fetch_retargets(self, args):
        args = args.split(',')
        if len(args) < 1:
            self.send_response(self.current_connection, "Invalid message format, missing arguments. Expecting: paths to folders to be searched for IK retargeters.")
            raise ValueError("Invalid message format, missing arguments. Expecting: paths to folders to be searched for IK retargeters.")

        print("Fetching IK retargeters")
        print(args)
        self.queue.enqueue(fetchUEInfo.fetch_retargets, args)

    # Function to check if an asset exists
    def asset_exists(self, asset_path):
        self.queue.enqueue(unreal.EditorAssetLibrary.does_asset_exist, [asset_path])

    def close_server(self):
        # Close the server socket
        if self.socket:
            self.socket.close()
            self.socket = None

    def handle_default(self, data):
        # Handle default message
        print("Received message:", data)

    def handle_data(self, data, connection):
        # Handle data received from client
        try:
            # Decode the byte string into a regular string
            data_str = data.decode('utf-8')
            print(f"Decoded data: {data_str}")

            # Split the decoded string into parts
            parts = data_str.split(':', 1)
            if len(parts) < 2:
                self.send_response(connection, "Invalid message format, missing ':'")
                raise ValueError("Invalid message format, missing ':'")

            message_type = parts[0]
            message_content = parts[1]
            self.current_connection = connection

            print(f"Message type: {message_type}")
            print(f"Message content: {message_content}")
            print(f"Client: {self.current_connection}")

            # Define message handlers
            message_handlers = {
                "create_ik_rig": self.create_ik_rig,
                "asset_exists": self.asset_exists,
                "import_fbx": self.import_fbx,
                "import_fbx_animation": self.import_fbx_animation,
                "retarget_ik_rigs": self.retarget_ik_rigs,
                "fetch_ik_rigs": self.fetch_ik_rigs,
                "fetch_retargets": self.fetch_retargets,
                "close_server": self.close_server,
                "stop_server": self.stop,
            }

            # Call the appropriate handler based on the message type
            handler = message_handlers.get(message_type, self.handle_default)
            if message_content == "" or message_content == None:
                handler()
            else:
                handler(message_content)

            # Send a response to the client
            # self.send_response(connection, f"Processed {message_type}")

        except UnicodeDecodeError as e:
            # Handle decoding errors
            print(f"Error decoding data: {e}")
            self.send_response(connection, f"Error decoding data: {e}")
        except ValueError as ve:
            # Handle invalid message format errors
            print(f"Error: {ve}")
            self.send_response(connection, f"Error: {ve}")
        except Exception as e:
            # Handle any other unexpected errors
            print(f"Unexpected error: {e}")
            self.send_response(connection, f"Unexpected error: {e}")


    def listen_clients(self):
        # Wait for incoming connections
        while self.running and self.socket:
            connection = None
            try:
                connection, client_address = self.socket.accept()
                print('Connection from', client_address)
                
                # Receive data from client
                data = connection.recv(1024)
                if data:
                    self.handle_data(data, connection)
                    
                
            except Exception as e:
                # Check if socket is still valid before breaking out of loop
                if self.socket:
                    print("Error accepting connection:", e)
                break
            # finally:
            #     if connection:
            #         connection.close()

    def send_response(self, connection, message):
        try:
            connection.sendall(message.encode('utf-8'))
        except Exception as e:
            print(f"Error sending response: {e}")
        finally:
            connection.close()

    def tick(self, delta_time):
        pass

# Example usage
retargeter = Retargeter()
retargeter.start()

# Start listening for clients in a separate thread
# listen_thread = threading.Thread(target=retargeter.listen_clients)
# listen_thread.start()

# Keep the program running until user interrupts or signals to stop
try:
    while True:
        # Keep the main thread alive
        unreal.idle()
        # retargeter.listen_clients()
except KeyboardInterrupt:
    retargeter.stop()
