from pathlib import Path
from glob import glob
from sklearn.model_selection import train_test_split
import shutil


raw_path = Path.cwd() / 'raw_images'
dataset_path = Path.cwd().parent / 'dataset' / 'grain_data' 
label_path = Path.cwd() / 'processed_labels'
train_path = dataset_path / 'train'
test_path = dataset_path / 'test'
val_path = dataset_path / 'val'

def split(images, test_size):
    train, test = train_test_split(images, test_size = 0.1, random_state = 42)

    [shutil.copy(x, train_path) for x in train] 
    [shutil.copy(str(label_path / Path(x).stem) + '.txt', train_path) for x in train] 

    [shutil.copy(x, test_path) for x in test] 
    [shutil.copy(str(label_path / Path(x).stem) + '.txt', test_path) for x in test] 
    
    
def split_data_set()    
    images = [x for x in glob(str(raw_path) + '/*')]
    split(images)




















