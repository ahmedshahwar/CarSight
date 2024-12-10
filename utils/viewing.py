import os
import cv2

# Function to load YOLO annotations from a txt file
def load_yolo_annotations(annotations_file):
    with open(annotations_file, 'r') as file:
        annotations = file.readlines()
    return [list(map(float, line.strip().split())) for line in annotations]

# Function to display bounding boxes on the image
def display_bounding_boxes(image_path, annotations, class_names):
    image = cv2.imread(image_path)
    h, w, _ = image.shape

    for annotation in annotations:
        class_id, x_center, y_center, bbox_width, bbox_height = annotation

        # Convert YOLO format (normalized) to actual pixel coordinates
        x_center, y_center = int(x_center * w), int(y_center * h)
        bbox_width, bbox_height = int(bbox_width * w), int(bbox_height * h)

        # Calculate the top-left corner of the bounding box
        x_min = int(x_center - bbox_width / 2)
        y_min = int(y_center - bbox_height / 2)
        x_max = int(x_center + bbox_width / 2)
        y_max = int(y_center + bbox_height / 2)

        # Draw the bounding box
        cv2.rectangle(image, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)

        # Put the class label text on the bounding box
        class_label = class_names[int(class_id)]
        cv2.putText(image, f'{class_label} ({int(class_id)})', (x_min, y_min - 10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    # Show the image with bounding boxes using cv2.imshow()
    cv2.imshow('Image with Bounding Boxes', image)
    
    # Wait for a key press; if 'q' is pressed, exit
    key = cv2.waitKey(0)
    if key == ord('q'):  # Press 'q' to quit
        cv2.destroyAllWindows()
        return False
    cv2.destroyAllWindows()  # Close the window for the next image
    return True

# Main function to process images and annotations
def process_images_with_bboxes(images_dir, annotations_dir, classes_file):
    # Load class names from classes.txt
    with open(classes_file, 'r') as file:
        class_names = [line.strip() for line in file.readlines()]

    # Iterate over the images in the directory
    for image_file in os.listdir(images_dir):
        if image_file.endswith(".jpeg"):
            image_path = os.path.join(images_dir, image_file)

            # Get corresponding annotation file
            annotation_file = os.path.join(annotations_dir, os.path.splitext(image_file)[0] + ".txt")
            if os.path.exists(annotation_file):
                # Load YOLO annotations
                annotations = load_yolo_annotations(annotation_file)

                # Display image with bounding boxes
                if not display_bounding_boxes(image_path, annotations, class_names):
                    break  # Exit if 'q' is pressed

# Main entry point
if __name__ == "__main__":
    images_dir = 'ZImages'  # Path to the directory with images
    annotations_dir = 'Labels'  # Path to the directory with YOLO annotations
    classes_file = 'new_classes.txt'  # Path to classes.txt

    process_images_with_bboxes(images_dir, annotations_dir, classes_file)
