import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class ClippyInit(QWidget):
    def __init__(self):
        super(ClippyInit, self).__init__()
        self.setUpTrayIcon()

    # Sets up and shows the desktop-pets tray
    def setUpTrayIcon(self):
        # Quit option on menu
        self.quit_clippy = QAction("Quit", self,
                                   triggered=QApplication.instance().quit)
        self.quit_clippy.setIcon(QIcon("img/exit_icon.png"))
        self.trayIconMenu = QMenu(self)
        self.trayIconMenu.addAction(self.quit_clippy)
        # Tray
        self.trayIcon = QSystemTrayIcon(self)
        self.trayIcon.setIcon(QIcon("img/task_icon.png"))
        self.trayIcon.setContextMenu(self.trayIconMenu)
        self.trayIcon.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    clippy = ClippyInit()
    sys.exit(app.exec_())
