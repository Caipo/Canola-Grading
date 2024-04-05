from pathlib import Path
import zipfile
import shutil
import os

zip_path = Path(__file__).parent / 'zip_files'
raw_image_path = Path(__file__).parent / 'raw_images'
raw_label_path = Path(__file__).parent / 'raw_labels'

def unzip_file(zip_file, destination):
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(destination)

if __name__ == '__main__':
    zip_files = [x for x in zip_path.glob('*.zip')]
    temp_file = zip_path / 'temp'


    for zip_file in zip_files:
    
        num_labels = len([x for x in raw_label_path.glob('*.xml')])
        unzip_file(zip_file, temp_file)
        shutil.rmtree(temp_file / '__MACOSX')
        [x.rename(x.with_suffix('.jpeg')) for x in temp_file.rglob('*.jp*g')]
        images = [x for x in temp_file.rglob('*.jp*g')]        
        lables = [x for x in temp_file.rglob('*.xml')]        
        
        for xml_file in lables: 
            xml_file.rename(xml_file.with_name(f'annotation-{num_labels}.xml'))
            num_labels += 1
            shutil.move(xml_file, raw_label_path) 

        for jpeg_file in images:
            shutil.move(jpeg_file(image, raw_image_path)
