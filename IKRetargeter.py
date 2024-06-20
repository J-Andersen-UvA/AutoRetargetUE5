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
    # rtg_controller.set_preview_mesh(unreal.RetargetSourceOrTarget.SOURCE, source_skel_mesh)
    # rtg_controller.set_preview_mesh(unreal.RetargetSourceOrTarget.TARGET, target_skel_mesh)

    # Clear mapping then auto-map chains
    rtg_controller.auto_map_chains(unreal.AutoMapChainType.CLEAR, True)
    rtg_controller.auto_map_chains(unreal.AutoMapChainType.FUZZY, True)

    # Auto align bones
    rtg_controller.auto_align_all_bones(unreal.RetargetSourceOrTarget.SOURCE)

# Example usage
# Load the source and target rigs
# source_rig = unreal.EditorAssetLibrary.load_asset('/Game/IKRigs/glassesGuyNewIKRig')
# target_rig = unreal.EditorAssetLibrary.load_asset('/Game/IKRigs/NemuIKRig')

# # Call the create_retargeter function
# create_retargeter(source_rig, target_rig, rtg_name='glassesGuyToNemuRTG')
