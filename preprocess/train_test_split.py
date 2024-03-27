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


os.makedirs(label_path, exist_ok = True)
os.makedirs(train_path, exist_ok = True)
os.makedirs(test_path, exist_ok = True)
os.makedirs(val_path, exist_ok = True)


def get_args():
    parser = argparse.ArgumentParser(description="Just an example",
                        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("--test_size", type=float, help="percentage split of train")
    parser.add_argument("--val_size", type=float, help="percentage split of val")
    parser.add_argument('--dvc', action='store_true', help='Train via DVC pipeline')

    args = parser.parse_args()
    return vars(args)


def split(images, test_size = None, val_size = None):
    train, test = train_test_split( images, 
                                    test_size = test_size, 
                                    random_state = 42
                                    )
    
    train, val = train_test_split( train, 
                                    test_size = val_size, 
                                    random_state = 42
                                    )

    get_label_path = lambda x : str(label_path / Path(x).stem) + '.txt'

    [shutil.copy(x, train_path) for x in train] 
    [shutil.copy(get_label_path(x), train_path) for x in train] 

    [shutil.copy(x, test_path) for x in test] 
    [shutil.copy(get_label_path(x), test_path) for x in test] 
    
    [shutil.copy(x, val_path) for x in val] 
    [shutil.copy(get_label_path(x), val_path) for x in val] 

if __name__ == '__main__':
    images = [x for x in glob(str(raw_path) + '/*')]
    args = get_args()

    if args['dvc']:
        with open('params.yaml') as file:
            params = yaml.safe_load(file)
            val_size = params['split']['val_size']
            test_size = params['split']['test_size']
    else:
        val_size = args['val_size']
        test_size = args['test_size']
    
    if val_size == 0:
        val_size = None

    if test_size == 0:
        test_size = None

    split(images, test_size, val_size)





















