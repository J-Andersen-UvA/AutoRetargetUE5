import unreal

def import_fbx(fbx_file_path, destination_path=""):
    """
    Imports an FBX file into Unreal Engine and moves the imported asset to the specified destination path.

    Args:
        fbx_file_path: The file path of the FBX file to import.
        destination_path: The destination path where the imported asset should be initially saved.

    return:
        True if the FBX file is successfully imported and moved to the desired destination path, False otherwise.
    """
    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()

    # Create AssetImportTask for FBX
    task = unreal.AssetImportTask()
    task.set_editor_property("automated", True)
    task.set_editor_property("filename", fbx_file_path)
    task.set_editor_property("save", True)  # Save imported asset

    # Set destination path for the imported asset
    if destination_path == "":
        mesh_name = unreal.Paths.get_base_filename(fbx_file_path)
        destination_path = f"/Game/SkeletalMeshes/{mesh_name}"
    task.set_editor_property("destination_path", destination_path)

    # Set import options for FBX using FbxSceneImportOptionsSkeletalMesh
    import_options = unreal.FbxSceneImportOptionsSkeletalMesh()
    import_options.set_editor_property("import_morph_targets", True)

    # Assign import options to the task
    task.set_editor_property("options", import_options)

    # Execute the import task
    asset_tools.import_asset_tasks([task])

    unreal.log("FBX imported successfully.")
    return True


# Example usage
# fbx_file_path = "C:/Users/VICON/Desktop/MathijsTestData/glassesGuy.FBX"  # Replace with your FBX file path
# destination_path = '/Game/ImportedAssets/'  # Replace with your desired destination path in Unreal Engine
# import_fbx(fbx_file_path)
