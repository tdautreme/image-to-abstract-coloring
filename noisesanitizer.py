import os
import skimage.measure as measure
import numpy as np
import sys
import skimage.io as io

def get_neighbors_flattened_colors(img, i_indices, j_indices, neighbors_radius=1):
    neighbor_colors = []
    for i, j in zip(i_indices, j_indices):
        i_min = max(i - neighbors_radius, 0)
        i_max = min(i + neighbors_radius + 1, img.shape[0])
        j_min = max(j - neighbors_radius, 0)
        j_max = min(j + neighbors_radius + 1, img.shape[1])
        neighbor_region = img[i_min:i_max, j_min:j_max]
        current_colors = neighbor_region.reshape(-1, neighbor_region.shape[-1])
        neighbor_colors += list(current_colors)
    # remove colors that are the same as the current color
    neighbor_colors = np.array(neighbor_colors)
    neighbor_colors = neighbor_colors.reshape(-1, neighbor_colors.shape[-1])
    return neighbor_colors

def get_img_id(img):
    differents_color = np.unique(img.reshape(-1, img.shape[-1]), axis=0)
    # create img_id which is a map of color_id (index of color in differents_color)
    img_id = np.zeros((img.shape[0], img.shape[1]), dtype=np.uint8)
    for i in range(differents_color.shape[0]):
        mask = np.all(img == differents_color[i], axis=-1)
        img_id[mask] = i + 1 # +1 because 0 is for background
    return img_id

def remove_noise(img, region_size_treshold=200, neighbors_radius=1):
    img_id = get_img_id(img)
    print("img_id unqiue id count", np.unique(img_id).shape[0])

    # diagnonal & adjacent
    # label_img = measure.label(img_gray)
    # adjacent
    label_img = measure.label(img_id, connectivity=1)
    regions = measure.regionprops(label_img)
    print("regions count", len(regions))
    impacted_region_count = 0    
    new_img = np.array(img)
    for region in regions:
        mask = label_img == region.label

        region_size = mask.sum()
        if region_size > region_size_treshold:
            continue
        impacted_region_count += 1
        
        # get current color
        current_color = img[mask][0]

        # get all coord of image where mask is true
        coords = np.where(mask)
        i_indices = coords[0]
        j_indices = coords[1]

        # get all the colors from neighbors of each coord
        neighbor_colors = get_neighbors_flattened_colors(img, i_indices, j_indices, neighbors_radius=neighbors_radius)
        neighbor_colors = neighbor_colors[~np.all(neighbor_colors == current_color, axis=1)]

        # get the color that is the most present
        colors, counts = np.unique(neighbor_colors, axis=0, return_counts=True)
        max_count_index = np.argmax(counts)
        max_count_color = colors[max_count_index]
        new_img[mask] = max_count_color
    return new_img, impacted_region_count


def sanitize_noise(img, weight=0.1): # weight is the ratio of the diagonal of the image
    has_alpha_channel = img.shape[2] == 4
    if has_alpha_channel:
        mask = img[:,:,3] == 0
        img = img[:,:,:3]

    pixel_number = img.shape[0] * img.shape[1]
    diagonal_pixel_number = np.sqrt(pixel_number)
    weight = 1
    region_size_treshold = diagonal_pixel_number * weight
    print(region_size_treshold)

    cnt = 0
    old_impacted_region_count = 0
    while True:
        print(f"iteration {cnt}")
        cnt+=1
        img, impacted_region_count = remove_noise(img, region_size_treshold=region_size_treshold, neighbors_radius=1)
        print("impacted region count", impacted_region_count)
        print("")
        if impacted_region_count == 0:
            break
        if impacted_region_count == old_impacted_region_count:
            break
        old_impacted_region_count = impacted_region_count

    # if has_alpha_channel:
    #     img = np.dstack((img, np.where(mask, 0, 255)))
    #     # convert to uint
    #     img = (img).astype(np.uint8)
    return img


if __name__ == "__main__":
    path = sys.argv[1]
    filename = os.path.basename(path)
    filename_without_extension, extension = os.path.splitext(filename)
    img = io.imread(path)
    sanitize_noise(img, weight=0.1)
    io.imsave(f'{filename_without_extension}_sanitized.png', img)