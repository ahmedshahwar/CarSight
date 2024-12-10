import os
import matplotlib.pyplot as plt
from collections import Counter

# Path to your images and labels folder
labels_folder = 'images_labels'

# Initialize a Counter to count class occurrences
class_count = Counter()

# Loop through all label files in the folder
for label_file in os.listdir(labels_folder):
    if label_file.endswith('.txt') and label_file != 'classes.txt':
        with open(os.path.join(labels_folder, label_file), 'r') as f:
            # Read each line (each label entry)
            for line in f:
                class_id = int(line.split()[0])  # YOLO format: class_id x_center y_center width height
                class_count[class_id] += 1

# Prepare data for plotting
class_ids = list(class_count.keys())
class_occurrences = list(class_count.values())

# Adjust the figure size based on the number of classes
plt.figure(figsize=(15, 6))  # Increase width for better readability (20 inches width)

# Plot the data using class numbers
bars = plt.bar(class_ids, class_occurrences, color='skyblue')
plt.xlabel('Class Number')
plt.ylabel('Number of Occurrences')
plt.title('Class Occurrences in YOLO Labels')

# Rotate x-axis labels for better visibility
plt.xticks(class_ids, rotation=90)  # Rotate the labels for 120 classes

# Add class occurrences as annotations on top of each bar
for bar, count in zip(bars, class_occurrences):
    plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(),
             str(count), ha='center', va='bottom', rotation=90)

plt.tight_layout()

# Save or show the plot
plt.savefig('class_occurrences_with_counts.png')  # Save as an image
plt.show()  # Or display the plot
