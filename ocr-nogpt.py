import requests
import os
import datetime

# Folder paths
images_folder = 'imgs'
output_file = 'output.md'
api_key = 'K82952330088957'  # Replace with your OCR.space API key

def get_image_files_sorted_by_date(folder_path):
    image_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.lower().endswith(('png', 'jpg', 'jpeg', 'tiff', 'bmp', 'gif'))]
    image_files.sort(key=lambda x: os.path.getctime(x))
    return image_files

def ocr_space_api(image_path, api_key):
    url = 'https://api.ocr.space/parse/image'
    with open(image_path, 'rb') as image_file:
        response = requests.post(url,
                                 files={image_path: image_file},
                                 data={'apikey': api_key,
                                       'language': 'eng,ara'})  # OCR.space supports multiple languages
    result = response.json()
    if result['IsErroredOnProcessing']:
        print(f"Error processing {image_path}: {result['ErrorMessage']}")
        return ""
    return result['ParsedResults'][0]['ParsedText']

def process_images_to_single_file(images_folder, output_file, api_key):
    image_files = get_image_files_sorted_by_date(images_folder)
    with open(output_file, 'w') as output:
        for image_file in image_files:
            text = ocr_space_api(image_file, api_key)
            note_title = os.path.splitext(os.path.basename(image_file))[0]
            creation_date = datetime.datetime.fromtimestamp(os.path.getctime(image_file)).strftime('%Y-%m-%d')
            
            output.write(f"# {note_title}\n")
            output.write(f"*Date: {creation_date}*\n\n")
            output.write(f"{text}\n\n")
            output.write("---\n\n")

# Output markdown file
process_images_to_single_file(images_folder, output_file, api_key)

print(f"Combined notes saved to: {output_file}")
