import os
import aspose.words as aw
from potrace import Bitmap
import skimage.color as color
import skimage.io as io
import sys
import aspose.imaging as ai

# NOT WORKING: error
def png_to_svg_aspose_ai(input_path, output_path):
    # Charger le fichier PNG avec la méthode Image.load
    png_image = ai.Image.load(input_path)

    # Créer et définir l'instance de la classe SvgOptions
    svg_options = ai.imageoptions.SvgOptions()
    print(ai.fileformats.svg.graphics)
    svg_options.color_type = ai.fileformats.svg.graphics.SvgColorMode.Rgb # Utiliser le mode de couleur RVB
    svg_options.text_as_shapes = True # Convertir le texte en formes

    # Appeler la méthode Image.save
    png_image.save(output_path, svg_options)


# NOT WORKING: pixelized
def png_to_svg_aspose(input_path, output_path):
    #  Create document object
    doc = aw.Document()

    # Create a document builder object
    builder = aw.DocumentBuilder(doc)

    # Load and insert PNG image
    shape = builder.insert_image(input_path)

    # Specify image save format as SVG
    saveOptions = aw.saving.ImageSaveOptions(aw.SaveFormat.SVG)

    # Save image as SVG
    shape.get_shape_renderer().save(output_path, saveOptions)

# NOT WORKING: grayscale + write_svg not exist
def png_to_svg_potrace(input_path, output_path):
    # read image 
    img = io.imread(input_path)
    if img.shape[2] == 4:
        img = img[:,:,:3]
    # convert to greyscale
    img = color.rgb2gray(img)

    bitmap = Bitmap(img)
    path = bitmap.trace()
    path.write_svg(output_path)

# NOT WORKING: potrace grayscale
def png_to_svg_potrace_cli(input_path, output_path, hex_color="#FFFFFF"):
    command = f'potracer {input_path} -o {output_path} -C "{hex_color}"'
    print(command)
    os.system(command)

if __name__ == "__main__":
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    png_to_svg_potrace_cli(input_path, output_path)
    