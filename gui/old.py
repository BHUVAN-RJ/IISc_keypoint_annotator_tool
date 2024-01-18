from PyQt5.uic import loadUi
import sys
import cv2
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5 import QtWidgets

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow,self).__init__()
        loadUi("mainWindow.ui",self)

        self.pauseBtn.clicked.connect(self.pauseFeed)
        self.Worker1 = Worker1()

        self.Worker1.start()
        self.Worker1.ImageUpdate.connect(self.ImageUpdateSlot)
        
    def ImageUpdateSlot(self, Image):
        self.label.setPixmap(QPixmap.fromImage(Image))

    def pauseFeed(self):
        self.Worker1.pause()
        self.pauseBtn.clicked.connect(self.resumeFeed)
    
    def resumeFeed(self):
        self.Worker1.resume()
        self.pauseBtn.clicked.connect(self.pauseFeed)

class Worker1(QThread):

    ImageUpdate = pyqtSignal(QImage)
    frameNo = 100
    def run(self):
        print("RUN CALLED")
        self.ThreadActive = True
        Capture = cv2.VideoCapture("test.mp4")
        Capture.set(cv2.CAP_PROP_POS_FRAMES,self.frameNo)
        while self.ThreadActive:
            ret, frame = Capture.read()
            print("Frame : ", str(Capture.get(cv2.CAP_PROP_POS_FRAMES)))
            if ret:
                Image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                ConvertToQtFormat = QImage(Image.data, Image.shape[1], Image.shape[0], QImage.Format_RGB888)
                Pic = ConvertToQtFormat.scaled(740, 480, Qt.KeepAspectRatio)
                self.ImageUpdate.emit(Pic)
                self.frameNo = Capture.get(cv2.CAP_PROP_POS_FRAMES)

    def pause(self):
        self.ThreadActive = False
    def resume(self):
        self.ThreadActive = True
        print("Resume Called")
        self.start()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())