import sys
sys.path.append('./')
from imagecolorreducer import reduce_image_colors
from noisesanitizer import sanitize_noise
import skimage.io as io
import os
import argparse

def convert_image(input_image_path, output_folder_path, color_count=10, sanitize_weight=0.1):
    filename = input_image_path.split("\\")[-1]
    filename_without_extension = filename.split(".")[0]
    path_builder = f"{output_folder_path}/{filename_without_extension}_"

    reduced_img_output_path = f"{path_builder}reduced.png"
    sanitized_reduced_img_output_path = f"{path_builder}reduced_sanitized.png"


    # create folder if not exists
    os.makedirs(output_folder_path, exist_ok=True)

    # first step is to reduce the number of colors
    img = io.imread(input_image_path)
    print("reducing colors on ", input_image_path)
    reduced_img = reduce_image_colors(img, color_count=color_count, iteration=1)
    # write image
    io.imsave(reduced_img_output_path, reduced_img)

    # second step is to remove noise
    reduced_img = io.imread(reduced_img_output_path)
    print("removing noise on ", reduced_img_output_path)
    sanitized_reduced_img = sanitize_noise(reduced_img, weight=sanitize_weight)
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
    '''
        GO TO https://png2svg.com/
        UPLOAD reduced_sanitized.png
        DOWNLOAD reduced_sanitized.svg
        RUN THIS SCRIPT AGAIN
    '''

def main(input_path, output_folder_path=None, color_count=10, sanitize_weight=0.1):
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
    if output_folder_path is None:
        output_folder_path = f"{input_image_folder_path}"
    convert_image(input_image_path, output_folder_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Transform an image into an abstract image with limited colors.\nDon't use excessively large images as it may take too much time.")

    parser.add_argument("input_path", help="Path to an image file or a directory")
    parser.add_argument(
        "--output_folder_path", "-o",
        help="Path to the output folder. If not specified, it defaults to the directory of the input path."
    )
    parser.add_argument(
        "--color_count", "-c",
        type=int, default=10,
        help="Number of colors to use in the abstract image (default: 10)"
    )
    parser.add_argument(
        "--sanitize_weight", "-s",
        type=float, default=0.1,
        help="Level of sanitization applied to the image (0 to 1) (default: 0.1)"
    )

    args = parser.parse_args()

    # If the output folder path is not specified, use the same folder as input_path
    if args.output_folder_path is None:
        if os.path.isfile(args.input_path):
            output_folder_path = os.path.dirname(args.input_path)
        elif os.path.isdir(args.input_path):
            output_folder_path = args.input_path
        else:
            print("The specified input path is neither a valid file nor a directory.")
            exit(1)

    main(args.input_path, output_folder_path, args.color_count, args.sanitize_weight)