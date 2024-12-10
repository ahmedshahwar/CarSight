import cv2
from ultralytics import YOLO
import re
from collections import defaultdict
import yaml
import torch
import random
import csv
from pathlib import Path

script_dir = Path(__file__).resolve().parent

# Load the model and class names
model = YOLO(str(script_dir/'carsight.pt'))
with open(str(script_dir/'data.yaml'), 'r') as f:
    class_names = yaml.safe_load(f)['names']

# Load the CSV file into memory
csv_file = str(script_dir/'autofil_data.csv')
vehicle_data = []
with open(csv_file, 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        vehicle_data.append(row)


def get_vehicle_info(make, model, variant, year):
    for row in vehicle_data:
        if (row['Make'].lower() == make.lower() and
            row['Model'].lower() == model.lower() and
            row['Variant'].lower() == variant.lower() and
            year in row['Year']):
            return row['Engine-CC'], row['Engine-Type'], row['Transmission']
    return '', '', ''

def post_process(labels):
    makes, models, variants, overalls = [], [], [], []

    for img, predictions in labels.items():
        unique_labels = set(label for _, label in predictions)

        for label in unique_labels:
            if label.endswith("_logo") or label.endswith("_badge"):
                makes.append(label.split('_')[0])
            elif label.endswith("_model"):
                models.append(label.split('_')[0])
            elif label.endswith("_variant"):
                variants.append(label.split('_')[0])
            elif re.search(r'\d{4}-\d{4}', label):  # Year range detection
                overalls.append(label)

    overall_count = defaultdict(int)
    for make in makes:
        for overall in overalls:
            if make in overall:
                overall_count[overall] += 1
    for model in models:
        for overall in overalls:
            if model in overall:
                overall_count[overall] += 1
    for variant in variants:
        for overall in overalls:
            if variant in overall:
                overall_count[overall] += 1

    full_name = max(overall_count, key=overall_count.get) if overall_count else "Dmake_Dmodel_Dvariant_Dyear"
    try:
        m1, m2, v, y = full_name.split("_")
    except ValueError:
        m1, m2, v, y = ("unknown", "unknown", "unknown", "unknown")
    v = v.replace("-", " ") if "-" in v else v

    # # Extract engine capacity (cc) if digits are present in `v`
    # cc = None
    # engine_capacity_match = re.search(r'(\d+\.\d+)', v)
    # if engine_capacity_match:
    #     cc = int(float(engine_capacity_match.group(1)) * 1000)
    # else: 
    #     cc = ''

    # # Determine transmission type
    # v_lower = v.lower()
    # if any(keyword in v_lower for keyword in ['cvt', 'automatic', 'ags', 'prosmatec', 'auto']):
    #     t = 'automatic'
    # elif any(keyword in v_lower for keyword in ['mt', 'manual']):
    #     t = 'manual'
    # else:
    #     if m1 == 'suzuki' or m1 == 'toyota' or m1 == 'honda' or (m1 == 'changan' and m2 == 'karvaan') or m1 == 'prince' or m1 == 'united':
    #         t = 'manual'
    #     else:
    #         t = 'automatic'

    # # Set default values for engine type and registration city
    # type = 'petrol'
    
    # Get engine capacity, engine type, and transmission from the CSV
    cc, type, t = get_vehicle_info(m1, m2, v, y)
    
    # Randomly select a year from the range in `y`
    year_range_match = re.search(r'(\d{4})-(\d{4})', y)
    if year_range_match:
        start_year, end_year = map(int, year_range_match.groups())
        y = str(random.randint(start_year, end_year))
    else:
        y = "unknown"
    
    # Set default values for city and randomly selecting one from this
    city = ['Islamanbad', 'Punjab', 'Lahore', 'Rawalpindi', 'Sindh', 'Karachi', 'Faisalabad', 'Peshawar', 'Quetta', 'Un-Registered']
    reg = random.choice(city)
    
    # Capitalize first letter of each word for make and model
    m1 = m1.title()
    m2 = m2.title()

    # Handle capitalization for variant (v)
    special_cases = ["VXR", "VX", "VXL", "AGS", "HEV", "RS", "GL", "GLS", "AWD", "FWD", 
                    "EX", "PHEV", "DLX", "DX", "GL", "GLX", "CVT"]
    two_letter_cases = ["GLI", "XLI"]

    # Split variant into words and process each word
    words = v.split()
    for i in range(len(words)):
        word_upper = words[i].upper()
        if word_upper in special_cases:
            words[i] = word_upper  # Capitalize all letters
        elif word_upper in two_letter_cases:
            words[i] = word_upper[:2].capitalize() + word_upper[2:].lower()  # Capitalize first two letters
        else:
            words[i] = words[i].title()  # Capitalize first letter of each word

    # Join the processed words back
    v = " ".join(words)

    return m1, m2, v, y, cc, type, t, reg


def pipeline(images):
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    labels = {}

    for img_path in images:
        img = cv2.imread(img_path)
        results = model.predict(img, save=False, conf=0.25, device=device)
        boxes = results[0].boxes.data.cpu().numpy() if len(results[0].boxes) > 0 else []

        img_labels = []
        for box in boxes:
            _, _, _, _, conf, class_id = box
            class_name = class_names[int(class_id)].lower()
            img_labels.append((conf, class_name))
        labels[img_path] = img_labels

    return post_process(labels)

# Code Test
# imgs = [
#     r'Deployment\ImageDetection\Test\img1-1.jpg',
#     r'Deployment\ImageDetection\Test\img1-2.jpg',
#     r'Deployment\ImageDetection\Test\img1-3.jpg',
#     r'Deployment\ImageDetection\Test\img1-4.jpg'
# ]

# make, model, variant, year, cc, t, trans, city = pipeline(imgs)
# # Print the results
# print(f"Make: {make}")
# print(f"Model: {model}")
# print(f"Variant: {variant}")
# print(f"Year: {year}")
# print(f"Engine Capacity: {cc}")
# print(f"Engine Type: {t}")
# print(f"Transmission: {trans}")
# print(f"Registration City: {city}")