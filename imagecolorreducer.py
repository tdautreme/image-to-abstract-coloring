
import skimage.io as io
from sklearn.cluster import KMeans
import numpy as np
import sys
import skimage.color as skcolor
import time

def find_mean_colors(image, color_count):
    # Redimensionnez l'image en un tableau 2D de pixels RGB
    pixels = image.reshape(-1, 3)

    # Utilisez K-Means pour regrouper les couleurs en "nombre_couleurs" clusters
    kmeans = KMeans(n_clusters=color_count)
    kmeans.fit(pixels)

    # Obtenez les centres des clusters (les couleurs moyennes)
    couleurs_moyennes = kmeans.cluster_centers_

    return couleurs_moyennes

def img_simplify_opti(img, mask, colors, distance=5):
    new_img = np.zeros_like(img)
    height, width, _ = img.shape
    cnt = 0
    old_percentage = 0
    mask_sum_false = np.sum(mask)
    pixel_to_process = height * width - mask_sum_false
    print(pixel_to_process, "pixels to process")
    for i in range(height):
        for j in range(width):
            if not mask[i, j]:
                i_min = max(i - distance, 0)
                i_max = min(i + distance + 1, height)
                j_min = max(j - distance, 0)
                j_max = min(j + distance + 1, width)
                
                valid_mask = ~mask[i_min:i_max, j_min:j_max]

                # debug progression
                cnt_percentage = int(float(cnt) / float(pixel_to_process) * 100)
                if cnt_percentage != old_percentage:
                    print(f"{cnt_percentage}%")
                    old_percentage = cnt_percentage
                cnt += 1
                
                neighbor_region = img[i_min:i_max, j_min:j_max]
                neighbor_colors = neighbor_region[valid_mask]
                # NEED OPTIMIZATION
                if False:
                    # create distance map
                    distance_map = create_distance_map_optimized(valid_mask, (i - i_min, j - j_min))

                    # distance_map = create_distance_map((i_max - i_min, j_max - j_min), (i - i_min, j - j_min))
                    # distance_map = distance_map[valid_mask]
                    
                    distance_map = distance_map.reshape(-1)
                    # reverse
                    max_distance = np.max(distance_map)
                    distance_map = max_distance - distance_map
                    # pow
                    distance_map = distance_map ** 5
                    # normalize
                    max_distance = np.max(distance_map)
                    distance_map = distance_map / max_distance


                    color = np.average(neighbor_colors, axis=0, weights=distance_map)
                else:
                    color = np.mean(neighbor_colors, axis=0)
                
                # pas besoin d'optimiser
                distances = np.linalg.norm(colors - color, axis=1)
                min_distance_index = np.argmin(distances)
                min_color = colors[min_distance_index]
                new_img[i, j] = min_color
                
    return new_img

# this method create the distance map from shape
def create_distance_map(shape, coord):
    distance_map = np.zeros(shape, dtype=np.float64)
    for i in range(shape[0]):
        for j in range(shape[1]):
            distance_map[i,j] = np.linalg.norm(coord - np.array([i,j]))
    return distance_map

# same but optimized
def create_distance_map_optimized(valid_mask, coord):
    i_indices, j_indices = np.where(valid_mask)
    distance_map = np.linalg.norm(np.column_stack((i_indices, j_indices)) - coord, axis=1)
    distance_map = distance_map.reshape(-1)
    return distance_map

def reduce_image_colors(img, color_count=5, iteration=1):
    has_alpha_channel = img.shape[2] == 4
    if has_alpha_channel:
        mask = img[:,:,3] == 0
        img = img[:,:,:3]
    else:
        mask = np.full((img.shape[0], img.shape[1]), False)

    # convert img to hsv
    img = skcolor.rgb2hsv(img)

    # find colors
    masked_img = img[~mask]
    colors = find_mean_colors(masked_img, color_count)

    # create new image with only colors using color distance
    for i in range(iteration):
        print(f"iteration {i}")
        current_time = time.time()
        img = img_simplify_opti(img, mask, colors)
        print(f"iteration {i} took {time.time() - current_time} seconds")

    # convert new image to rgb
    img = skcolor.hsv2rgb(img)

    # if has alpha, add with 0 if mask is true, 255 if mask is false
    if has_alpha_channel:
        img = np.dstack((img, np.where(mask, 0, 1)))

    # convert to uint
    img = (img * 255).astype(np.uint8)
    return img

if __name__ == "__main__":
    path = sys.argv[1]
    filename = path.split("\\")[-1]
    filename_without_extension = filename.split(".")[0]
    img = io.imread(path)
    img = reduce_image_colors(img)
    io.imsave(f'{filename_without_extension}_colors.png', img)