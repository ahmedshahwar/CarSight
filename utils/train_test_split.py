import os
import shutil
import random

# Paths
base_dir = 'Yolo_Model'  # Update this to the actual path
images_dir = os.path.join(base_dir, 'images')
labels_dir = os.path.join(base_dir, 'labels')

# Output directories for splits
train_images_dir = os.path.join(images_dir, 'train')
val_images_dir = os.path.join(images_dir, 'val')
test_images_dir = os.path.join(images_dir, 'test')
train_labels_dir = os.path.join(labels_dir, 'train')
val_labels_dir = os.path.join(labels_dir, 'val')
test_labels_dir = os.path.join(labels_dir, 'test')

# Split ratios
train_ratio = 0.7
val_ratio = 0.2
test_ratio = 0.1

# Create output directories
for split in ['train', 'val', 'test']:
    os.makedirs(os.path.join(train_images_dir), exist_ok=True)
    os.makedirs(os.path.join(val_images_dir), exist_ok=True)
    os.makedirs(os.path.join(test_images_dir), exist_ok=True)
    os.makedirs(os.path.join(train_labels_dir), exist_ok=True)
    os.makedirs(os.path.join(val_labels_dir), exist_ok=True)
    os.makedirs(os.path.join(test_labels_dir), exist_ok=True)

# Get all image files
image_files = sorted([f for f in os.listdir(images_dir) if f.endswith('.jpeg')])

# Shuffle files randomly
random.shuffle(image_files)

# Calculate the number of files for each split
total_files = len(image_files)
train_count = int(train_ratio * total_files)
val_count = int(val_ratio * total_files)

# Split the dataset
train_files = image_files[:train_count]
val_files = image_files[train_count:train_count + val_count]
test_files = image_files[train_count + val_count:]

# Helper function to move files
def move_files(file_list, img_dest, lbl_dest):
    for file in file_list:
        # Move image file
        src_img = os.path.join(images_dir, file)
        dest_img = os.path.join(img_dest, file)
        shutil.copy(src_img, dest_img)

        # Move corresponding label file
        label_file = file.replace('.jpeg', '.txt')
        src_lbl = os.path.join(labels_dir, label_file)
        dest_lbl = os.path.join(lbl_dest, label_file)
        
        if os.path.exists(src_lbl):
            shutil.copy(src_lbl, dest_lbl)

# Move the files to their respective folders
move_files(train_files, train_images_dir, train_labels_dir)
move_files(val_files, val_images_dir, val_labels_dir)
move_files(test_files, test_images_dir, test_labels_dir)

# Remove extra images and labels from original directories
for file in image_files:
    if file not in train_files + val_files + test_files:
        os.remove(os.path.join(images_dir, file))
        
        # Remove corresponding label file
        label_file = file.replace('.jpg', '.txt')
        lbl_path = os.path.join(labels_dir, label_file)
        if os.path.exists(lbl_path):
            os.remove(lbl_path)

print("Dataset successfully split into train, validation, and test sets, and extra files removed.")
