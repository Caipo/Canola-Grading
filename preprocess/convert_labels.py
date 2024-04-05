import os
import xml.etree.ElementTree as ET
import cv2
from pathlib import Path
from glob import glob
import os

current = Path(__file__).parent
xml_dir = current / 'raw_labels'
output_dir = current.parent / 'dataset' / 'grain_data' / 'labels'

os.makedirs(output_dir, exist_ok = True)

def make_lables(file):
    file = Path(file)
    with open(file, 'r') as f:
        tree = ET.parse(file)
        root = tree.getroot()

        
        for image in root.findall('image'):

            image_width = float(image.get('width'))
            image_height = float(image.get('height'))
            name = image.get('name')

            data = list()

            for box in image.findall('box'):
                label = box.get('label')
                x_min = float(box.get('xtl'))
                y_min = float(box.get('ytl'))
                x_max = float(box.get('xbr'))
                y_max = float(box.get('ybr'))

                x_center = round((x_min + x_max) / 2)
                width = round(x_max - x_min)

                y_center = round((y_min + y_max) / 2)
                height = round(y_max - y_min)

                x_center = x_center / image_width
                width = width / image_width
                
                y_center = y_center / image_height
                height = height / image_height

                data.append(f'{label} {x_center} {y_center} {width} {height}')

            with open(output_dir / (name.replace('.jpg', '.txt')), 'w') as write_file:
                write_file.write('\n'.join(data))

if __name__ == '__main__':
    files = [x for x in glob(str(xml_dir) + '/*')]
    for file in files:
        make_lables(file)
