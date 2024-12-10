import os
import shutil

def organize_yolo_model(zimages_dir):
    # Get the current working directory (root directory)
    root_dir = os.getcwd()

    # Create Yolo_Model folder structure in the current directory
    yolo_model_dir = os.path.join(root_dir, 'Yolo_Model')
    images_dir = os.path.join(yolo_model_dir, 'images')
    labels_dir = os.path.join(yolo_model_dir, 'labels')

    # Create necessary subdirectories (you can add train/val/test if needed)
    os.makedirs(images_dir, exist_ok=True)
    os.makedirs(labels_dir, exist_ok=True)

    # Get all image and label files
    image_extensions = ['.jpg', '.jpeg', '.png']  # Add other image formats if needed
    files = os.listdir(zimages_dir)
    
    images = [f for f in files if os.path.splitext(f)[1].lower() in image_extensions]
    labels = [f for f in files if f.endswith('.txt')]

    # Move/Copy images and labels to Yolo_Model structure
    for image in images:
        # Copy image to images folder
        src_image_path = os.path.join(zimages_dir, image)
        dst_image_path = os.path.join(images_dir, image)
        shutil.copy(src_image_path, dst_image_path)

    for label in labels:
        # Copy label to labels folder
        src_label_path = os.path.join(zimages_dir, label)
        dst_label_path = os.path.join(labels_dir, label)
        shutil.copy(src_label_path, dst_label_path)

    print(f"Images and labels have been copied to the Yolo_Model structure at: {yolo_model_dir}")

# Define the ZImages directory
zimages_dir = 'ZImages'

organize_yolo_model(zimages_dir)
