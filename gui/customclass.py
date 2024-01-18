from PyQt5.QtWidgets import *
from PyQt5.QtCore import QThread, pyqtSignal, Qt, QPoint

class clickablelabel(QLabel):
    mouseOver = pyqtSignal(int,int)
    mousePress = pyqtSignal(int,int,int,int)
    mouseRelease  = pyqtSignal(int,int,int,int)
    def __init__(self, args):
        super(clickablelabel,self).__init__(args)
        self.setMouseTracking(True)

    def mouseMoveEvent(self,event):
        x= event.pos().x()
        y= event.pos().y()
        self.mouseOver.emit(x,y)

    def mousePressEvent(self,event):
        x = event.pos().x()
        y = event.pos().y()
        button = event.button()
        self.mousePress.emit(x,y,button,1)

    def mouseReleaseEvent(self,event):
        x = event.pos().x()
        y = event.pos().y()
        button = event.button()
        self.mouseRelease.emit(x,y,button,2)