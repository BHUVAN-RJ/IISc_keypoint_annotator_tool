from PyQt5.uic import loadUi
import sys
import cv2
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5 import QtWidgets
import time
from frameProcessor import *

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow,self).__init__()
        loadUi("mainWindow.ui",self)

        self.pauseBtn.clicked.connect(self.pauseFeed)
        self.rewindBtn.clicked.connect(self.rewindFeed)
        self.forwardBtn.clicked.connect(self.forwardFeed)
        self.Worker1 = Worker1()

        self.Worker1.start()
        self.angle2.setText("str")
        self.angle3.setText("str")
        self.angle4.setText("str")
        self.angle5.setText("str")
        self.angle6.setText("str")
        self.angle7.setText("str")
        self.angle8.setText("str")

    def pauseFeed(self):
        self.Worker1.pause()
        self.pauseBtn.clicked.connect(self.resumeFeed)
    
    def resumeFeed(self):
        self.Worker1.resume()
        self.pauseBtn.clicked.connect(self.pauseFeed)
    
    def rewindFeed(self):
        self.Worker1.rewind()
    
    def forwardFeed(self):
        self.Worker1.forward()

class Worker1(QThread):

    #Constantly update the new frame that was processed
    ImageUpdate = pyqtSignal(QImage)
    AngleUpdate = pyqtSignal(str)
    frameNo = 0
    Cap = frameProcessor("/Users/bhuvanrj/Desktop/Video_Tool_IISc-main/gui/test.mp4")
    pauseFlag = False

    def reFormat(self,frame):
        Image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        ConvertToQtFormat = QImage(Image.data, Image.shape[1], Image.shape[0], QImage.Format_RGB888)
        return ConvertToQtFormat.scaled(740, 480, Qt.KeepAspectRatio)
                

    def run(self):
        print(self.frameNo)
        #Allow the thread to run
        self.ThreadActive = True
        
        #Replace the capture function with my own custom capture class
        #Set the capture position based on the frame number
        self.Cap.set(self.frameNo)
        # cv2.waitKey(-1)
        
        while not self.pauseFlag:
            ret, frame = self.Cap.read()
            # print("Frame : ", str(Cap.get(cv2.CAP_PROP_POS_FRAMES))) #*Debug
            # time.sleep(0.025) #! Not the best way to adjust frame rate
            if ret:
                Pic = self.reFormat(frame)
                self.ImageUpdate.emit(Pic)
                self.AngleUpdate.emit(str(self.frameNo))
                self.frameNo = self.Cap.get()
            else:
                self.Cap.set(0)
                pass
        if self.pauseFlag:
            ret,frame = self.Cap.read()
            if ret:
                PausedPic = self.reFormat(frame)
                self.ImageUpdate.emit(PausedPic)
                self.AngleUpdate.emit(str(self.frameNo))
                self.frameNo = self.Cap.get() - 1
            else:
                pass

    def forward(self):
        print("Pressed Forward")

    def rewind(self):
        print("Presed Backward")
        # if self.ThreadActive == False:
        if self.pauseFlag == True:
            self.Cap.previousFrame(self.frameNo)
            self.pauseFlag = True
            self.frameNo = self.Cap.get()
            self.start()

    def pause(self):
        self.pauseFlag = True
        self.ThreadActive = False
    def resume(self):
        self.pauseFlag = False
        self.ThreadActive = True
        self.start()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())