import pytesseract
from PIL import Image
import cv2
import numpy as np
import os
import datetime

# Folder paths
images_folder = 'imgs'
output_file = 'output.md'

def preprocess_image(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    gray = cv2.GaussianBlur(gray, (5, 5), 0)

    binary_image = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

    scale_percent = 150
    width = int(binary_image.shape[1] * scale_percent / 100)
    height = int(binary_image.shape[0] * scale_percent / 100)
    dim = (width, height)
    resized = cv2.resize(binary_image, dim, interpolation=cv2.INTER_LINEAR)
    
    return resized

def get_image_files_sorted_by_date(folder_path):
    image_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.lower().endswith(('png', 'jpg', 'jpeg', 'tiff', 'bmp', 'gif'))]
    image_files.sort(key=lambda x: os.path.getctime(x))
    return image_files

def process_images_to_single_file(images_folder, output_file):
    image_files = get_image_files_sorted_by_date(images_folder)
    with open(output_file, 'w') as output:
        for image_file in image_files:
            preprocessed_image = preprocess_image(image_file)
            custom_config = r'--oem 3 --psm 6'  # Configuration for Tesseract
            text = pytesseract.image_to_string(preprocessed_image, lang='eng+ara', config=custom_config)
            note_title = os.path.splitext(os.path.basename(image_file))[0]
            creation_date = datetime.datetime.fromtimestamp(os.path.getctime(image_file)).strftime('%Y-%m-%d')
            
            output.write(f"# {note_title}\n")
            output.write(f"*Date: {creation_date}*\n\n")
            output.write(f"{text}\n\n")
            output.write("---\n\n")

# Output markdown file
process_images_to_single_file(images_folder, output_file)

print(f"Combined notes saved to: {output_file}")
