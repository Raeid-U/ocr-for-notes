import pytesseract
from PIL import Image
import os
import datetime

# folder paths
images_folder = 'imgs'
output_file = 'output.md'

def ocr_image(image_path):
    with Image.open(image_path) as img:
        # both English and Arabic
        text = pytesseract.image_to_string(img, lang='eng+ara')
    return text

def get_image_files_sorted_by_date(folder_path):
    image_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.lower().endswith(('png', 'jpg', 'jpeg', 'tiff', 'bmp', 'gif'))]
    image_files.sort(key=lambda x: os.path.getctime(x))
    return image_files

def process_images_to_single_file(images_folder, output_file):
    image_files = get_image_files_sorted_by_date(images_folder)
    with open(output_file, 'w') as output:
        for image_file in image_files:
            text = ocr_image(image_file)
            note_title = os.path.splitext(os.path.basename(image_file))[0]
            creation_date = datetime.datetime.fromtimestamp(os.path.getctime(image_file)).strftime('%Y-%m-%d')
            
            output.write(f"# {note_title}\n")
            output.write(f"*Date: {creation_date}*\n\n")
            output.write(f"{text}\n\n")
            output.write("---\n\n")

# output markdown file
process_images_to_single_file(images_folder, output_file)

print(f"Combined notes saved to: {output_file}")
