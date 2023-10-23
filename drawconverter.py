import sys
sys.path.append('./')
from imagecolorreducer import reduce_image_colors
from noisesanitizer import sanitize_noise
import skimage.io as io
import os

def convert_image(input_image_path, output_folder_path):
    filename = input_image_path.split("\\")[-1]
    filename_without_extension = filename.split(".")[0]
    path_builder = f"{output_folder_path}/{filename_without_extension}_"

    reduced_img_output_path = f"{path_builder}reduced.png"
    sanitized_reduced_img_output_path = f"{path_builder}reduced_sanitized.png"


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

if __name__ == "__main__":
    input_path = sys.argv[1]
    # if folder find first file that is a png or jpg
    if os.path.isdir(input_path):
        input_image_path = None
        image_extensions = [".png", ".jpg"]
        for file in os.listdir(input_path):
            if file.endswith(tuple(image_extensions)):
                input_image_path = f"{input_path}/{file}"
                break
    else:
        input_image_path = input_path

    input_image_folder_path = input_image_path.split("\\")[:-1]
    input_image_folder_path = "\\".join(input_image_folder_path)
    output_folder_path = f"{input_image_folder_path}"
    convert_image(input_image_path, output_folder_path)
    