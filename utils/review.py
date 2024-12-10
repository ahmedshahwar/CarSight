##-------------------------------------------------------------------------------------------------------##
##-------------------------------------------------------------------------------------------------------##
##                                      REMOVE NULL LABELS                                               ##
##-------------------------------------------------------------------------------------------------------##
##-------------------------------------------------------------------------------------------------------##

# import os

# # Function to load the classes from the txt file and remove "null_*" labels
# def load_and_clean_classes(file_path):
#     with open(file_path, 'r') as file:
#         classes = file.readlines()

#     # Remove any class starting with "null"
#     cleaned_classes = [label.strip() for label in classes if not label.startswith("null")]
#     return cleaned_classes

# # Function to update annotation files by adjusting class indices
# def update_annotations(annotation_dir, old_classes, new_classes):
#     class_index_mapping = {}
    
#     # Build a mapping from old index to new index
#     for i, old_class in enumerate(old_classes):
#         if old_class in new_classes:
#             new_index = new_classes.index(old_class)
#             class_index_mapping[i] = new_index
#         # Skip the "null_*" labels (they won't have a corresponding new index)

#     # Update each annotation file
#     for file_name in os.listdir(annotation_dir):
#          # Skip the 'classes.txt' file itself
#         if file_name == 'classes.txt':
#             continue
        
#         if file_name.endswith(".txt"):
#             file_path = os.path.join(annotation_dir, file_name)
#             with open(file_path, 'r') as file:
#                 annotations = file.readlines()

#             updated_annotations = []
#             for annotation in annotations:
#                 elements = annotation.split()
#                 class_index = int(elements[0])

#                 # Skip annotations that had a "null_*" label
#                 if class_index in class_index_mapping:
#                     new_class_index = class_index_mapping[class_index]
#                     elements[0] = str(new_class_index)
#                     updated_annotations.append(" ".join(elements) + "\n")

#             # Save the updated annotations
#             with open(file_path, 'w') as file:
#                 file.writelines(updated_annotations)

# # Function to write the new cleaned classes.txt file
# def write_new_classes_file(output_file_path, new_classes):
#     with open(output_file_path, 'w') as file:
#         for label in new_classes:
#             file.write(f"{label}\n")

# # Main function to run the script
# def main():
#     old_classes_file = 'Images_2.0/classes.txt'  # Path to your original classes.txt
#     new_classes_file = 'new_classes.txt'  # Path where new classes.txt will be saved
#     annotation_dir = 'Images_2.0/'  # Path to the directory containing annotation files

#     # Load the old classes and clean the list
#     old_classes = load_and_clean_classes(old_classes_file)

#     # Remove "null_*" and create the cleaned list of new classes
#     new_classes = [label for label in old_classes if not label.startswith("null")]

#     # Write the new cleaned classes.txt
#     write_new_classes_file(new_classes_file, new_classes)

#     # Update the annotations based on the new class indices
#     update_annotations(annotation_dir, old_classes, new_classes)

#     print(f"Updated classes.txt saved to {new_classes_file}")
#     print(f"Annotation files updated successfully in {annotation_dir}")

# if __name__ == "__main__":
#     main()


##-------------------------------------------------------------------------------------------------------##
##-------------------------------------------------------------------------------------------------------##
##                                      CHECK FOR SPECIFIC LABEL                                         ##
##-------------------------------------------------------------------------------------------------------##
##-------------------------------------------------------------------------------------------------------##

# import cv2
# import os

# # Path to your images and annotations
# image_folder = 'Images_2.0'
# annotation_folder = 'Images_2.0'

# # Classes to filter
# target_classes = [89, 90, 91, 92, 93]

# # List to store the names of the files that contain the target classes
# files_with_target_classes = []

# # Loop through the annotations
# for filename in os.listdir(annotation_folder):
#     if filename.endswith('.txt'):
#         image_name = filename.replace('.txt', '.jpeg')  # Assuming images are in .jpeg format
#         annotation_path = os.path.join(annotation_folder, filename)

#         # Flag to check if the file contains any of the target classes
#         contains_target_class = False

#         # Read the annotation file
#         with open(annotation_path, 'r') as file:
#             for line in file:
#                 try:
#                     # Try converting values to float
#                     class_index, x_center, y_center, w, h = map(float, line.strip().split())
                    
#                     # If the class index is in the target classes, mark the file for display
#                     if int(class_index) in target_classes:
#                         contains_target_class = True
#                         break  # No need to check further; we found a matching class

#                 except ValueError:
#                     print(f"Skipping invalid line in file: {filename} - {line.strip()}")
#                     continue  # Skip invalid lines

#         # If the file contains a target class, add it to the list
#         if contains_target_class:
#             files_with_target_classes.append(image_name)

# # Display the files with the target classes
# for image_name in files_with_target_classes:
#     image_path = os.path.join(image_folder, image_name)
    
#     # Read the image
#     image = cv2.imread(image_path)

#     # Check if the image was loaded successfully
#     if image is None:
#         print(f"Error loading image: {image_path}")
#         continue

#     # Display the filename on the image
#     cv2.putText(image, image_name, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

#     # Show the image
#     cv2.imshow('Image with Target Classes', image)
#     cv2.waitKey(0)  # Press any key to move to the next image

# cv2.destroyAllWindows()

# # Output the names of the files with target classes
# print("Files with target classes:")
# for file_name in files_with_target_classes:
#     print(file_name)


##-------------------------------------------------------------------------------------------------------##
##-------------------------------------------------------------------------------------------------------##
##                                  VIEW IMAGES WITH BOUNDING BOXES                                      ##
##-------------------------------------------------------------------------------------------------------##
##-------------------------------------------------------------------------------------------------------##

import cv2
import os

# Path to your images and annotations
image_folder = 'ZImages'
annotation_folder = 'ZImages'
classes_file = 'ZImages/classes.txt'  # Path to your classes.txt file

# Load class names from classes.txt
with open(classes_file, 'r') as file:
    class_names = [line.strip() for line in file.readlines()]

# Target classes to look for
target_classes = {89, 90, 91, 92, 93}

# Loop through the annotations
for filename in os.listdir(annotation_folder):
    if filename.endswith('.txt'):
        # Skip the classes.txt file itself
        if filename == 'classes.txt':
            continue
        
        image_name = filename.replace('.txt', '.jpeg')  # Assuming images are in .jpeg format
        image_path = os.path.join(image_folder, image_name)
        annotation_path = os.path.join(annotation_folder, filename)

        # Read the annotation file
        display_image = False
        with open(annotation_path, 'r') as file:
            for line in file:
                class_index, x_center, y_center, w, h = map(float, line.strip().split())

                # Check if the class index is one of the target classes
                if int(class_index) in target_classes:
                    display_image = True
                    break  # No need to continue reading if the class is found

        # Display the image if it contains one of the target classes
        if display_image:
            # Read the image
            image = cv2.imread(image_path)

            # Check if the image was loaded successfully
            if image is None:
                print(f"Error loading image: {image_path}")
                continue

            # Get image dimensions
            height, width, _ = image.shape

            # Read the annotation file again to draw all bounding boxes
            with open(annotation_path, 'r') as file:
                for line in file:
                    class_index, x_center, y_center, w, h = map(float, line.strip().split())

                    # Convert YOLO format to bounding box coordinates
                    x_min = int((x_center - w / 2) * width)
                    y_min = int((y_center - h / 2) * height)
                    x_max = int((x_center + w / 2) * width)
                    y_max = int((y_center + h / 2) * height)

                    # Draw the bounding box and class name on the image
                    class_name = class_names[int(class_index)] if int(class_index) < len(class_names) else f'Class {int(class_index)}'
                    cv2.rectangle(image, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
                    cv2.putText(image, f'{class_name} ({int(class_index)})', (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)

            # Display the image with bounding boxes and filename
            cv2.putText(image, image_name, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)
            cv2.imshow('Annotated Image', image)
            cv2.waitKey(0)  # Press any key to close the image

cv2.destroyAllWindows()
