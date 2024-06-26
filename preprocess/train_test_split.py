from pathlib import Path
from glob import glob
from sklearn.model_selection import train_test_split
import shutil
import os
import argparse
import yaml

current_dir = Path(__file__).parent
raw_path = current_dir / 'raw_images'
dataset_path = current_dir.parent / 'dataset' / 'grain_data' 
label_path = dataset_path / 'labels'
train_path = dataset_path / 'train'
test_path = dataset_path / 'test'
val_path = dataset_path / 'val'
manual_path = current_dir / 'manual_sets'

os.makedirs(label_path, exist_ok = True)
os.makedirs(train_path, exist_ok = True)
os.makedirs(test_path, exist_ok = True)
os.makedirs(val_path, exist_ok = True)




def get_args():
    parser = argparse.ArgumentParser(description="Just an example",
                        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("--val_size", type=float, help="percentage split of val")
    parser.add_argument('--dvc', action='store_true', help='Train via DVC pipeline')

    args = parser.parse_args()
    return vars(args)

def split(images, val_size = 0):
    val = list()
    #Val test split
    if val_size != 0:
        train, val = train_test_split( images, 
                                        test_size = val_size, 
                                        random_state = 42
                                        )
    else:
        train = images

    get_label_path = lambda x : str(label_path / Path(x).stem) + '.txt'
    
    # Train
    [shutil.copy(x, train_path) for x in train] 
    [shutil.copy(get_label_path(x), train_path) for x in train] 
    
    # Test
    [shutil.copy(x, test_path) for x in test_set] 
    [shutil.copy(get_label_path(x), test_path) for x in test_set] 
    
    # Validation
    [shutil.copy(x, val_path) for x in val] 
    [shutil.copy(get_label_path(x), val_path) for x in val] 



if __name__ == '__main__':
    with open( manual_path / 'remove.txt') as file:
        to_remove = [x.replace('\n' ,'') for x in file]

    with open( manual_path / 'test.txt') as file:
        test_set = [str(raw_path /  x.replace('\n', '')) for x in file]

    # Flilter out the images 
    images = [ x for x in glob(str(raw_path) + '/*') 
                    if not any([name in x for name in to_remove])
             ]

    images = [ x for x in  images 
                    if not any([name in x for name in test_set])
             ]
    
    # Arguments for manual spliting
    args = get_args()
    os.system(f'rm -rf {train_path}/*')
    os.system(f'rm -rf {test_path}/*')
    os.system(f'rm -rf {val_path}/*')
    
    
    # Dvc pipeline arguments
    if args['dvc']:
        with open('params.yaml') as file:
            params = yaml.safe_load(file)
            val_size = params['split']['val_size']
    else:
        val_size = args['val_size']
    
    if val_size is None:
        val_size = 0

    split(images, val_size)
