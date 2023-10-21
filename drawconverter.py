import sys
sys.path.append('./')
from imagecolorreducer import reduce_image_colors
from noisesanitizer import sanitize_noise
from imageoutliner import get_outline_binary_mask, make_outline_img, outline_sanitize
from svgsplitter import split_svg_by_path
import numpy as np
import skimage.io as io
import os

if __name__ == "__main__":
    input_image_path = sys.argv[1]
    output_folder_path = sys.argv[2]    
    filename = input_image_path.split("\\")[-1]
    filename_without_extension = filename.split(".")[0]
    path_builder = f"{output_folder_path}/{filename_without_extension}_"

    reduced_img_output_path = f"{path_builder}reduced.png"
    sanitized_reduced_img_output_path = f"{path_builder}reduced_sanitized.png"
    outline_img_output_path = f"{path_builder}reduced_sanitized_outline.png"
    outline_img_output_path = f"{path_builder}reduced_sanitized_outline_sanitized.png"


    # create folder if not exists
    os.makedirs(output_folder_path, exist_ok=True)

    # first step is to reduce the number of colors
    img = io.imread(input_image_path)
    reduced_img = reduce_image_colors(img, color_count=10, iteration=1)
    # write image
    io.imsave(reduced_img_output_path, reduced_img)

    # second step is to remove noise
    reduced_img = io.imread(reduced_img_output_path)
    sanitized_reduced_img = sanitize_noise(reduced_img, percentage=0.1)
    # write image
    io.imsave(sanitized_reduced_img_output_path, sanitized_reduced_img)

    # # # third step is to get the outline
    # sanitized_reduced_img = io.imread(sanitized_reduced_img_output_path)
    # outline_img = make_outline_img(sanitized_reduced_img)
    # # write image
    # io.imsave(outline_img_output_path, outline_img)

    # # sanitize outline
    # outline_img = io.imread(outline_img_output_path)
    # sanitized_outline_img = outline_sanitize(outline_img)
    # # write image
    # io.imsave(outline_img_output_path, sanitized_outline_img)
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


