from random import randint, random

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt, QTimer, QThread, QRunnable, QThreadPool
from PyQt5 import QtGui, QtCore

from clippyChat import ClippyChat


class Clippy(QWidget):
    def __init__(self):
        super(Clippy, self).__init__()
        self.getAnimations()
        self.state = 0
        self.i_frame = 0
        self.event_number = randint(1, 3)
        self.initUI()

    def initUI(self):
        # Remove window bar and make Clippy stay on top of windows and have translucent background
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setAutoFillBackground(True)
        # label to display image
        self.img = QLabel(self)
        transparentImg = QImage()
        transparentImg.load('img/tp.png')
        self.img.setPixmap(QPixmap.fromImage(transparentImg))
        self.resize(128, 128)
        # Initializing clippy's chat box
        self.ask = ClippyChat()
        # Placing clippy in the bottom right
        self.clippyPos()
        self.show()

        #Start animation cycle
        QTimer.singleShot(1, self.update)

    # Loads png files into an array as QImages to use for animation
    def loadPNGToArr(self, imgs):
        picArr = []
        for file in imgs:
            img = QImage()
            img.load('img/' + file)
            picArr.append(img)
        return picArr

    # Sends array of files to loadPNGToArr function and saves them in groups of state
    def getAnimations(self):
        self.idle = self.loadPNGToArr(
            ["idle1.png", "idle2.png", "idle3.png", "idle4.png", "idle5.png", "idle6.png", "idle7.png", "idle8.png",
             "idle9.png"])
        self.idle_to_sleeping = self.loadPNGToArr(
            ["sleeping1.png", "sleeping2.png", "sleeping3.png", "sleeping4.png", "sleeping5.png", "sleeping6.png"])
        self.sleeping = self.loadPNGToArr(["sleep1.png", "sleep2.png", "sleep3.png", "sleep4.png"])
        self.sleeping_to_idle = self.loadPNGToArr(
            ["sleeping6.png", "sleeping5.png", "sleeping4.png", "sleeping3.png", "sleeping2.png", "sleeping1.png"])
        self.thinking = self.loadPNGToArr(["thinking1.png", "thinking2.png", "thinking3.png", "thinking4.png"])
        self.talk = self.loadPNGToArr(["talk1.png", "talk2.png", "talk3.png", "talk4.png", "talk5.png"])

    # Picks state based on either chat or randomly generated numbers in update
    def setStates(self):
        if self.ask.talking:
            self.state = 0
            self.event_number = 1
            print('talking')
        elif not self.ask.isHidden():
            self.state = 0
            self.event_number = 1
            print("thinking")
        elif  1 <= self.event_number <= 4:
            self.state = 0
            print('idle')
        elif self.event_number == 5:
            self.state = 1
            print('idle to sleep')
        elif 6 <= self.event_number <= 11:
            self.state = 2
            print('sleep')
        elif self.event_number == 12:
            self.state = 3
            print('from sleep to idle')

        QTimer.singleShot(400, self.update)

    # Grabs image based on either Chat visibility or state
    def update(self):
        if self.ask.talking:
            if self.i_frame >= len(self.talk):
                self.i_frame = 0
            self.frame = self.talk[self.i_frame]
            self.animate(self.talk, 19, 24)

        elif not self.ask.isHidden():
            if self.i_frame >= len(self.thinking):
                self.i_frame = 0
            self.frame = self.thinking[self.i_frame]
            self.animate(self.thinking, 13, 16)

        elif self.state == 0:
            self.frame = self.idle[self.i_frame]
            self.animate(self.idle, 1, 5)

        elif self.state == 1:
            self.frame = self.idle_to_sleeping[self.i_frame]
            self.animate(self.idle_to_sleeping, 6, 6)

        elif self.state == 2:
            self.frame = self.sleeping[self.i_frame]
            self.animate(self.sleeping, 6, 12)

        elif self.state == 3:
            self.frame = self.sleeping_to_idle[self.i_frame]
            self.animate(self.sleeping_to_idle, 1, 1)

        self.img.setPixmap(QPixmap.fromImage(self.frame))


        QTimer.singleShot(1, self.setStates)

    #function to loop through the images, if loop is done it will generate a number randomly limited on the next state it can have
    def animate(self, array, a, b):
        if self.i_frame < len(array) - 1:
            self.i_frame += 1
        else:
            self.i_frame = 0
            self.event_number = randint(a, b)

    # Sets clippy to the bottom right and the chatbox next to him.
    def clippyPos(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        print((screen.width() - size.width()), (screen.height() - size.height()))
        self.move((screen.width() - size.width()), (screen.height() - size.height() - 100))
        self.ask.move((screen.width() - size.width() - 310), (screen.height() - size.height() - 250))

    # Overrides functions to allow user to move Clippy
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.m_drag = True
            self.m_DragPosition = event.globalPos() - self.pos()
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))

    def mouseMoveEvent(self, QMouseEvent):
        if Qt.LeftButton and self.m_drag:
            self.move(QMouseEvent.globalPos() - self.m_DragPosition)
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_drag = False
        self.setCursor(QCursor(Qt.ArrowCursor))

    # Double click to open chatbox
    def mouseDoubleClickEvent(self, a0: QtGui.QMouseEvent) -> None:
        print("double click")
        if self.ask.isHidden():
            self.ask.show()
        else:
            self.ask.close()
        return super().mouseDoubleClickEvent(a0)
