from PIL import Image
import os
from tqdm import tqdm

src_dir = 'C:\\Users\\Hans\\omni.replicator_out\\replicator_pallets_random\\images_png'
dest_dir = 'C:\\Users\\Hans\\omni.replicator_out\\replicator_pallets_random\\images_jpg'

# Create destination directory if it doesn't exist
os.makedirs(dest_dir, exist_ok=True)

for filename in tqdm(os.listdir(src_dir)):
    if filename.endswith('.png'):
        with Image.open(os.path.join(src_dir, filename)) as img:
            dest_filename = filename.replace('.png', '.jpg')
            img.convert('RGB').save(os.path.join(dest_dir, dest_filename), 'JPEG', quality=98)

print("Conversion completed.")
