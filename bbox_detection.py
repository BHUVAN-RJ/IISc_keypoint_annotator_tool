import os
from ultralytics import YOLO

# Initialize YOLO model
model = YOLO("yolov8l.pt")

# Set paths for images and labels folders
images_folder = "/Users/bhuvanrj/Desktop/pose-detection-keypoints-estimation-yolov8-main/data/detect/images/val"
labels_folder = "/Users/bhuvanrj/Desktop/pose-detection-keypoints-estimation-yolov8-main/data/detect/labels/val"

# Iterate through image files
for image_file in os.listdir(images_folder):
    if image_file.endswith(".jpg") or image_file.endswith(".png"):
        # Image file path
        image_path = os.path.join(images_folder, image_file)

        # Run YOLO model on the image
        results = model(image_path, show=False)

        # Check if there is exactly one detection named 'person'
        if len(results[0]) == 1 and results[0].names[0] == 'person':
            # Extract normalized bounding box coordinates
            det = results[0].boxes.xywh[0].tolist()
            normalized_values = [value / 256 for value in det]
            x, y, width, height = normalized_values

            # Label file path
            label_file = os.path.join(labels_folder, image_file.replace(".jpg", ".txt").replace(".png", ".txt"))

            # Read and update label file
            with open(label_file, 'r') as file:
                lines = file.readlines()

            # Update the values in the label file
            for i in range(len(lines)):
                elements = lines[i].strip().split()
                elements[1] = format(float(x), '.7f')
                elements[2] = format(float(y), '.7f')
                elements[3] = format(float(width), '.7f')
                elements[4] = format(float(height), '.7f')
                lines[i] = " ".join(elements)

            # Write back the updated content to the label file
            with open(label_file, 'w') as file:
                file.writelines(lines)

            print(f"Label file {label_file} updated successfully.")
        else:
            print(f"No or multiple 'person' detections in {image_file}. Skipping update.")

print("All label files processed.")
