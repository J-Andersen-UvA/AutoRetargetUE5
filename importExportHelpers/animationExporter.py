import unreal

def export_animation(animation_asset_path : str, export_path : str, name : str = "animation", ascii : bool = False, force_front_x_axis : bool = False):
    if not export_path.endswith("/"):
        export_path += "/"

    # Full export filename including .fbx extension
    full_export_path = f"{export_path}{name}.fbx"

    FbxExportOptions = unreal.FbxExportOption()
    FbxExportOptions.ascii = ascii
    FbxExportOptions.export_local_time = True
    FbxExportOptions.export_morph_targets = True
    FbxExportOptions.export_preview_mesh = False
    FbxExportOptions.force_front_x_axis = force_front_x_axis

    task = unreal.AssetExportTask()
    task.set_editor_property("exporter", unreal.AnimSequenceExporterFBX())
    task.options = FbxExportOptions
    task.automated = True
    task.filename = full_export_path
    task.object = unreal.load_asset(animation_asset_path)
    task.write_empty_files = False
    task.replace_identical = True
    task.prompt = False

    # Export the animation
    if not unreal.Exporter.run_asset_export_task(task):
        raise ValueError(f"Failed to export animation at path {animation_asset_path}")
    return True, full_export_path

# Usage example
# print("++++++++++++++")
# export_path = "C:/Users/VICON/Desktop/tmp/testAnimExport/"  # Replace with your desired export path
# animation_asset_path = "/Game/Anims/APPEL_Anim"
# export_animation(animation_asset_path, export_path, name="appelAnimExported")
