from PIL import Image
import os
from tqdm import tqdm
import re

src_dir = r'C:\Users\Hans\omni.replicator_out\replicator_pallets_random_new\images'
dest_dir = r'C:\Users\Hans\omni.replicator_out\replicator_pallets_random_new\images_jpg'

# Function to extract the identifier from the filename
def extract_id(filename, prefix):
    return re.sub(f'^{prefix}', '', filename.split('.')[0])

# Create destination directory if it doesn't exist
os.makedirs(dest_dir, exist_ok=True)

for filename in tqdm(os.listdir(src_dir)):
    if filename.endswith('.png'):
        with Image.open(os.path.join(src_dir, filename)) as img:
            dest_filename = extract_id(filename, "rgb_")+".jpg"
            img.convert('RGB').save(os.path.join(dest_dir, dest_filename), 'JPEG', quality=80)

print("Conversion completed.")
