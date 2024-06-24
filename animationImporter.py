import unreal

def import_fbx_animation(fbx_file_path, destination_path, name, skeleton_path=""):
    task = unreal.AssetImportTask()
    task.filename = fbx_file_path
    task.destination_path = destination_path
    task.destination_name = name

    task.replace_existing = True
    task.automated = True
    task.save = True

    task.options = unreal.FbxImportUI()
    task.options.import_materials = False
    task.options.import_animations = True
    task.options.import_as_skeletal = True
    task.options.import_mesh = False
    task.options.automated_import_should_detect_type = False

    if skeleton_path != "":
        skeleton_asset = unreal.load_asset(skeleton_path)
        if isinstance(skeleton_asset, unreal.Skeleton):
            task.options.skeleton = skeleton_asset
        elif isinstance(skeleton_asset, unreal.SkeletalMesh):
            task.options.skeleton = skeleton_asset.skeleton
        else:
            raise TypeError(f"The asset at {skeleton_path} is not of type Skeleton")
    else:
        task.options.skeleton = None

    task.options.mesh_type_to_import = unreal.FBXImportType.FBXIT_ANIMATION 

    unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([task])

# Usage example
# print("++++++++++++++")
# fbx_file_path = "C:/Users/VICON/Desktop/MathijsTestData/AnimNoMesh.FBX"  # Replace with your FBX file path
# destination_path = '/Game/ImportedAssets/'  # Replace with your desired destination path in Unreal Engine
# name = "testAnim2"
# import_fbx_animation(fbx_file_path, destination_path, name, skeleton_path="/Game/ImportedAssets/AnimMesh")
# import_fbx_animation(fbx_file_path, destination_path, name)
