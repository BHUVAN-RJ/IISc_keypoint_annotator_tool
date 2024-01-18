import cv2

class frameProcessor:

    def __init__(self,path) -> None:
        self.stream = cv2.VideoCapture(path)
    
    def nextFrame(self,frameNo):
        pass
    
    def previousFrame(self,frameNo):
        self.stream.set(cv2.CAP_PROP_POS_FRAMES,frameNo-1)
    
    def set(self,frameNo):
        self.stream.set(cv2.CAP_PROP_POS_FRAMES,frameNo)

    def get(self):
        return self.stream.get(cv2.CAP_PROP_POS_FRAMES)

    def read(self):
        ret, frame = self.stream.read()
        return ret,frame

    def setFlags(self,property,flag):
        pass