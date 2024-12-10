import os
import re

# Function to load the classes from a txt file
def load_classes(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    return [line.strip() for line in lines]

# Function to map old label to new label considering year ranges
def map_old_to_new_label(old_label, new_classes):
    if old_label.startswith("null"):
        return None  # Skip null labels
    
    match_old = re.match(r'(.*)_(\d{4})$', old_label)
    if not match_old:
        return old_label  # If no year is found, return the label as is

    base_old_label = match_old.group(1)
    old_year = int(match_old.group(2))

    for new_label in new_classes:
        match_new = re.match(r'(.*)_(\d{4})(-(\d{4}))?$', new_label)
        if match_new:
            base_new_label = match_new.group(1)
            start_year = int(match_new.group(2))
            end_year = int(match_new.group(4)) if match_new.group(4) else start_year

            if base_old_label == base_new_label and start_year <= old_year <= end_year:
                return new_label  # Return the new label if it falls within the year range

    return old_label  # If no match is found, return the old label

# Function to update annotation files with new label mappings and save in a new folder
def update_annotations(annotation_dir, output_dir, old_classes, new_classes):
    # Create a mapping from old class index to new class index
    old_to_new_map = {}
    for i, old_label in enumerate(old_classes):
        if old_label.startswith("null"):
            continue  # Skip null labels
        
        new_label = map_old_to_new_label(old_label, new_classes)
        if new_label is None:
            continue  # Skip mapping for null labels

        old_to_new_map[i] = new_classes.index(new_label)

    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Update each annotation file
    for file_name in os.listdir(annotation_dir):
        if file_name == 'classes.txt':
            continue
            
        if file_name.endswith(".txt"):
            file_path = os.path.join(annotation_dir, file_name)
            with open(file_path, 'r') as file:
                annotations = file.readlines()

            updated_annotations = []
            for annotation in annotations:
                elements = annotation.split()
                class_index = int(elements[0])  # First element is the class index
                if class_index in old_to_new_map:
                    new_class_index = old_to_new_map.get(class_index, class_index)  # Map old index to new
                    elements[0] = str(new_class_index)
                    updated_annotations.append(" ".join(elements) + "\n")

            # Save the updated annotations to the new folder
            output_file_path = os.path.join(output_dir, file_name)
            with open(output_file_path, 'w') as file:
                file.writelines(updated_annotations)

# Main function to run the script
def main():
    old_classes_file = 'ZImages/classes.txt'  # Path to old classes.txt
    new_classes_file = 'new_classes.txt'  # Path to new classes.txt
    annotation_dir = 'ZImages/'  # Directory with original annotation files
    output_dir = 'Labels/'  # Directory where updated annotation files will be saved

    # Load old and new classes
    old_classes = load_classes(old_classes_file)
    new_classes = load_classes(new_classes_file)

    # Update annotation files and save them in the new folder
    update_annotations(annotation_dir, output_dir, old_classes, new_classes)
    print(f"Annotation files updated and saved in '{output_dir}'.")

if __name__ == "__main__":
    main()
