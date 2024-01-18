import cv2
import json
# from frameEditor import *

class Playback:
    
    def __init__(self,path) -> None:
        #initialize our capture object
        self.Stream = cv2.VideoCapture(path)
        # self.FrameEdit = FrameEditor(path)

    def set(self,frameNo):
        #When the read command is called the required frame is read
        #Index is in the range of 0-No of Frames
        self.Stream.set(cv2.CAP_PROP_POS_FRAMES,frameNo-1)
    
    def get(self):
        #return the index of the current frame. One based Index
        return self.Stream.get(cv2.CAP_PROP_POS_FRAMES)
    
    def processFrame(self,frame,frameNo):
        temp_dict = self.main_dict[str(frameNo)]
        values = list(temp_dict.values())
        pass

    def read(self):
        #Capture the frame and return it along with the boolean value
        ret,frame = self.Stream.read()
        #Convert from BGR to RGB
        frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        #Return rectified frame
        return ret,frame