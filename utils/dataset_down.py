# ===================================================================== #
#                           DATASET DOWNLOAD                            #
# ===================================================================== #
# from roboflow import Roboflow
# rf = Roboflow(api_key="60Xb1TD7Sf0mHTeyFKYa")
# project = rf.workspace("carsightv2").project("carsightv2")
# version = project.version(4)
# dataset = version.download("yolov8")

# ===================================================================== #
#                             SPLIT DATASET                             #
# ===================================================================== #
import os
from sklearn.model_selection import train_test_split
import shutil

base_dir = 'CarSightv2-4'
images_dir = os.path.join(base_dir, "train/images")
labels_dir = os.path.join(base_dir, "train/labels")
new_base_dir = os.path.join('', "dataset")

# Create the new directory structure
new_train_images_dir = os.path.join(new_base_dir, "train/images")
new_train_labels_dir = os.path.join(new_base_dir, "train/labels")
new_val_images_dir = os.path.join(new_base_dir, "valid/images")
new_val_labels_dir = os.path.join(new_base_dir, "valid/labels")
new_test_images_dir = os.path.join(new_base_dir, "test/images")
new_test_labels_dir = os.path.join(new_base_dir, "test/labels")

for path in [new_train_images_dir, new_train_labels_dir, new_val_images_dir, new_val_labels_dir, new_test_images_dir, new_test_labels_dir]:
    os.makedirs(path, exist_ok=True)

# Get all image and label files
image_files = [f for f in os.listdir(images_dir) if f.endswith('.jpg') or f.endswith('.png')]
label_files = [f.replace('.jpg', '.txt').replace('.png', '.txt') for f in image_files]

# Split into train, validation, and test sets (e.g., 70% train, 15% val, 15% test)
train_images, test_images, train_labels, test_labels = train_test_split(image_files, label_files, test_size=0.3, random_state=42)
val_images, test_images, val_labels, test_labels = train_test_split(test_images, test_labels, test_size=0.5, random_state=42)

# Function to copy files to the respective folders
def copy_files(file_list, src_dir, dest_dir):
    for file_name in file_list:
        src_path = os.path.join(src_dir, file_name)
        dest_path = os.path.join(dest_dir, file_name)
        if os.path.exists(src_path):
            shutil.copy(src_path, dest_path)

# Copy files for train set
copy_files(train_images, images_dir, new_train_images_dir)
copy_files(train_labels, labels_dir, new_train_labels_dir)

# Copy files for validation set
copy_files(val_images, images_dir, new_val_images_dir)
copy_files(val_labels, labels_dir, new_val_labels_dir)

# Copy files for test set
copy_files(test_images, images_dir, new_test_images_dir)
copy_files(test_labels, labels_dir, new_test_labels_dir)

print("Dataset split successfully.")