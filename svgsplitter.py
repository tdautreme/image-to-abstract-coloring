
import svgwrite
from xml.etree import ElementTree
import json
import svgwrite
import re
import os
from lxml import etree
import sys

def extract_coord(path_data):
    minX = float('inf')
    minY = float('inf')
    maxX = float('-inf')
    maxY = float('-inf')

    # Analize path data
    commands = re.findall(r'([MLHVCSQTAZmlhvcsqtaz])\s*([^MLHVCSQTAZmlhvcsqtaz]*)', path_data)

    for command, params in commands:
        params = params.strip()
        params = re.split(r'[ ,]+', params)

        if command in ['M', 'L', 'H', 'V']:
            for i in range(0, len(params), 2):
                x = float(params[i])
                y = float(params[i + 1])
                minX = min(minX, x)
                minY = min(minY, y)
                maxX = max(maxX, x)
                maxY = max(maxY, y)
        elif command in ['C', 'S', 'Q', 'T']:
            for i in range(0, len(params), 2):
                x = float(params[i])
                y = float(params[i + 1])
                minX = min(minX, x)
                minY = min(minY, y)
                maxX = max(maxX, x)
                maxY = max(maxY, y)
        elif command in ['A']:
            for i in range(5, len(params), 5):
                x = float(params[i])
                y = float(params[i + 1])
                minX = min(minX, x)
                minY = min(minY, y)
                maxX = max(maxX, x)
                maxY = max(maxY, y)

    return minY, minX, maxY, maxX

# WORK ONLY WITH https://png2svg.com/
def split_svg_by_path(input_path, output_dir, override_color=None):
    # Load SVG file
    tree = ElementTree.parse(input_path)
    root = tree.getroot()

    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Fetch SVG width and height
    svg_width = float(root.get('width').replace('px', ''))
    svg_height = float(root.get('height').replace('px', ''))
    print("width", svg_width, "height", svg_height)

    # Initialiser un dictionnaire pour stocker les coordonnées normalisées
    json_data = {
        "width": svg_width,
        "height": svg_height,
        "images": [],
    }

    # Parcourir les éléments <path> et les enregistrer dans des fichiers distincts
    for i, path_element in enumerate(root.findall('.//{http://www.w3.org/2000/svg}path')):

        filename_svg = f'output_{i}.svg'
        # Créer un nouveau document SVG pour chaque chemin
        svg = svgwrite.Drawing(filename=os.path.join(output_dir, filename_svg), profile='tiny', size=('100%', '100%'))

        # Créer un nouvel objet path et ajouter les attributs
        path_data = path_element.attrib['d']
        path = svg.path(d=path_data)

        # Obtenir la couleur de remplissage (fill) du chemin
        sprite_color = path_element.get('fill', 'none')
        if override_color is None:
            fill_color = sprite_color
        else:
            fill_color = override_color
        # Définir la trait en blanc et la couleur de remplissage avec la couleur extraite
        # path.stroke("black")
        # path.fill(fill_color)
        path.fill(fill_color)

        svg.add(path)

        # Enregistrer le nouveau document
        svg.save()

        # Extraire les coordonnées et tailles
        minY, minX, maxY, maxX = extract_coord(path_data)
        
        # Stocker les coordonnées dans le dictionnaire
        sub_json_data = {
            "filename": filename_svg,
            "minY": minY,
            "minX": minX,
            "maxY": maxY,
            "maxX": maxX,
            "color": sprite_color,
        }
        json_data["images"].append(sub_json_data)


    # check if coord are out of bound, then compute offset and apply it
    minY = float('inf')
    minX = float('inf')
    for image in json_data["images"]:
        minY = min(minY, image["minY"])
        minX = min(minX, image["minX"])

    offset_y = 0
    offset_x = 0
    if minY < 0:
        offset_y = -minY
    if minX < 0:
        offset_x = -minX

    for image in json_data["images"]:
        image["minY"] += offset_y
        image["minX"] += offset_x
        image["maxY"] += offset_y
        image["maxX"] += offset_x

    # Write json as data.json at output_dir
    with open(f'{output_dir}/data.json', 'w') as outfile:
        json.dump(json_data, outfile, indent=4)

    return json_data



def split_svg_by_color(input_file, output_dir):
    # Load SVG file
    tree = etree.parse(input_file)
    root = tree.getroot()

    # Create dictionary to store shapes by color
    color_shapes = {}

    for shape in root.findall(".//{http://www.w3.org/2000/svg}path"):
        color = shape.get('fill')
        if color not in color_shapes:
            color_shapes[color] = []
        color_shapes[color].append(shape)

    # For each color, create a new SVG file
    for color, shapes in color_shapes.items():
        new_tree = etree.ElementTree(etree.Element(root.tag, nsmap=root.nsmap))
        new_root = new_tree.getroot()

        for shape in shapes:
            new_root.append(shape)

        # Write new SVG file
        output_file = f"{output_dir}/output_{color.replace('#', '')}.svg"
        new_tree.write(output_file, pretty_print=True)


if __name__ == "__main__":
    input_path = sys.argv[1]
    output_folder_path = sys.argv[2]
    split_svg_by_path(input_path, output_folder_path)