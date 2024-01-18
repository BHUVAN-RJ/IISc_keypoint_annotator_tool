# keypoint_annotator_tool
This is a tool to create datasets from videos for training YOLOv8-pose on custom dataset
#Steps to run:
1. select the video to capture frames from and run the mainWindow.py, using this script you can select and save needed frames.
2. Run rename_files.py to rename the files to your needs.
3. Run keypoint_annotation.py.
   3.1. Select the weights from the weights folder to load the YOLO model.
   3.2. Select the frames folder, correct the initial annotation, and hit save you will get .txt(label file) for that frame.
4. Run bbox_detection.py, this will detect the person in the frame and update the coordinates of bbox in the initial label files. 
