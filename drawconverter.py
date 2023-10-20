import sys
sys.path.append('./')
from imagecolorreducer import reduce_image_colors
from noisesanitizer import sanitize_noise
from imageoutliner import get_outline_binary_mask
from svgsplitter import split_svg_by_path
import numpy as np
import skimage.io as io
import os

if __name__ == "__main__":
    input_image_path = sys.argv[1]
    output_folder_path = sys.argv[2]    
    filename = input_image_path.split("\\")[-1]
    filename_without_extension = filename.split(".")[0]
    img = io.imread(input_image_path)

    # create folder if not exists
    os.makedirs(output_folder_path, exist_ok=True)

    # first step is to reduce the number of colors
    reduced_img = reduce_image_colors(img, color_count=5, iteration=1)
    # write image
    io.imsave(f"{output_folder_path}/{filename_without_extension}_reduced.png", reduced_img)

    # second step is to remove noise
    sanitized_reduced_img = sanitize_noise(reduced_img, percentage=0.1)
    # write image
    io.imsave(f"{output_folder_path}/{filename_without_extension}_reduced_sanitized.png", sanitized_reduced_img)

    # third step is to get the outline
    outline_mask = get_outline_binary_mask(sanitized_reduced_img)
    outline_img = np.array(sanitized_reduced_img)
    outline_img[outline_mask] = [0, 0, 0]
    # write image
    io.imsave(f"{output_folder_path}/{filename_without_extension}_reduced_sanitized_outline.png", outline_img)

    # sanitize again after outline
    sanitized_outline_img = sanitize_noise(outline_img, percentage=0.1)
    # write image
    io.imsave(f"{output_folder_path}/{filename_without_extension}_reduced_sanitized_outline_sanitized.png", sanitized_outline_img)
    exit(0)

    '''
        GO TO https://png2svg.com/
        UPLOAD reduced_sanitized.png
        DOWNLOAD reduced_sanitized.svg
        RUN THIS SCRIPT AGAIN
    '''
    # create splitted svg folder
    splitted_svg_folder_path = f"{output_folder_path}/{filename_without_extension}_splitted_svg"
    os.makedirs(splitted_svg_folder_path, exist_ok=True)
    # create svgs
    split_svg_by_path(f"{output_folder_path}/{filename_without_extension}_reduced_sanitized.svg", splitted_svg_folder_path, override_color="white")


