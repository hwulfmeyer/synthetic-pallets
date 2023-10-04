import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt

data = []
#directory = r'D:\code\DATA\LOCO_YOLOv6_BBOX\labels\train'
directory = r'D:\code\DATA\REPLICATOR_PALLETS_YOLO\labels\train'
IMG_SIZE = 1280

for filename in os.listdir(directory):
    if filename.endswith('.txt'):
        filepath = os.path.join(directory, filename)
        with open(filepath, 'r') as file:
            lines = file.readlines()
            for line in lines:
                values = line.strip().split()
                class_id, x_center, y_center, width, height = map(float, values)
                width *= IMG_SIZE
                height *= IMG_SIZE
                area = width * height  # calculate area
                data.append([class_id, x_center, y_center, width, height, area])

columns = ['class_id', 'x_center', 'y_center', 'width', 'height', 'area']
df = pd.DataFrame(data, columns=columns)

filtered_df = df[df['class_id'] == 6]

# The rest of the code is the same as above

print(filtered_df.describe(percentiles=[.05, .25, .5, .75, .90, .95]))

width_05, width_95 = filtered_df['width'].quantile([0.05, 0.95])
height_05, height_95 = filtered_df['height'].quantile([0.05, 0.95])

# Filtering the data
filtered_df = filtered_df[(filtered_df['width'] >= width_05) & (filtered_df['width'] <= width_95) & 
                 (filtered_df['height'] >= height_05) & (filtered_df['height'] <= height_95)]

print(filtered_df.describe(percentiles=[.05, .25, .5, .75, .90, .95]))


# You'll need to install seaborn if you haven't already
# pip install seaborn

plt.figure(figsize=(8, 8))
sns.kdeplot(x=df['x_center']*IMG_SIZE, y=df['y_center']*IMG_SIZE, fill=True, cmap='Reds', thresh=0)
plt.xlabel('X Coordinate')
plt.ylabel('Y Coordinate')
plt.title('Heatmap of Centers')
plt.axis('equal')  # This ensures that the scale of x and y is the same
plt.show()
