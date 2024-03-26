import os
import xml.etree.ElementTree as ET
import cv2
from pathlib import Path
from glob import glob

current = Path.cwd()
xml_dir = current / 'raw_labels'
output_dir = current / 'processed_labels'

def make_lables(file):
    file = Path(file)
    with open(file, 'r') as f:
        tree = ET.parse(file)
        root = tree.getroot()

        image_width = int(root.find('size').find('width').text)
        image_height = int(root.find('size').find('height').text)

        data = list()
        for obj in root.findall('object'):
            name = obj.find('name').text
            box = obj.find('bndbox')
            x_min = float(box.find('xmin').text)
            y_min = float(box.find('ymin').text)
            x_max = float(box.find('xmax').text)
            y_max = float(box.find('ymax').text)

            x_center = round((x_min + x_max) / 2)
            width = round(x_max - x_min)

            y_center = round((y_min + y_max) / 2)
            height = round(y_max - y_min)

            x_center = x_center / image_width
            width = width / image_width
            
            y_center = y_center / image_height
            height = height / image_height

            data.append(f'{name} {x_center} {y_center} {width} {height}')

    with open(output_dir / (file.stem + '.txt'), 'w') as write_file:
        write_file.write('\n'.join(data))


def convert_labels():
    files = [x for x in glob(str(xml_dir) + '/*')]
    for file in files:
        print(file)
        make_lables(file)

