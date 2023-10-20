
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

if __name__ == "__main__":
    path = sys.argv[1]
    filename = path.split("\\")[-1]
    filename_without_extension = filename.split(".")[0]
    img = io.imread(path)

    outline_mask = get_outline_binary_mask(img)
    outline_img = np.full((img.shape[0], img.shape[1], 3), [255, 255, 255], dtype=np.uint8)
    outline_img[outline_mask] = [0, 0, 0]

    io.imsave(f'{filename_without_extension}_outline.png', outline_img)