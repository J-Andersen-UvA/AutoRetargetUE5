import unreal
import socket
import threading

class Retargeter:
    def __init__(self):
        self.socket = None
        self.running = False
        self.slate_post_tick_handle = None
    
    def start(self, port=9999):
        self.running = True
        # Start the server socket in a separate thread
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(('localhost', port))
        self.socket.listen(1)
        print("Retargeter started. Listening on port", port)
        
        # Register Slate post-tick callback
        # self.slate_post_tick_handle = unreal.register_slate_post_tick_callback(self.on_slate_post_tick)
    
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
        pass
    
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
                    print("Received:", data)
                
            except Exception as e:
                # Check if socket is still valid before breaking out of loop
                if self.socket:
                    print("Error accepting connection:", e)
                break
            finally:
                if connection:
                    connection.close()
    
    def tick(self, delta_time):
        pass

# Example usage
retargeter = Retargeter()
retargeter.start()

# Start listening for clients in a separate thread
listen_thread = threading.Thread(target=retargeter.listen_clients)
listen_thread.start()

# asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
# rtg = asset_tools.create_asset(asset_name='RTG', package_path='/Game/tst/autoretarget', asset_class=unreal.IKRetargeter, factory=unreal.IKRetargetFactory())
# rtg_controller = unreal.IKRetargeterController.get_controller(rtg)
# source_mesh = unreal.load_asset(name='/Game/SkeletalMeshes/glassesGuy/glassesGuyNew')
# target_mesh = unreal.load_asset(name='/Game/SkeletalMeshes/Nemu/Nemu')
# # source_ik_rig = unreal.IKUtilities.create_ik_data(source_mesh.skeleton)
# # target_ik_rig = unreal.IKUtilities.create_ik_data(target_mesh.skeleton)
# # rtg_controller.set_ik_rig(unreal.RetargetSourceOrTarget.SOURCE, source_ik_rig)
# # rtg_controller.set_ik_rig(unreal.RetargetSourceOrTarget.TARGET, target_ik_rig)
# rtg_controller.set_ik_rig(unreal.RetargetSourceOrTarget.SOURCE, source_mesh)
# rtg_controller.set_ik_rig(unreal.RetargetSourceOrTarget.TARGET, target_mesh)

# retargeter = unreal.BatchRetargetSettings()  # Create a new instance of BatchRetargetSettings
# # Create a new instance with auto_generate_retargeter set to True
# retargeter.auto_generate_retargeter = True
# source_mesh = unreal.load_asset(name='/Game/SkeletalMeshes/glassesGuy/glassesGuyNew')
# target_mesh = unreal.load_asset(name='/Game/SkeletalMeshes/Nemu/Nemu')
# retargeter.source_skeletal_mesh = source_mesh
# retargeter.target_skeletal_mesh = target_mesh

# unreal.IKRetargetAnimInstance
# unreal.retarget
# unreal.IKRetarget
# Keep the program running until user interrupts or signals to stop
try:
    while True:
        # Keep the main thread alive
        unreal.idle()
except KeyboardInterrupt:
    retargeter.stop()


def createIKRig(meshName : str = "glassesGuyNew") -> bool:
    '''
        An approach to making IK rigs with python in UE

        Steps:
        1. Create IKRigDefinition object
        2. Get IKRigController from it
        3. Add skeletal mesh to it
        4. Add retarget chain if not present
        5. Use apply_auto_fbik to attempt to automatically generate the IK rig
        6. Profit

        Args:
            meshName (str): The name of the mesh to create the IK rig for
    '''
    def setBoneChains(ik_rig_controller):
        # Add retarget chain
        # SPINE AND HEAD
        ik_rig_controller.add_retarget_chain("Spine", "Spine", "Spine2", unreal.Name())
        ik_rig_controller.add_retarget_chain("Neck", "Neck", "Neck", unreal.Name())
        ik_rig_controller.add_retarget_chain("Head", "Head", "Head", unreal.Name())

        # LEGS
        ik_rig_controller.add_retarget_chain("LeftLeg", "LeftUpLeg", "LeftToeBase", "LeftFootIK")
        ik_rig_controller.add_retarget_chain("RightLeg", "RightUpLeg", "RightToeBase", "RightFootIK")

        # ARMS
        ik_rig_controller.add_retarget_chain("LeftClavicle", "LeftShoulder", "LeftShoulder", unreal.Name())
        ik_rig_controller.add_retarget_chain("RightClavicle", "RightShoulder", "RightShoulder", unreal.Name())
        ik_rig_controller.add_retarget_chain("LeftArm", "LeftArm", "LeftHand", "LeftHandIK")
        ik_rig_controller.add_retarget_chain("RightArm", "RightArm", "RightHand", "RightHandIK")

        # HANDS
        ik_rig_controller.add_retarget_chain("LeftThumb", "LeftHandThumb1", "LeftHandThumb3", unreal.Name())
        ik_rig_controller.add_retarget_chain("LeftIndex", "LeftHandIndex1", "LeftHandIndex3", unreal.Name())
        ik_rig_controller.add_retarget_chain("LeftMiddle", "LeftHandMiddle1", "LeftHandMiddle3", unreal.Name())
        ik_rig_controller.add_retarget_chain("LeftRing", "LeftHandRing1", "LeftHandRing3", unreal.Name())
        ik_rig_controller.add_retarget_chain("LeftPinky", "LeftHandPinky1", "LeftHandPinky3", unreal.Name())
        ik_rig_controller.add_retarget_chain("RightThumb", "RightHandThumb1", "RightHandThumb3", unreal.Name())
        ik_rig_controller.add_retarget_chain("RightIndex", "RightHandIndex1", "RightHandIndex3", unreal.Name())
        ik_rig_controller.add_retarget_chain("RightMiddle", "RightHandMiddle1", "RightHandMiddle3", unreal.Name())
        ik_rig_controller.add_retarget_chain("RightRing", "RightHandRing1", "RightHandRing3", unreal.Name())
        ik_rig_controller.add_retarget_chain("RightPinky", "RightHandPinky1", "RightHandPinky3", unreal.Name())

        return ik_rig_controller

    # Define the save path
    save_path = f"/Game/IKRigs/{meshName}IKRig.{meshName}IKRig"

    # Create a new IKRig asset
    unreal.AssetToolsHelpers.get_asset_tools().create_asset(
        asset_name=f"{meshName}IKRig",
        package_path="/Game/IKRigs",
        asset_class=unreal.IKRigDefinition,
        factory=unreal.IKRigDefinitionFactory()
    )

    # Load the newly created IKRig asset
    ik_rig_definition = unreal.EditorAssetLibrary.load_asset(save_path)

    # Get IKRigController from it
    ik_rig_controller = unreal.IKRigController().get_controller(ik_rig_definition)

    # Add skeletal mesh to it
    mesh_path = f"/Game/SkeletalMeshes/{meshName}/{meshName}"
    skeletal_mesh = unreal.EditorAssetLibrary.load_asset(mesh_path)
    ik_rig_controller.set_skeletal_mesh(skeletal_mesh)

    # Create IK Goals
    ik_rig_controller.add_new_goal("LeftFootIK", "LeftToeBase")
    ik_rig_controller.add_new_goal("RightFootIK", "RightToeBase")
    ik_rig_controller.add_new_goal("LeftHandIK", "LeftHand")
    ik_rig_controller.add_new_goal("RightHandIK", "RightHand")

    # Set retargetRootBone
    ik_rig_controller.set_retarget_root("Hips")

    ik_rig_controller = setBoneChains(ik_rig_controller)

    # Use apply_auto_fbik to attempt to automatically generate the IK rig
    if (not ik_rig_controller.apply_auto_fbik()):
        unreal.log_error("Failed to automatically generate IK rig.")
    else:
        unreal.log("IK rig generated successfully.")

    unreal.EditorAssetLibrary.save_asset(save_path)

    unreal.log("IK rig saved to: " + save_path)

createIKRig("glassesGuyNew")
createIKRig("Nemu")
