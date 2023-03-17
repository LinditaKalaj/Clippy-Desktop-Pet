import sys
from PyQt6.QtWidgets import QWidget, QApplication, QMenu, QSystemTrayIcon
from PyQt6.QtGui import QIcon, QAction
from clippy import Clippy


class ClippyInit(QWidget):
    def __init__(self):
        super(ClippyInit, self).__init__()
        self.quit_clippy = None
        self.tray_icon_menu = None
        self.tray_icon = None
        self.clippy = None
        self.setup_tray_icon()

    # Sets up and shows the desktop-pets tray
    def setup_tray_icon(self):
        # Quit option on menu
        self.quit_clippy = QAction("Quit", self,
                                   triggered=QApplication.instance().quit)
        self.quit_clippy.setIcon(QIcon("img/exit_icon.png"))
        self.tray_icon_menu = QMenu(self)
        self.tray_icon_menu.addAction(self.quit_clippy)

        # Tray
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon("img/task_icon.png"))
        self.tray_icon.setContextMenu(self.tray_icon_menu)
        self.tray_icon.show()

        # Creates clippy
        self.clippy = Clippy()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    clippyApp = ClippyInit()
    sys.exit(app.exec())
