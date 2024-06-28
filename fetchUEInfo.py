import unreal

def fetch_ik_rigs(search_paths=["/Game"]):
    ikrig_filepaths = []
    
    # Use the AssetRegistry to find all assets of the specified type
    asset_registry = unreal.AssetRegistryHelpers.get_asset_registry()
    
    if not isinstance(search_paths, list):
        search_paths = [search_paths]

    for search_path in search_paths:
        print(f"Searching for rigs in: {search_path}")
        asset_data_list = asset_registry.get_assets_by_path(search_path)
        
        for asset_data in asset_data_list:
            if asset_data.asset_class_path.asset_name == "IKRigDefinition":
                ikrig_filepaths.append(asset_data.package_name)
    
    return ikrig_filepaths

def fetch_rig_with_name(name, search_paths=["/Game"]):
    # Use the AssetRegistry to find all assets of the specified type
    asset_registry = unreal.AssetRegistryHelpers.get_asset_registry()

    if not isinstance(search_paths, list):
        search_paths = [search_paths]
    
    for search_path in search_paths:
        print(f"Searching for rigs with name {name} in: {search_path}")
        asset_data_list = asset_registry.get_assets_by_path(search_path)
        
        for asset_data in asset_data_list:
            if asset_data.asset_class_path.asset_name == "IKRigDefinition" and name in str(asset_data.package_name):
                return str(asset_data.package_name)
    
    return False

def fetch_retargets(search_paths=["/Game"]):
    retarget_filepaths = []
    
    # Use the AssetRegistry to find all assets of the specified type
    asset_registry = unreal.AssetRegistryHelpers.get_asset_registry()
    
    if not isinstance(search_paths, list):
        search_paths = [search_paths]

    for search_path in search_paths:
        print("Searching for retargets in: " + search_path)
        asset_data_list = asset_registry.get_assets_by_path(search_path)
        
        for asset_data in asset_data_list:
            if asset_data.asset_class_path.asset_name == "IKRetargeter":
                retarget_filepaths.append(asset_data.package_name)
    
    return retarget_filepaths

# Example usage:
# You can specify multiple search paths if needed
# search_paths = ['/Game/IKRigs']
# ikrigs = fetch_ik_rigs(search_paths)
# retargets = fetch_retargets(search_paths)

# print("IK Rigs:")
# for path in ikrigs:
#     print(path)

# print("\nRetargets:")
# for path in retargets:
#     print(path)
