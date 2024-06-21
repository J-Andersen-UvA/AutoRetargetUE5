import unreal

# Using 2 IK-rigs, create a retargeter between them
def create_retargeter(source_rig_path : str, target_rig_path : str, rtg_name : str="RTG") -> bool:
    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()

    # Load the source and target rigs
    source_rig = unreal.EditorAssetLibrary.load_asset(source_rig_path)
    target_rig = unreal.EditorAssetLibrary.load_asset(target_rig_path)

    # Create the RTG
    rtg = asset_tools.create_asset(asset_name=rtg_name, package_path='/Game/Retargets', asset_class=unreal.IKRetargeter, factory=unreal.IKRetargetFactory())
    rtg_controller = unreal.IKRetargeterController.get_controller(rtg)
    rtg_controller.set_ik_rig(unreal.RetargetSourceOrTarget.SOURCE, source_rig)
    rtg_controller.set_ik_rig(unreal.RetargetSourceOrTarget.TARGET, target_rig)

    # Clear mapping then auto-map chains
    rtg_controller.auto_map_chains(unreal.AutoMapChainType.CLEAR, True)
    rtg_controller.auto_map_chains(unreal.AutoMapChainType.FUZZY, True)

    # Auto align bones
    rtg_controller.auto_align_all_bones(unreal.RetargetSourceOrTarget.SOURCE)

# Helper function to convert AnimSequence to AssetData
def get_asset_data(animation):
    return unreal.AssetRegistryHelpers.get_asset_registry().get_asset_by_object_path(animation.get_path_name())

# Retarget an animation using the given retargeter
def retarget_animation(animation_path: str, retargeter_path: str) -> bool:
    # Load the animation
    animation_paths = animation_path.split(',')
    animations = [unreal.EditorAssetLibrary.load_asset(path) for path in animation_paths]
    print(animations)
    retargeter = unreal.EditorAssetLibrary.load_asset(retargeter_path)
    source_mesh = unreal.IKRetargeterController.get_controller(retargeter).get_preview_mesh(unreal.RetargetSourceOrTarget.SOURCE)
    target_mesh = unreal.IKRetargeterController.get_controller(retargeter).get_preview_mesh(unreal.RetargetSourceOrTarget.TARGET)

    animations_asset_data = [get_asset_data(animation) for animation in animations]
    unreal.IKRetargetBatchOperation.duplicate_and_retarget(animations_asset_data, source_mesh, target_mesh, retargeter, suffix='_retargeted_to_' + target_mesh.get_name())

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
# retarget_animation(anim_path, retargeter_path)