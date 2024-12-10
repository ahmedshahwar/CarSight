import re

# Function to load classes from the file and clean them
def load_and_clean_classes(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Create a dictionary to store merged labels and a list to store non-year labels
    labels_dict = {}
    other_labels = []

    for label in lines:
        label = label.strip()
        
        # Skip null labels
        if label.startswith("null"):
            continue

        # Check if the label matches make_model_variant_year pattern
        match = re.match(r'(.*)_(\d{4})$', label)
        if match:
            base_label = match.group(1)
            year = match.group(2)
            if base_label in labels_dict:
                labels_dict[base_label].append(int(year))
            else:
                labels_dict[base_label] = [int(year)]
        else:
            # If it's not a year-based label, keep it in the other_labels list
            other_labels.append(label)

    # Merge year ranges and update labels
    merged_labels = []
    for base_label, years in labels_dict.items():
        years = sorted(set(years))
        if len(years) > 1:
            new_label = f"{base_label}_{years[0]}-{years[-1]}"
        else:
            new_label = f"{base_label}_{years[0]}"
        merged_labels.append(new_label)

    return merged_labels, other_labels

# Function to write the new classes file
def write_new_classes_file(merged_labels, other_labels, output_file_path):
    with open(output_file_path, 'w') as file:
        # Write the merged labels first
        for label in merged_labels:
            file.write(f"{label}\n")
        
        # Write the other labels that didn't need merging
        for label in other_labels:
            file.write(f"{label}\n")

# Main function to run the script
def main():
    classes_file = 'ZImages/classes.txt'  # Input file path
    new_classes_file = 'new_classes.txt'  # Output file path

    # Load and clean classes
    merged_labels, other_labels = load_and_clean_classes(classes_file)

    # Write the new classes file
    write_new_classes_file(merged_labels, other_labels, new_classes_file)
    print(f"New classes file saved at: {new_classes_file}")

if __name__ == "__main__":
    main()
