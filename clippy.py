from random import randint
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt, QTimer
from PyQt5 import QtGui, QtCore
from clippyChat import ClippyChat


class Clippy(QWidget):
    def __init__(self):
        super(Clippy, self).__init__()
        self.img = None
        self.ask = None
        self.idle = None
        self.idle_to_sleeping = None
        self.sleeping = None
        self.sleeping_to_idle = None
        self.thinking = None
        self.talk = None
        self.frame = None
        self.m_DragPosition = None
        self.m_drag = None

        self.get_animations()
        self.state = 0
        self.i_frame = 0
        self.event_number = randint(1, 3)
        self.init_ui()

    def init_ui(self):
        # Remove window bar and make Clippy stay on top of windows and have translucent background
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setAutoFillBackground(True)

        # label to display image
        self.img = QLabel(self)
        transparent_img = QImage()
        transparent_img.load('img/tp.png')
        self.img.setPixmap(QPixmap.fromImage(transparent_img))
        self.resize(128, 128)

        # Initializing Clippy's chat box
        self.ask = ClippyChat()

        # Placing clippy in the bottom right
        self.clippy_pos()
        self.show()

        # Start animation cycle
        QTimer.singleShot(1, self.update)

    # Loads png files into an array as QImages to use for animation
    def load_png(self, images):
        pic_arr = []
        for image in images:
            img = QImage()
            img.load('img/' + image)
            pic_arr.append(img)
        return pic_arr

    # Sends array of files to loadPNGToArr function and saves them in groups of state
    def get_animations(self):
        self.idle = self.load_png(
            ["idle1.png", "idle2.png", "idle3.png", "idle4.png", "idle5.png", "idle6.png", "idle7.png", "idle8.png",
             "idle9.png"])

        self.idle_to_sleeping = self.load_png(
            ["sleeping1.png", "sleeping2.png", "sleeping3.png", "sleeping4.png", "sleeping5.png", "sleeping6.png"])
        self.sleeping = self.load_png(["sleep1.png", "sleep2.png", "sleep3.png", "sleep4.png"])

        self.sleeping_to_idle = self.load_png(
            ["sleeping6.png", "sleeping5.png", "sleeping4.png", "sleeping3.png", "sleeping2.png", "sleeping1.png"])

        self.thinking = self.load_png(["thinking1.png", "thinking2.png", "thinking3.png", "thinking4.png"])

        self.talk = self.load_png(["talk1.png", "talk2.png", "talk3.png", "talk4.png", "talk5.png"])

    # Picks state based on either chat or randomly generated numbers in update
    def set_states(self):
        # Clippy talking
        if self.ask.talking:
            self.state = 0
            self.event_number = 1

        # Clippy thinking
        elif not self.ask.isHidden():
            self.state = 0
            self.event_number = 1

        # Clippy idle
        elif 1 <= self.event_number <= 4:
            self.state = 0

        # Clippy idle to sleep
        elif self.event_number == 5:
            self.state = 1

        # Clippy sleeping
        elif 6 <= self.event_number <= 11:
            self.state = 2

        # Clippy waking up
        elif self.event_number == 12:
            self.state = 3

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

        QTimer.singleShot(1, self.set_states)

    # Function to loop through the images, if loop is done it will generate a number randomly limited on the next
    # state it can have
    def animate(self, array, a, b):
        if self.i_frame < len(array) - 1:
            self.i_frame += 1
        else:
            self.i_frame = 0
            self.event_number = randint(a, b)

    # Sets clippy to the bottom right and the chat box next to him.
    def clippy_pos(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()), (screen.height() - size.height() - 100))
        self.ask.move((screen.width() - size.width() - 310), (screen.height() - size.height() - 250))

    # Overrides functions to allow user to move Clippy
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.m_drag = True
            self.m_DragPosition = event.globalPos() - self.pos()
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))

    # Mouse events to drag Clippy around
    def mouseMoveEvent(self, event):
        if Qt.LeftButton and self.m_drag:
            self.move(event.globalPos() - self.m_DragPosition)
            event.accept()

    def mouseReleaseEvent(self, event):
        self.m_drag = False
        self.setCursor(QCursor(Qt.ArrowCursor))

    # Double click to open chat box
    def mouseDoubleClickEvent(self, a0: QtGui.QMouseEvent) -> None:
        if self.ask.isHidden():
            self.ask.show()
        else:
            self.ask.close()
        return super().mouseDoubleClickEvent(a0)
