from pathlib import Path
from glob import glob
from sklearn.model_selection import train_test_split
import shutil
import os


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

def split(images, test_size = None):
    train, test = train_test_split( images, 
                                    test_size = test_size, 
                                    random_state = 42
                                    )
    
    get_label_path = lambda x : str(label_path / Path(x).stem) + '.txt'

    [shutil.copy(x, train_path) for x in train] 
    [shutil.copy(get_label_path(x), train_path) for x in train] 

    [shutil.copy(x, test_path) for x in test] 
    [shutil.copy(get_label_path(x), test_path) for x in test] 
    
    
    '''
    [shutil.copy(x, val_path) for x in val] 
    [shutil.copy(get_label_path(x) + '.txt', val_path) for x in val] 
    '''

if __name__ == '__main__':
    images = [x for x in glob(str(raw_path) + '/*')]
    split(images)




















