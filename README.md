# image-to-abstract-coloring
Transform an image into an abstract image with limited colors.<br>
Don't use excessively large images as it may take too much time.<br>
# Install and requirements
Python 3.11.0<br>
Use this command to install required packages:<br>
pip install -r requirements.txt
# How to run it
```
usage: drawconverter.py [-h] [--output_folder_path OUTPUT_FOLDER_PATH] [--color_count COLOR_COUNT] [--sanitize_weight SANITIZE_WEIGHT] input_path

Transform an image into an abstract image with limited colors. Don't use excessively large images as it may take too much time.

positional arguments:
  input_path            Path to an image file or a directory

options:
  -h, --help            show this help message and exit
  --output_folder_path OUTPUT_FOLDER_PATH, -o OUTPUT_FOLDER_PATH
                        Path to the output folder. If not specified, it defaults to the directory of the input path.
  --color_count COLOR_COUNT, -c COLOR_COUNT
                        Number of colors to use in the abstract image (default: 10)
  --sanitize_weight SANITIZE_WEIGHT, -s SANITIZE_WEIGHT
                        Level of sanitization applied to the image (0 to 1) (default: 0.1)
```
# Example
The folder "example" contain only one image. After using the command, two more images will be generated in the same folder.<br>
python drawconverter.py example
<br><br>
![Source image](https://github.com/tdautreme/image-to-abstract-coloring/blob/main/example/lion.jpg?raw=true)
![Color reduced](https://github.com/tdautreme/image-to-abstract-coloring/blob/main/example/lion_reduced.png?raw=true)
![Color reduced and sanitized](https://github.com/tdautreme/image-to-abstract-coloring/blob/main/example/lion_reduced_sanitized.png?raw=true)

