import os
import requests
import zipfile
import torch
from pathlib import Path
import shutil

# Download and extract the zipped file
def download_and_extract(url, extract_to='.'):
    zip_file_path = os.path.join(extract_to, 'images.zip')
    response = requests.get(url, stream=True)
    with open(zip_file_path, 'wb') as f:
        f.write(response.content)
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    os.remove(zip_file_path)

# Fine-tune the YOLO model
def fine_tune_yolo_model(image_dir, person_name, output_dir='output'):
    # Load a pre-trained YOLO model
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)  # yolov5s.pt is the small model

    # Fine-tune on the new images
    model.train(data=image_dir, epochs=5)  # Adjust epochs and training params as necessary

    # Save the fine-tuned model
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    model_path = os.path.join(output_dir, f'{person_name}_model.pt')
    model.save(model_path)

    print(f'Model saved as {model_path}')
    return model_path

# Detect objects and faces using the fine-tuned model
def detect_faces_and_objects(model_path, image_dir):
    model = torch.load(model_path)  # Load the fine-tuned model

    # Perform detection on test images
    results = model(image_dir)
    results.print()  # Print the results (can be customized)

    # Optionally save the results to a file
    results.save()

# Main function to orchestrate the task
def main(url, person_name):
    extract_dir = r'C:\\Users\\vigne\\OneDrive\\Desktop\\app-assessment'
    download_and_extract(url, extract_dir)

    # Fine-tune the YOLO model
    model_path = fine_tune_yolo_model(extract_dir, person_name)

    # Detect objects and faces using the fine-tuned model
    detect_faces_and_objects(model_path, extract_dir)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python app.py <url> <person_name>")
    else:
        url = sys.argv[1]
        person_name = sys.argv[2]
        main(url, person_name)
