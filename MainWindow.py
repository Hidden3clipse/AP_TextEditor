from PyQt6.QtCore import pyqtSlot
from PyQt6.QtWidgets import QMainWindow, QMenu, QMenuBar, QFileDialog, QFontDialog, QStatusBar

from CentralWidget import CentralWidget


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.__initial_filter = "Default files (*.txt)"
        self.__filter = self.__initial_filter + ";;All files (*)"

        self.__directory = ""

        central_widget = CentralWidget(self)

        self.setWindowTitle("Mein Texteditor")

        self.setStatusBar(QStatusBar(self))

        menuBar = QMenuBar(self)

        files = QMenu("Files", menuBar)

        action_file_open = files.addAction("Open ...")
        action_file_open.triggered.connect(self.file_open)

        action_file_save = files.addAction("Save ...")
        action_file_save.triggered.connect(self.file_save)

        action_file_copy = files.addAction("Copy ...")
        action_file_copy.triggered.connect(self.file_copy)

        action_file_move = files.addAction("Move ...")
        action_file_move.triggered.connect(self.file_move)

        menuBar.addMenu(files)

        action_font = menuBar.addAction("Font")
        action_font.triggered.connect(self.font)

        self.setMenuBar(menuBar)

        self.setCentralWidget(central_widget)

    @pyqtSlot()
    def file_open(self):
        (path, self.__initial_filter) = QFileDialog.getOpenFileName(self, "Open File", self.__directory, self.__filter, self.__initial_filter)

        if path:
            self.__directory = path[:path.rfind("/")]
            self.statusBar().showMessage("File opened: " + path[path.rfind("/") + 1:])

    @pyqtSlot()
    def file_save(self):
        (path, self.__initial_filter) = QFileDialog.getSaveFileName(self, "Save File", self.__directory, self.__filter, self.__initial_filter)

        if path:
            self.__directory = path[:path.rfind("/")]
            self.statusBar().showMessage("File opened: " + path[path.rfind("/") + 1:])

    @pyqtSlot()
    def file_copy(self):
        pass

    @pyqtSlot()
    def file_move(self):
        pass

    @pyqtSlot()
    def font(self):
        QFontDialog.show()
