import os
import numpy as np
import pickle
import pdb

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors



glass_folder = "/Users/marc/Downloads/test_zed_points_original_4/"
original_folder = "/Users/marc/Downloads/test_zed_points_glass_4/"


def get_mean_point_cloud_array(folder_path):
    dm_arrays = []
    img_count = int(len(os.listdir(folder_path))/3)
    img_count = 1
    for i in range(img_count):
        cloud_path = f"point_cloud_{i}.pkl"
        full_cloud_path = os.path.join(folder_path, cloud_path)
        with open(full_cloud_path, 'rb') as file:
            point_cloud = pickle.load(file)
        depth_map = point_cloud[:, :, 2]
        dm_arrays.append(depth_map)

    # Stack the arrays to form a (N, 600, 960) array
    stacked_arrays = np.stack(dm_arrays)

    # Calculate the mean along the first axis (axis=0), ignoring NaNs
    mean_array = np.nanmean(stacked_arrays, axis=0)
    return mean_array


def get_cloud_array(folder_path, index):
    cloud_path = f"point_cloud_{index}.pkl"
    full_cloud_path = os.path.join(folder_path, cloud_path)
    with open(full_cloud_path, 'rb') as file:
        point_cloud = pickle.load(file)
    depth_map = point_cloud[:, :, 2]

    return depth_map



def get_stdev_point_cloud_array(folder_path):
    dm_arrays = []
    img_count = int(len(os.listdir(folder_path))/3)
    img_count = 1
    for i in range(img_count):
        cloud_path = f"point_cloud_{i}.pkl"
        full_cloud_path = os.path.join(folder_path, cloud_path)
        with open(full_cloud_path, 'rb') as file:
            point_cloud = pickle.load(file)
        depth_map = point_cloud[:, :, 2]
        dm_arrays.append(depth_map)

    # Stack the arrays to form a (10, 600, 960) array
    stacked_arrays = np.stack(dm_arrays)

    # Calculate the mean along the first axis (axis=0), ignoring NaNs
    std_array = np.nanstd(stacked_arrays, axis=0)
    return std_array



original_mean_array = get_mean_point_cloud_array(original_folder)
new_mean_array = get_mean_point_cloud_array(glass_folder)

pts0 = get_cloud_array(glass_folder, 6)
pts1 = get_cloud_array(glass_folder, 7)

# delta = pts2-pts1

# pdb.set_trace()



# Calculate the signed differences
difference_map = new_mean_array - original_mean_array
# difference_map = pts1-pts0

#threshold the difference_map so we can see a bit more
more_than20 = difference_map > 10
less_than20 = difference_map < -10


nancondition = np.isnan(difference_map)
condition = np.logical_or(more_than20, less_than20)
# condition = np.logical_and(condition, ~nancondition)



# Calculate the minimum and median of the non-NaN values
min_value = np.nanmin(difference_map)
median_value = np.nanmedian(difference_map)

#mask the values
# blah = difference_map[~condition] = np.nan

print("Minimum of the non-NaN values:", min_value)
print("Median of the non-NaN values:", median_value)

# Define the colormap
# cmap = mcolors.LinearSegmentedColormap.from_list("custom_cmap", ["red", "yellow", "green", "yellow", "red"])
colors = ["blue", "cyan", "magenta", "pink", "yellow", "red"]
cmap = mcolors.ListedColormap(colors)


# Define the boundaries for the discrete bins
boundaries = [-1000, -20, -10,0, 10, 20, 1000]  # Example boundaries
norm = mcolors.BoundaryNorm(boundaries, cmap.N, clip=True)




# Plotting the heatmap
plt.figure(figsize=(12, 6))
plt.imshow(difference_map, cmap=cmap, norm=norm)
plt.colorbar(label='Signed Difference')
plt.title('Heatmap of Signed Differences Between Glass (0.8mm) and Original Images')
plt.xlabel('Width')
plt.ylabel('Height')
plt.show()

















