import os
import shutil

# Define the source directory
src_dir = 'C://Users//Hans//omni.replicator_out//replicator_pallets_random//bbox2D'

# Define the folders to create and the file prefixes that belong in them
folders = {
    'delete': ('bounding_box_2d_tight_labels_','bounding_box_2d_tight_prim_paths','bounding_box_3d_tight_labels_','bounding_box_3d_prim_paths_',),
    'bbox2D': ('bounding_box_2d_tight_',),
    'bbox3D': ('bounding_box_3d_',),
    'cameraparams': ('camera_params_',),
    'depth': ('distance_to_camera'),
    'images': ('rgb_',),
    'other': ()  # All other files will go here
}

# Function to check if a file belongs in a folder
def check_file(filename, prefixes):
    return any(filename.startswith(prefix) for prefix in prefixes)

# Create the folders
for folder in folders.keys():
    os.makedirs(os.path.join(src_dir, folder), exist_ok=True)

# Move the files to the respective folders
for filename in os.listdir(src_dir):
    filepath = os.path.join(src_dir, filename)
    # Ensure we are only moving files, not directories
    if os.path.isfile(filepath):
        moved = False  # Keep track if file was moved
        for folder, prefixes in folders.items():
            if check_file(filename, prefixes):
                shutil.move(filepath, os.path.join(src_dir, folder, filename))
                moved = True
                break
        # If file did not match any prefix, move to 'other' folder
        if not moved:
            shutil.move(filepath, os.path.join(src_dir, 'other', filename))

print("Files sorted successfully.")
