from ultralytics import YOLO
import torch
from pathlib import Path

script_dir = Path(__file__).resolve().parent
model = YOLO(script_dir / 'damagedetection.pt')

# Penalty rates for damage types
penalty_rates = {
    "dent": 0.008,   
    "scratch": 0.005,
    "crack": 0.025   
}

def process_images(images):
    class_counts = {
        "dent": 0,
        "scratch": 0,
        "crack": 0
    }
    
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    
    for image in images:
        # print(f"Processing image: {image.name}")
        results = model.predict(source=image, task="segment", save=False, device=device, conf=0.4)
        
        if results[0].boxes is not None:  # Check if detections exist
            for idx in results[0].boxes.cls:
                class_name = model.names[int(idx.item())]
                if class_name in class_counts:
                    class_counts[class_name] += 1
        # else:
        #     print(f"No detections found for image: {image.name}")
    
    return class_counts


def calculate_penalty(class_counts):
    total_penalty = 0
    
    for class_name, count in class_counts.items():
        if class_name in penalty_rates:
            total_penalty += penalty_rates[class_name] * count
            
    # Ensure penalty factor is between 0.5 and 1.0
    return max(0.5, 1 - total_penalty)


def pipeline(images):
    damage_counts = process_images(images)
    penalty_factor = calculate_penalty(damage_counts)
    return damage_counts, penalty_factor


# Main script
# imgs = script_dir / 'Test'
# image_files = list(imgs.glob("*.jpg"))

# if not image_files:
#     print("No image files found in the 'Test' directory.")
# else:
#     damage_counts, penalty_factor = pipeline(image_files)
    
#     print("\nFinal Results:")
#     print(f"Damage Counts: {damage_counts}")
#     print(f"Penalty Factor: {penalty_factor:.2f}")
