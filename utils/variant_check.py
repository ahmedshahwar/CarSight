# import os
# from collections import defaultdict

# # Directory containing the images
# image_dir = 'AImages'

# # Dictionary to store model and its variants
# model_variants_count = defaultdict(lambda: defaultdict(int))

# # Iterate over all images in the directory
# for filename in os.listdir(image_dir):
#     if filename.endswith('.jpeg') or filename.endswith('.jpg') or filename.endswith('.png'):
#         # Split the filename into parts based on underscores and periods
#         parts = filename.split('_')
        
#         # Extract the model and variant
#         make = parts[0]
#         model = parts[1]
#         year = parts[-2]  # Year is the second last part
#         variant = '_'.join(parts[2:-2])  # Join all parts between model and year as the variant
        
#         # Add to dictionary
#         model_variants_count[f"{make}_{model}"][variant] += 1

# # Print the result
# for model, variants in model_variants_count.items():
#     print(f"Model: {model}")
#     for variant, count in variants.items():
#         print(f"  Variant: {variant} - Number of images: {count}")


#--------------------------------------------------------------#
#          -------------------------------------------         #
#--------------------------------------------------------------#

import os
import random
import shutil
from collections import defaultdict

# Directory containing the images
image_dir = 'AImages'
output_dir = 'hst'

# Create the output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Dictionary to store categorized models, variants, and their year ranges
categorized_data = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))

# Year ranges for specific models
year_ranges = {
    'honda_br-v': [(2017, 2023)],
    'honda_civic': [(2013, 2015), (2016, 2021), (2022, 2023)],
    'honda_city': [(2013, 2020), (2021, 2023)],
    'honda_hr-v': [(2022, 2023)],
    'suzuki_alto': [(2013, 2023)],
    'suzuki_bolan': [(2013, 2023)],
    'suzuki_cultus': [(2013, 2016), (2017, 2023)],
    'suzuki_mehran': [(2013, 2019)],
    'suzuki_swift': [(2013, 2021), (2022, 2023)],
    'suzuki_wagon': [(2017, 2023)],
    'toyota_corolla': [(2013, 2014), (2015, 2023)],
    'toyota_fortuner': [(2017, 2023)],
    'toyota_hilux': [(2015, 2023)],
    'toyota_yaris': [(2020, 2023)],
}

# Iterate over all images in the directory
for filename in os.listdir(image_dir):
    if filename.endswith(('.jpeg', '.jpg', '.png')):        
        parts = filename.lower().split('_')
        try:
            make = parts[0]
            model = parts[1]
            year = int(parts[-2])  # Year is the second last part
            variant = '_'.join(parts[2:-2])  # Join all parts between model and year as the variant

            if variant == '':
                continue

            model_name = f"{make}_{model}"

            if model_name in year_ranges:
                for start_year, end_year in year_ranges[model_name]:
                    if start_year <= year <= end_year:
                        year_range_key = f"{start_year}-{end_year}"
                        categorized_data[model_name][year_range_key][variant].append(filename)
        except ValueError as e:
            print(f"Error parsing year for file {filename}: {e}")

fixed_number = 120  # Total number of images needed per year range

for model, year_dict in categorized_data.items():
    model_dir = os.path.join(output_dir, model)
    os.makedirs(model_dir, exist_ok=True)

    for year_range, variants in year_dict.items():
        year_range_dir = os.path.join(model_dir, year_range)
        os.makedirs(year_range_dir, exist_ok=True)

        total_variants = len(variants)
        if total_variants == 0:
            continue

        images_per_variant = fixed_number // total_variants
        print(f"Model: {model} ({year_range}) - Total Variants: {total_variants}")

        for variant, files in variants.items():
            print(f"  Variant: {variant} - Number of images: {len(files)}")
            num_images_needed = images_per_variant - len(files)

            if len(files) >= images_per_variant:
                selected_files = random.sample(files, images_per_variant)
                for file in selected_files:
                    shutil.copy(os.path.join(image_dir, file), os.path.join(year_range_dir, file))
            else:
                for file in files:
                    shutil.copy(os.path.join(image_dir, file), os.path.join(year_range_dir, file))

                # Copy and rename only the needed number of images
                for i in range(num_images_needed):
                    file = files[i % len(files)]
                    base_name, ext = os.path.splitext(file)
                    new_filename = f"{base_name}_copy{i}{ext}"
                    shutil.copy(os.path.join(image_dir, file), os.path.join(year_range_dir, new_filename))

print("\nSummary:")
total_images_in_hst = sum([len(files) for _, _, files in os.walk(output_dir)])
wanted_number = 0
for model_name, year_ranges_list in year_ranges.items():
    wanted_number += 120 * len(year_ranges_list)

print(f"Total images in the 'hst' folder: {total_images_in_hst}")
print(f"Expected number of images (wanted_number): {wanted_number}")
print(f"Difference: {wanted_number - total_images_in_hst if total_images_in_hst < wanted_number else 0}")

