import os
import shutil
from sklearn.model_selection import train_test_split

# Proporciones
train = 0.8
test = 0.1
val = 0.1

# Crear directorios
for folder in ["images/train","images/test","images/val","labels/train","labels/test","labels/val"]:
    if not os.path.exists(folder):
        os.mkdir(folder)

# Read images and labels
images = [os.path.join('images', x) for x in os.listdir('images') if x[-3:] in ("png", "jpg", "bmp")]
labels = [os.path.join('labels', x) for x in os.listdir('labels') if x[-3:] == "txt"]

images.sort()
labels.sort()

# Split the dataset into train-valid-test splits 
train_images, val_images, train_labels, val_labels = train_test_split(images, labels, test_size = test+val, random_state = 1)
val_images, test_images, val_labels, test_labels = train_test_split(val_images, val_labels, test_size = test/(test+val), random_state = 1)

#Utility function to move images 
def move_files_to_folder(list_of_files, destination_folder):
    for f in list_of_files:
        try:
            shutil.move(f, destination_folder)
        except:
            print(f)
            assert False

# Move the splits into their folders
move_files_to_folder(train_images, 'images/train')
move_files_to_folder(val_images, 'images/val/')
move_files_to_folder(test_images, 'images/test/')
move_files_to_folder(train_labels, 'labels/train/')
move_files_to_folder(val_labels, 'labels/val/')
move_files_to_folder(test_labels, 'labels/test/')