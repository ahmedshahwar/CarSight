import os
import shutil

def func(main_folder):
    # Create a new folder called 'AImages'
    output_folder = 'AImages'
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Walk through the directory
    for root, dirs, files in os.walk(main_folder):
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            images = [f for f in os.listdir(dir_path) if f.endswith('.jpeg')]  # Find only the renamed .jpeg images
            
            # Copy each image to 'ZImages' folder
            for image in sorted(images):
                image_path = os.path.join(dir_path, image)
                shutil.copy(image_path, os.path.join(output_folder, image))
                print(f"Copied: {image_path} to {output_folder}")

# Specify the main folder where subfolders are located
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

func('Aymen Images/archive/honda')
func('Aymen Images/archive/Suzuki')
func('Aymen Images/archive/Toyota')
# func('Aymen Images/archive/odometer')

