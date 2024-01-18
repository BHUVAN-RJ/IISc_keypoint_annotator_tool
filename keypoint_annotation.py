import os
import cv2
import tkinter as tk
from tkinter import Canvas, Button, Label, Toplevel

from ultralytics import YOLO

model = YOLO("/Users/bhuvanrj/Desktop/pose-detection-keypoints-estimation-yolov8-main/Weights/last.pt")

colors = [
    (255, 0, 0), (0, 255, 0), (0, 0, 255),
    (255, 255, 0), (255, 0, 255), (0, 255, 255),
    (128, 0, 0), (0, 128, 0), (0, 0, 128),
    (128, 128, 0), (128, 0, 128), (0, 128, 128),
    (128, 128, 128), (255, 128, 0), (255, 0, 128),
    (0, 255, 128), (128, 255, 0), (0, 128, 255),
    (128, 0, 255), (255, 128, 128), (128, 255, 128),
    (0, 128, 128)
]


parts = [
    "left eye", "right eye", "nose", "left ear", "right ear",
    "left shoulder", "right shoulder", "left elbow", "right elbow",
    "left wrist", "right wrist", "left hip",
    "right hip", "left knee", "right knee", "left ankle", "right ankle",
    "left finger", "right finger", "back", "left toe", "right toe"
]

class KeypointEditor:
    def __init__(self, root, image_path, initial_points):
        initial_points = initial_points[0]
        self.root = root
        self.image_size = 256
        self.image_ac_size = None
        self.image_path = image_path
        self.initial_points = initial_points
        self.final_points = [list(point) for point in initial_points]  # Convert to lists
        self.selected_point = None

        self.scale_factor = 2.5  # Scale factor for both image and points

        self.label = Label(root, text="File Name: {}".format(os.path.basename(image_path)))
        self.label.pack()

        self.message_label = Label(root, text="")
        self.size_label = Label(root, text="")
        self.size_label.pack()

        self.message_label.pack()

        self.canvas = Canvas(root)
        self.canvas.pack()

        self.load_image()
        self.draw_keypoints()

        self.save_button = Button(root, text="Save", command=self.save_coordinates)
        self.save_button.pack()

        self.canvas.bind("<Button-1>", self.select_point)
        self.canvas.bind("<B1-Motion>", self.move_selected_point)

    def load_image(self):
        self.image = cv2.imread(self.image_path)
        image_size = self.image.shape
        self.size_label.config(text=f"Image_ac_size {image_size}")
        # self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        self.image = cv2.resize(self.image, None, fx=self.scale_factor, fy=self.scale_factor)  # Scale up the image
        self.photo = tk.PhotoImage(data=cv2.imencode('.png', self.image)[1].tobytes())
        self.canvas.config(width=self.image.shape[1], height=self.image.shape[0])  # Set canvas size to match image size
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)

    def draw_keypoints(self):
        for i, (x, y) in enumerate(self.final_points):
            x_scaled, y_scaled = x * self.scale_factor, y * self.scale_factor  # Scale up the points
            color = colors[i % len(colors)]
            self.canvas.create_oval(x_scaled - 5, y_scaled - 5, x_scaled + 5, y_scaled + 5,
                                    fill="#%02x%02x%02x" % color, outline="#%02x%02x%02x" % color)

    def select_point(self, event):
        x, y = event.x // self.scale_factor, event.y // self.scale_factor  # Scale down the mouse click coordinates
        for i, (px, py) in enumerate(self.final_points):
            if abs(px - x) < 10 and abs(py - y) < 10:
                self.selected_point = i
                break

    def move_selected_point(self, event):
        if self.selected_point is not None:
            x, y = event.x // self.scale_factor, event.y // self.scale_factor  # Scale down the mouse move coordinates
            self.final_points[self.selected_point] = [int(x), int(y)]  # Convert to integers and update as list
            self.redraw_keypoints()

    def redraw_keypoints(self):
        self.canvas.delete("all")
        self.load_image()
        self.draw_keypoints()

    def save_coordinates(self):
        # Ensure all points in final_points are integers
        self.final_points = [[int(px), int(py)] for px, py in self.final_points]

        # Normalize the points to the original image size
        normalized_points = [(x / self.image_size, y / self.image_size) for x, y in self.final_points]

        # Create a formatted string for saving
        save_string = "0 0.5 0.5 1 1 " + " ".join([f"{x} {y}" for x, y in normalized_points])

        # Create a 'labels' folder if it doesn't exist
        labels_folder = os.path.join(os.path.dirname(self.image_path), "labels")
        os.makedirs(labels_folder, exist_ok=True)

        # Save to a .txt file inside the 'labels' folder
        save_filename = os.path.splitext(os.path.basename(self.image_path))[0] + ".txt"
        save_path = os.path.join(labels_folder, save_filename)

        with open(save_path, "w") as file:
            file.write(save_string)

        # Update the message label
        self.message_label.config(text=f"Saved coordinates to {save_path}")

def display_parts_colors():
    part_colors_window = Toplevel()
    part_colors_window.title("Parts and Colors")

    for i in range(len(parts)):
        color = colors[i % len(colors)]
        part_label = Label(part_colors_window, text=parts[i], fg="#%02x%02x%02x" % color)
        part_label.grid(row=i, column=0, sticky="w")

        color_label = Label(part_colors_window, text="#%02x%02x%02x" % color)
        color_label.grid(row=i, column=1, sticky="e")

def main():
    folder_path = "/Users/bhuvanrj/Desktop/pose-detection-keypoints-estimation-yolov8-main/data/detect/images/train"
    image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

    for image_file in image_files:
        image_path = os.path.join(folder_path, image_file)
        image = cv2.resize(cv2.imread(image_path), (256, 256))
        results = model(image)
        initial_points = results[0].keypoints.xy.tolist()

        root = tk.Tk()
        root.title("Keypoint Editor")
        editor = KeypointEditor(root, image_path, initial_points)
        parts_button = Button(root, text="Display Parts and Colors", command=display_parts_colors)
        parts_button.pack()
        root.mainloop()

if __name__ == "__main__":
    main()
