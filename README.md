# Unreal Engine Animation Retargeter Server

## Overview

This project implements a server-side application for managing animation retargeting tasks within Unreal Engine 5.4. It provides functionality to import FBX files, create IK rigs, fetch IK rigs and retargeters, and retarget animations using a queue-based system. The server listens for client connections, processes incoming requests, and executes tasks asynchronously.

## Features

- **Server Management**: Start and stop the server using defined methods.
- **Task Management**: Utilizes a queue system to manage and execute tasks in the main thread via a Slate post-tick callback.
- **Functionality**:
  - Import FBX files and animations into Unreal Engine.
  - Create IK rigs for skeletal meshes.
  - Retarget animations between different rigs.
  - Fetch available IK rigs and retargeters from specified directories.
  - Check if assets exist in Unreal Engine.
  - Export FBX animations.

## Requirements

- **Unreal Engine 5.4**: The server is designed to interact with Unreal Engine functionalities and requires an Unreal Engine environment to execute tasks.

## Usage

To use the server, follow these steps:

1. **Installation**:
   - Clone this repository to your local machine.

2. **Setup**:
   - Ensure Unreal Engine is installed and configured properly.
   - Modify the server configuration (port number, IP address, etc.) in the script if necessary.

3. **Running the Server**:
   - Link the server script to start up on a UE5.4 project in the project. By default, the server listens on port 9999.

4. **Client Interaction**:
   - Connect clients to the server using the specified port. Clients can send commands to import files, create rigs, retarget animations, and more.

5. **Running Unreal Engine Headless with Editor functionalities**:
   - Use command: ```UE_.4\Engine\Binaries\Win64\UnrealEditor.exe project\projectName.uproject -nullrhi -log```. With arguments like ```-game``` and ```-server```, you will not be able to access the needed unreal editor commands for retargeting.

## Calling functions / Message Format
Messages sent to the server should follow the format {function}:{arg1},{arg2},.... Each message consists of a function identifier followed by a : and then comma-separated arguments:

Function: The function to be executed by the server (e.g., import_fbx, create_ik_rig).
Arguments: Optional arguments required by the specified function. Arguments should be comma-separated.
Example: To import an FBX file, the message format would be import_fbx:fbx_file_path,destination_path,name.

Ensure that messages are correctly formatted to avoid errors during command execution.

### All functions:
- create_ik_rig:mesh_name
- asset_exists:asset_path
- import_fbx:fbx_file_path,destination_path(optional)
- import_fbx_animation:fbx_file_path,destination_path,name,skeleton_path(optional)
- retarget_ik_rigs:source_rig_path,target_rig_path,rtg_name
- fetch_ik_rigs:path1,path2,...
- fetch_retargets:path1,path2,...
- retarget_animation:retargeter_path,animation_path1,animation_path2,...
- close_server:
- stop_server:
- export_fbx_animation:

## Server Illustration
![RetargetFlowchart](/imgs/retargeterFlowchart.png)
