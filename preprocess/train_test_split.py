from pathlib import Path
from glob import glob
from sklearn.model_selection import train_test_split
import shutil


raw_path = Path.cwd() / 'raw_images'
dataset_path = Path.cwd().parent / 'dataset' / 'grain_data' 
label_path = Path.cwd().parent / 'dataset' / 'processed_labels'
train_path = dataset_path / 'train'
test_path = dataset_path / 'test'
val_path = dataset_path / 'val'

def split(images, test_size = 0.1):
    train, test = train_test_split( images, 
                                    test_size = test_size, 
                                    random_state = 42
                                    )

    
    get_label_path = lambda x : str(label_path / Path(x).stem) + '.txt'

    [shutil.copy(x, train_path) for x in train] 
    [shutil.copy(get_label_path(x), train_path) for x in train] 

    [shutil.copy(x, test_path) for x in test] 
    [shutil.copy(get_label_path(x) + '.txt', test_path) for x in test] 
    
    
    '''
    [shutil.copy(x, val_path) for x in val] 
    [shutil.copy(get_label_path(x) + '.txt', val_path) for x in val] 
    '''

if __name__ == '__main__':
    images = [x for x in glob(str(raw_path) + '/*')]
    split(images)




















