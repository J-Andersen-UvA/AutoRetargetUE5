import unreal

def createIKRig(meshName : str = "glassesGuyNew") -> bool:
    """
    Creates an IK Rig for a specified skeletal mesh. The function sets up the IK rig,
    adds the skeletal mesh, and attempts to automatically generate the IK rig using Unreal Engine's tools.
    The IK rig is then saved to "/Game/IKRigs".
    The skeletalMesh is fetched from "/Game/SkeletalMeshes/{meshName}/{meshName}".

    Args:
        meshName: The name of the skeletal mesh to create the IK rig for (default: "glassesGuyNew")

    return:
        True if the IK rig is successfully created and saved, False otherwise
    """

    # def setBoneChains(ik_rig_controller):
    #     # Add retarget chain
    #     # SPINE AND HEAD
    #     ik_rig_controller.add_retarget_chain("Spine", "Spine", "Spine2", unreal.Name())
    #     ik_rig_controller.add_retarget_chain("Neck", "Neck", "Neck", unreal.Name())
    #     ik_rig_controller.add_retarget_chain("Head", "Head", "Head", unreal.Name())

    #     # LEGS
    #     ik_rig_controller.add_retarget_chain("LeftLeg", "LeftUpLeg", "LeftToeBase", "LeftFootIK")
    #     ik_rig_controller.add_retarget_chain("RightLeg", "RightUpLeg", "RightToeBase", "RightFootIK")

    #     # ARMS
    #     ik_rig_controller.add_retarget_chain("LeftClavicle", "LeftShoulder", "LeftShoulder", unreal.Name())
    #     ik_rig_controller.add_retarget_chain("RightClavicle", "RightShoulder", "RightShoulder", unreal.Name())
    #     ik_rig_controller.add_retarget_chain("LeftArm", "LeftArm", "LeftHand", "LeftHandIK")
    #     ik_rig_controller.add_retarget_chain("RightArm", "RightArm", "RightHand", "RightHandIK")

    #     # HANDS
    #     ik_rig_controller.add_retarget_chain("LeftThumb", "LeftHandThumb1", "LeftHandThumb3", unreal.Name())
    #     ik_rig_controller.add_retarget_chain("LeftIndex", "LeftHandIndex1", "LeftHandIndex3", unreal.Name())
    #     ik_rig_controller.add_retarget_chain("LeftMiddle", "LeftHandMiddle1", "LeftHandMiddle3", unreal.Name())
    #     ik_rig_controller.add_retarget_chain("LeftRing", "LeftHandRing1", "LeftHandRing3", unreal.Name())
    #     ik_rig_controller.add_retarget_chain("LeftPinky", "LeftHandPinky1", "LeftHandPinky3", unreal.Name())
    #     ik_rig_controller.add_retarget_chain("RightThumb", "RightHandThumb1", "RightHandThumb3", unreal.Name())
    #     ik_rig_controller.add_retarget_chain("RightIndex", "RightHandIndex1", "RightHandIndex3", unreal.Name())
    #     ik_rig_controller.add_retarget_chain("RightMiddle", "RightHandMiddle1", "RightHandMiddle3", unreal.Name())
    #     ik_rig_controller.add_retarget_chain("RightRing", "RightHandRing1", "RightHandRing3", unreal.Name())
    #     ik_rig_controller.add_retarget_chain("RightPinky", "RightHandPinky1", "RightHandPinky3", unreal.Name())

    #     return ik_rig_controller

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

    # # Create IK Goals
    # ik_rig_controller.add_new_goal("LeftFootIK", "LeftToeBase")
    # ik_rig_controller.add_new_goal("RightFootIK", "RightToeBase")
    # ik_rig_controller.add_new_goal("LeftHandIK", "LeftHand")
    # ik_rig_controller.add_new_goal("RightHandIK", "RightHand")

    # # Set retargetRootBone
    # ik_rig_controller.set_retarget_root("Hips")

    # ik_rig_controller = setBoneChains(ik_rig_controller)

    ik_rig_controller.apply_auto_generated_retarget_definition()

    # Use apply_auto_fbik to attempt to automatically generate the IK rig
    if (not ik_rig_controller.apply_auto_fbik()):
        unreal.log_error("Failed to automatically generate IK rig.")
        return False
    else:
        unreal.log("IK rig generated successfully.")

    unreal.EditorAssetLibrary.save_asset(save_path)

    unreal.log("IK rig saved to: " + save_path)

    return True
