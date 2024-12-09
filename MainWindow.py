from PyQt6.QtCore import pyqtSlot
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QMainWindow, QMenu, QMenuBar, QFileDialog

from CentralWidget import CentralWidget


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        central_widget = CentralWidget(self)

        self.setWindowTitle("Mein Texteditor")

        menuBar = QMenuBar(self)

        files = QMenu("Files", menuBar)
        action_file_open = files.addAction("Open ...")
        action_file_open.triggered.connect(self.file_open)
        action_file_save = files.addAction("Save ...")
        action_file_copy = files.addAction("Copy ...")
        action_file_move = files.addAction("Move ...")

        menuBar.addMenu(files)

        self.setMenuBar(menuBar)

        self.setCentralWidget(central_widget)

    @pyqtSlot()
    def file_open(self):
        (path, filter) = QFileDialog.getOpenFileName(self, "Open File", "./", "Text files (*.txt);;All files (*)")

        print(path)
        print(filter)

        if path:
            pass
