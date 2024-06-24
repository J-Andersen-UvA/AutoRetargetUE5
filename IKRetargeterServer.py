import unreal
import socket
import threading
import ikRigCreator
import IKRetargeter
import simpleQueue
import skeletalMeshImporter
import fetchUEInfo
import animationImporter
import animationExporter
import functools

class Retargeter:
    """
    The Retargeter class manages a server for handling Unreal Engine animation retargeting tasks.
    It includes methods to start and stop the server, process client requests, and perform various retargeting and import operations.
    The class uses a queue to manage tasks, ensuring they are executed in the main thread via a Slate post-tick callback.

    Attributes:
        socket: The server socket for listening to client connections.
        running: A flag indicating whether the server is running.
        slate_post_tick_handle: Handle for the Slate post-tick callback.
        queue: A queue to manage tasks to be processed.
        current_connection: The current client connection being processed.
        rigs: A list to store fetched IK rigs.
        retargets: A list to store fetched retargeters.

    Methods:
        start(port=9999): Starts the server and begins listening for client connections.
        stop(): Stops the server and closes the socket.
        on_slate_post_tick(delta_time): Processes tasks from the queue in the main thread.
        import_fbx(args): Enqueues an FBX import task.
        import_fbx_animation(args): Enqueues an FBX animation import task.
        create_ik_rig(mesh_name): Enqueues a task to create an IK rig.
        retarget_ik_rigs(args): Enqueues a task to retarget IK rigs.
        fetch_ik_rigs(args): Enqueues a task to fetch IK rigs.
        fetch_retargets(args): Enqueues a task to fetch IK retargeters.
        asset_exists(asset_path): Enqueues a task to check if an asset exists.
        retarget_animation(args): Enqueues a task to retarget an animation.
        close_server(): Closes the server socket.
        handle_default(data): Handles default messages.
        handle_data(data, connection): Handles data received from clients and dispatches tasks.
        listen_clients(): Listens for client connections and processes incoming data.
        send_response(connection, message): Sends a response to the client.
        tick(delta_time): Placeholder for future implementation.
    """
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
        """
        Processes functions from the queue and executes them with the provided arguments. Logs the function name, arguments, and result.
        We do this in the Slate post-tick callback to ensure that we are executing the queue functions in the main thread.
        For each function we send a response back to the client with the result of the function.
        Depending on the incomming function we handle the function calls differently.

        Args:
            delta_time: The time elapsed since the last tick (currently not used)
        
        return:
            None
        """
        if (self.queue.size() > 0):
            func, args = self.queue.dequeue()
            unreal.log(f"Calling function {func.__name__} with arguments: {args}")

            if func == fetchUEInfo.fetch_ik_rigs:
                result = func(args)
                self.rigs = result
            elif func == fetchUEInfo.fetch_retargets:
                result = func(args)
                self.retargets = result
            elif func == IKRetargeter.retarget_animations:
                result = func(args)
            else:
                result = func(*args)

            unreal.log("Result: " + str(result))
            self.send_response(self.current_connection, str(result))
        pass
    
    def import_fbx(self, args):
        args = args.split(',')

        if len(args) < 1:
            self.send_response(self.current_connection, "Invalid message format, missing arguments. Expecting: fbx_file_path, destination_path (optional)")
            raise ValueError("Invalid message format, missing arguments. Expecting: fbx_file_path, destination_path (optional)")

        # Import FBX file into Unreal Engine
        print("Importing FBX file:", args[0])

        if len(args) > 1:
            self.queue.enqueue(skeletalMeshImporter.import_fbx, [args[0], args[1]])
        else:
            self.queue.enqueue(skeletalMeshImporter.import_fbx, [args[0]])

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

    def retarget_animation(self, args):
        args = args.split(',', 1)
        if len(args) < 2:
            self.send_response(self.current_connection, "Invalid message format, missing arguments. Expecting: retargeter_path, animation_paths")
            raise ValueError("Invalid message format, missing arguments. Expecting: retargeter_path, animation_paths")

        retargeter_path = args[0]
        animation_path = args[1]

        print("Retargeting animation:", retargeter_path, animation_path)
        self.queue.enqueue(IKRetargeter.retarget_animations, [retargeter_path, animation_path])

    def export_fbx_animation(self, args):
        args = args.split(',')
        if len(args) < 2:
            self.send_response(self.current_connection, "Invalid message format, missing arguments. Expecting: animation_asset_path, export_path, name(optional), ascii(optional), force_front_x_axis(optional)")
            raise ValueError("Invalid message format, missing arguments. Expecting: animation_asset_path, export_path, name(optional), ascii(optional), force_front_x_axis(optional)")

        print("Exporting animation to FBX:", args[0], args[1])
        self.queue.enqueue(animationExporter.export_animation, args)

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
                "retarget_animation": self.retarget_animation,
                "close_server": self.close_server,
                "stop_server": self.stop,
                "export_fbx_animation": self.export_fbx_animation,
                "export_animation": self.export_fbx_animation,
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

# Keep the program running until user interrupts or signals to stop
try:
    while True:
        # Keep the main thread alive
        unreal.idle()
except KeyboardInterrupt:
    retargeter.stop()
