import os
from tqdm import tqdm
import numpy as np
import pandas as pd
import re

src_dir = 'D:\\replicator_pallets_random\\bbox2D'
dest_dir = 'D:\\REPLICATOR_PALLETS_YOLO\\bbox2D'

# Create destination directory if it doesn't exist
os.makedirs(dest_dir, exist_ok=True)

"""
https://docs.omniverse.nvidia.com/extensions/latest/ext_replicator/annotators_details.html
Outputs a “tight” 2d bounding box of each entity with semantics in the camera’s viewport.

Tight bounding boxes bound only the visible pixels of entities. Completely occluded entities are ommited.
np.dtype(
        [
            ("semanticId", "<u4"),          # Semantic identifier which can be transformed into a readable label using the `idToLabels` mapping
            ("x_min", "<i4"),               # Minimum bounding box pixel coordinate in x (width) axis in the range [0, width]
            ("y_min", "<i4"),               # Minimum bounding box pixel coordinate in y (height) axis in the range [0, height]
            ("x_max", "<i4"),               # Maximum bounding box pixel coordinate in x (width) axis in the range [0, width]
            ("y_max", "<i4"),               # Maximum bounding box pixel coordinate in y (height) axis in the range [0, height]
            ('occlusionRatio', '<f4')]),    # **EXPERIMENTAL** Occlusion percentage, where `0.0` is fully visible and `1.0` is fully occluded. See additional notes below.
        ])
"""

def convert_to_yolo(arr, img_width, img_height):
    yolo_data = []
    yolo_data_additional = []
    occlusion_threshold_min = 0.0
    occlusion_threshold_max = 0.90
    # Filter out bounding boxes with occlusion rate above the threshold
    filtered_boxes = [box for box in arr if box[-1] >= occlusion_threshold_min and box[-1] <= occlusion_threshold_max]
    for box in filtered_boxes:
        semantic_id, x_min, y_min, x_max, y_max, occlusion_ratio = box
        # Berechnung der Bounding-Box-Abmessungen und des Zentrums im YOLO-Format
        x_center = ((x_min + x_max) / 2) / img_width
        y_center = ((y_min + y_max) / 2) / img_height
        width = (x_max - x_min) / img_width
        height = (y_max - y_min) / img_height
        occlusion_ratio = round(occlusion_ratio, 4)
        length_abs = abs(x_min - x_max)
        width_abs = abs(y_min - y_max)
        area = length_abs * width_abs
        if area > 100:
            yolo_data.append(f"{6} {x_center} {y_center} {width} {height}") #hard coding 6 for pallets
            yolo_data_additional.append(f"{occlusion_ratio} {area}")
    
    return yolo_data, yolo_data_additional

# Function to extract the identifier from the filename
def extract_id(filename, prefix):
    return re.sub(f'^{prefix}', '', filename.split('.')[0])

def openall():
    alldata = []
    for filename in tqdm(os.listdir(src_dir)):
        if filename.endswith('.npy'):
            data = np.load(os.path.join(src_dir, filename))
            yolo_data,yolo_data_additional = convert_to_yolo(data, img_width=1280, img_height=1280)
            alldata += yolo_data_additional
            yolo_id = extract_id(filename, "bounding_box_2d_tight_")
            yolo_filename = os.path.join(dest_dir, yolo_id+".txt")
            with open(yolo_filename, 'w') as f:
                f.write('\n'.join(yolo_data))
    return alldata


alldata = openall()
# Convert `alldata` into a list of lists
import pandas as pd

# Assume alldata is your data
split_data = [item.split() for item in alldata]
for i in range(len(split_data)):
    split_data[i] = [float(split_data[i][0])] + [int(split_data[i][1])]

df = pd.DataFrame(split_data, columns=['occlusion_ratio', 'area'])

# Compute statistics
print(df.describe(percentiles=[.05, .25, .5, .75, .90, .95]))
occlusion_mean = df['occlusion_ratio'].mean()
occlusion_std = df['occlusion_ratio'].std()
occlusion_05_percentile = df['occlusion_ratio'].quantile(0.05)
occlusion_95_percentile = df['occlusion_ratio'].quantile(0.95)

area_mean = df['area'].mean()
area_std = df['area'].std()
area_05_percentile = df['area'].quantile(0.05)
area_95_percentile = df['area'].quantile(0.95)

# Output the statistics
print(f'Occlusion Ratio - Mean: {occlusion_mean:.4f}, Standard Deviation: {occlusion_std:.4f}')
print(f'Occlusion Ratio - 5th Percentile: {occlusion_05_percentile:.4f}, 95th Percentile: {occlusion_95_percentile:.4f}')
print(f'Area - Mean: {area_mean:.4f}, Standard Deviation: {area_std:.4f}')
print(f'Area - 5th Percentile: {area_05_percentile:.4f}, 95th Percentile: {area_95_percentile:.4f}')

