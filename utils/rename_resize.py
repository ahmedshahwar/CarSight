import os

def func(main_folder):
    # Walk through the directory
    for root, dirs, files in os.walk(main_folder):
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            images = [f for f in os.listdir(dir_path) if f.endswith('.webp')]
            
            # Rename each image
            for i, image in enumerate(sorted(images), start=1):
                old_path = os.path.join(dir_path, image)
                new_name = f"{dir_name}_{i}.jpeg"
                new_path = os.path.join(dir_path, new_name)
                
                # Rename the image
                os.rename(old_path, new_path)
                
                print(f"Renamed: {old_path} to {new_path}")

# Run the function for the specified folders
# func('BAIC')
# func('Changan')
# func('Chery')
# func('DFSK')
# func('Haval')
# func('Hyundai')
# func('KIA')
# func('MG')
# func('Peugeot')
# func('Prince')
# func('Proton')
# func('United')

# func('Aymen Images/archive/Honda')
# func('Aymen Images/archive/Suzuki')
# func('Aymen Images/archive/Toyota')
func('Aymen Images/archive/odo')
