import os
import re

# Define the source directory
src_dir = 'C:\\Users\\Hans\\omni.replicator_out\\replicator_pallets_random'

# Define file types and their respective directories
file_types = {
    'images_png': ('rgb_', '.png'),
    'bbox2D': ('bounding_box_2d_tight_', '.npy'),
    'bbox3D': ('bounding_box_3d_', '.npy'),
    'cameraparams': ('camera_params_', '.json'),
    'depth': ('distance_to_camera_', '.npy')
}


# Function to extract the identifier from the filename
def extract_id(filename, prefix):
    return re.sub(f'^{prefix}', '', filename.split('.')[0])

# Gather all identifiers from the image files
image_ids = set()
for filename in os.listdir(os.path.join(src_dir, 'images_png')):
    if filename.endswith('.png'):
        image_ids.add(extract_id(filename, file_types['images_png'][0]))
    else:
        print(f'Unexpected file or folder in images directory: {filename}')


print(len(image_ids))

# Check each image identifier to ensure all file types are present
for image_id in image_ids:
    missing_files = [
        file_type
        for file_type, (prefix, extension) in file_types.items()
        if not os.path.exists(os.path.join(src_dir, file_type, f'{prefix}{image_id}{extension}'))
    ]
    if missing_files:
        print(f'Missing {", ".join(missing_files)} files for image identifier {image_id}')

print("Check completed.")
