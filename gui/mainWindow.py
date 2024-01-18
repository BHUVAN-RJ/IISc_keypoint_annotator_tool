import sys
import cv2
import time
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5 import QtWidgets
from PyQt5.uic import loadUi
from customclass import clickablelabel
import os
from playback import Playback


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("mainWindow.ui", self)

        self.CVWorker = CVWorker("test.mp4")
        self.pauseBtn.clicked.connect(self.pauseFeed)
        self.playBtn.clicked.connect(self.resumeFeed)
        self.forwardBtn.clicked.connect(self.forwardFeed)
        self.rewindBtn.clicked.connect(self.rewindFeed)
        self.saveBtn.clicked.connect(self.saveFrame)  # Connect Save button to saveFrame method

        self.CVWorker.start()
        self.CVWorker.ImageUpdate.connect(self.ImageUpdateSlot)
        self.CVWorker.AngleUpdate.connect(self.AngleUpdateSlot)

    def ImageUpdateSlot(self, Image):
        self.label.setPixmap(QPixmap.fromImage(Image))

    def AngleUpdateSlot(self, frameNo):
        self.angle1.setText(str(frameNo))

    def rewindFeed(self):
        self.CVWorker.rewind()

    def forwardFeed(self):
        self.CVWorker.forward()

    def pauseFeed(self):
        self.CVWorker.pause()

    def resumeFeed(self):
        self.CVWorker.resume()

    def saveFrame(self):
        current_frame = self.CVWorker.frameNo
        ret, frame = self.CVWorker.Capture.read()
        if ret:
            # Ensure the "frames" directory exists, create it if not
            frames_folder = "frames"
            if not os.path.exists(frames_folder):
                os.makedirs(frames_folder)

            # Resize the frame to 256x256
            resized_frame = cv2.resize(frame, (256, 256))

            filename = f"{frames_folder}/frame_{current_frame}.jpg"
            cv2.imwrite(filename, resized_frame)
            print(f"Frame {current_frame} saved as {filename}")


class CVWorker(QThread):
    ImageUpdate = pyqtSignal(QImage)
    AngleUpdate = pyqtSignal(float)

    def __init__(self, path):
        super(CVWorker, self).__init__()
        self.frameNo = 1
        self.pauseFlag = False
        self.rewindFlag = False
        self.forwardFlag = False
        self.Capture = Playback(path)

    def toQtFormat(self, Image):
        ConvertToQtFormat = QImage(Image.data, Image.shape[1], Image.shape[0], QImage.Format_RGB888)
        return ConvertToQtFormat.scaled(740, 480, Qt.KeepAspectRatio)

    def displayFrame(self, frameNo):
        self.Capture.set(frameNo)
        ret, frame = self.Capture.read()
        if ret:
            Pic = self.toQtFormat(frame)
            self.ImageUpdate.emit(Pic)
            self.frameNo = self.Capture.get()

    def rewind(self):
        if self.pauseFlag:
            self.rewindFlag = True

    def forward(self):
        if self.pauseFlag:
            self.forwardFlag = True

    def pause(self):
        self.pauseFlag = True

    def resume(self):
        self.pauseFlag = False

    def run(self):
        while True:
            if self.pauseFlag:
                if self.rewindFlag:
                    self.AngleUpdate.emit(self.frameNo - 1)
                    self.displayFrame(self.frameNo - 1)
                    self.rewindFlag = False
                    continue
                if self.forwardFlag:
                    self.displayFrame(self.frameNo + 1)
                    self.forwardFlag = False
                    continue
                else:
                    continue
            if not self.pauseFlag:
                ret, frame = self.Capture.read()
                time.sleep(0.033)
                if ret:
                    Pic = self.toQtFormat(frame)
                    self.ImageUpdate.emit(Pic)
                    self.frameNo = self.Capture.get()
                    self.AngleUpdate.emit(self.frameNo)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
