
import skimage.io as io
import skimage.measure as measure
import sys
import numpy as np

def get_outline_binary_mask(img, width=1):
    # Create a binary mask for the outline
    outline_mask = np.zeros((img.shape[0], img.shape[1]), dtype=bool)

    for row in range(width, img.shape[0] - width):
        for col in range(width, img.shape[1] - width):
            pixel_color = img[row, col]

            # Check if any neighboring pixel is different within the specified width
            is_outline_pixel = False
            for i in range(-width, width + 1):
                for j in range(-width, width + 1):
                    if not (i == 0 and j == 0):
                        neighbor_color = img[row + i, col + j]
                        if not np.array_equal(pixel_color, neighbor_color):
                            is_outline_pixel = True
                            break

            if is_outline_pixel:
                outline_mask[row, col] = True  # White pixel for outline

    return outline_mask


def make_outline_img(img, outline_color=[0,0,0], width=1):
    for row in range(width, img.shape[0] - width):
        for col in range(width, img.shape[1] - width):
            pixel_color = img[row, col]
            # skip if pixel is already outline color
            if np.array_equal(pixel_color, outline_color):
                continue

            # process
            is_outline_pixel = False
            for i in range(-width, width + 1):
                for j in range(-width, width + 1):
                    if not (i == 0 and j == 0):
                    # if (i == 0 or j == 0) and not (i == 0 and j == 0):
                        neighbor_color = img[row + i, col + j]
                        if not np.array_equal(outline_color, neighbor_color) and not np.array_equal(pixel_color, neighbor_color):
                            is_outline_pixel = True
                            break
                if is_outline_pixel:
                    break
            # set pixel to outline color
            if is_outline_pixel:
                img[row, col] = outline_color
    return img

def outline_sanitize(img, outline_color=[0,0,0], width=1):
    cnt = 0
    while True:
        print("outline_sanitize iteration", cnt)
        work_one_time = False
        for row in range(width, img.shape[0] - width):
            for col in range(width, img.shape[1] - width):
                pixel_color = img[row, col]
                if not np.array_equal(pixel_color, outline_color):
                    continue
                # iam outline pixel
                # check if outline can be removed
                is_outline_pixel = False
                different_colors = []
                for i in range(-width, width + 1):
                    for j in range(-width, width + 1):
                        if not (i == 0 and j == 0):
                        # if (i == 0 or j == 0) and not (i == 0 and j == 0):
                            neighbor_color = img[row + i, col + j]
                            # if neighbor is outline color, skip
                            if np.array_equal(neighbor_color, outline_color):
                                continue

                            # check if neighbor color is already in list
                            is_in_list = False if len(different_colors) == 0 else np.any(np.all(neighbor_color == different_colors, axis=1))
                            if not is_in_list:
                                different_colors.append(neighbor_color)
                                if len(different_colors) > 1:
                                    is_outline_pixel = True
                                    break
                    if is_outline_pixel:
                        break
                if len(different_colors) == 1:
                    # remove outline
                    img[row, col] = different_colors[0]
                    work_one_time = True
        if not work_one_time:
            break
        cnt += 1
    return img

if __name__ == "__main__":
    path = sys.argv[1]
    filename = path.split("\\")[-1]
    filename_without_extension = filename.split(".")[0]
    img = io.imread(path)

    outline_mask = get_outline_binary_mask(img)
    outline_img = np.full((img.shape[0], img.shape[1], 3), [255, 255, 255], dtype=np.uint8)
    outline_img[outline_mask] = [0, 0, 0]

    io.imsave(f'{filename_without_extension}_outline.png', outline_img)