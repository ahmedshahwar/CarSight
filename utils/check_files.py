import os

def check_annotations(images_dir, labels_dir):
    # Get all image files and label files
    image_extensions = ['.jpg', '.jpeg', '.png']  # Add other image formats if needed
    images = [f for f in os.listdir(images_dir) if os.path.splitext(f)[1].lower() in image_extensions]
    labels = [f for f in os.listdir(labels_dir) if f.endswith('.txt')]

    # Strip extensions to compare filenames
    image_names = {os.path.splitext(f)[0] for f in images}
    label_names = {os.path.splitext(f)[0] for f in labels}

    # Find images without labels
    images_without_labels = image_names - label_names
    # Find labels without images
    labels_without_images = label_names - image_names

    # Count the number of image and label files
    num_images = len(images)
    num_labels = len(labels)

    # Print out results
    print(f"Number of image files: {num_images}")
    print(f"Number of label (.txt) files: {num_labels}")
    
    if images_without_labels:
        print(f"Images without corresponding .txt files: {images_without_labels}")
    else:
        print("All images have corresponding .txt files.")

    if labels_without_images:
        print(f".txt files without corresponding images: {labels_without_images}")
    else:
        print("All .txt files have corresponding images.")

# Set the paths to your images and labels directories
images_dir = 'ZImages'
labels_dir = 'ZImages'

check_annotations(images_dir, labels_dir)
