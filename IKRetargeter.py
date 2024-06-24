import unreal

# Using 2 IK-rigs, create a retargeter between them
def create_retargeter(source_rig_path : str, target_rig_path : str, rtg_name : str="RTG") -> bool:
    """
    Create a retargeter between the source and target IK-rigs. Loading of the source and target rigs is done using the EditorAssetLibrary.
    Retarget saved in the /Game/Retargets folder.

    Args:
        source_rig_path: The path to the source IK-rig asset
        target_rig_path: The path to the target IK-rig asset
        rtg_name: The name of the retargeter asset (default: "RTG")

    Returns:
        True if the retargeter is successfully created, False otherwise
    """
    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()

    # Load the source and target rigs
    source_rig = unreal.EditorAssetLibrary.load_asset(source_rig_path)
    target_rig = unreal.EditorAssetLibrary.load_asset(target_rig_path)

    if not source_rig or not target_rig:
        raise ValueError(f"Failed to load source or target rig at path {source_rig_path} or {target_rig_path}")

    # Create the RTG
    rtg = asset_tools.create_asset(asset_name=rtg_name, package_path='/Game/Retargets', asset_class=unreal.IKRetargeter, factory=unreal.IKRetargetFactory())
    rtg_controller = unreal.IKRetargeterController.get_controller(rtg)
    rtg_controller.set_ik_rig(unreal.RetargetSourceOrTarget.SOURCE, source_rig)
    rtg_controller.set_ik_rig(unreal.RetargetSourceOrTarget.TARGET, target_rig)

    if not rtg:
        raise ValueError(f"Failed to create retargeter at path /Game/Retargets/{rtg_name}")

    # Clear mapping then auto-map chains
    rtg_controller.auto_map_chains(unreal.AutoMapChainType.CLEAR, True)
    rtg_controller.auto_map_chains(unreal.AutoMapChainType.FUZZY, True)

    # Auto align bones
    rtg_controller.auto_align_all_bones(unreal.RetargetSourceOrTarget.SOURCE)

    return True

# Helper function to convert AnimSequence to AssetData
def get_asset_data(animation):
    return unreal.AssetRegistryHelpers.get_asset_registry().get_asset_by_object_path(animation.get_path_name())

def retarget_animations(retargeter_path: str, animation_paths: str, destination_path : str = "/Game/Anims/RetargetedAnimations") -> bool:
    """
    Retarget an animation using the given retargeter path. Loading of the retargeter and animations is done using the EditorAssetLibrary.
    You can specify multiple animation paths separated by commas. The retargeted animations will be saved to the destination path.

    Args:
        retargeter_path: The path to the retargeter asset
        animation_paths: The paths to the animation assets to be retargeted, separated by commas
        destination_path: The destination path for the retargeted animations (default: "/Game/Anims/RetargetedAnimations")
    return:
        True if the retargeting is successful, False otherwise
    """
    # Load the animation paths and the retargeter with the source and target meshes
    animation_paths = animation_paths.split(',')
    animations = [unreal.EditorAssetLibrary.load_asset(path) for path in animation_paths]
    retargeter = unreal.EditorAssetLibrary.load_asset(retargeter_path)
    if not retargeter:
        raise ValueError(f"Failed to load retargeter at path {retargeter_path}")

    source_mesh = unreal.IKRetargeterController.get_controller(retargeter).get_preview_mesh(unreal.RetargetSourceOrTarget.SOURCE)
    target_mesh = unreal.IKRetargeterController.get_controller(retargeter).get_preview_mesh(unreal.RetargetSourceOrTarget.TARGET)

    # Make sure we are using asset_data for the animations
    animations_asset_data = [get_asset_data(animation) for animation in animations]
    retargeted_assets = unreal.IKRetargetBatchOperation.duplicate_and_retarget(animations_asset_data, source_mesh, target_mesh, retargeter, suffix='_retargeted_to_' + target_mesh.get_name())

    # Move the retargeted animations to the specified destination path
    for asset_data in retargeted_assets:
        asset_path = asset_data.get_asset().get_path_name()
        asset_name = unreal.EditorAssetLibrary.get_path_name_for_loaded_asset(asset_data.get_asset()).split('/')[-1]
        new_asset_path = destination_path + '/' + asset_name
        
        if not unreal.EditorAssetLibrary.rename_asset(asset_path, new_asset_path):
            raise ValueError(f"Failed to move asset {asset_path} to {new_asset_path}")

    return True

# Example usage
# print("++++++++++++++")
# Load the source and target rigs
# source_rig_path = '/Game/IKRigs/glassesGuyNewIKRig'
# target_rig_path = '/Game/IKRigs/NemuIKRig'

# # Call the create_retargeter function
# create_retargeter(source_rig_path, target_rig_path, rtg_name='glassesGuyToNemuRTG')

# Retarget an animation using the retargeter
# anim_path = "/Game/Anims/APPEL_Anim"
# retargeter_path = "/Game/Retargets/glassesGuyToNemuRTG"
# retarget_animation(retargeter_path, anim_path)