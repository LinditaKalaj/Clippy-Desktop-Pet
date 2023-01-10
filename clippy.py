import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class TaskBar(QWidget):
    def __init__(self):
        super(TaskBar, self).__init__()
        quit_clippy = QAction("Quit", self, triggered=self.close_program)
        quit_clippy.setIcon(QIcon("img/exit_icon.png"))
        self.trayIconMenu = QMenu(self)
        self.trayIconMenu.addAction(quit_clippy)
        self.trayIcon = QSystemTrayIcon(self)
        self.trayIcon.setIcon(QIcon("img/task_icon.png"))
        self.trayIcon.setContextMenu(self.trayIconMenu)
        self.trayIcon.show()

    def close_program(self):
        sys.exit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    x = TaskBar()
    app.exec_()
