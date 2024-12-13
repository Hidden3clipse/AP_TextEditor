from PyQt6.QtCore import pyqtSlot, QFile, QIODevice, QTextStream, pyqtSignal
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QMainWindow, QMenu, QMenuBar, QFileDialog, QFontDialog, QStatusBar, QMessageBox
from PyQt6.uic.Compiler.qtproxies import QtCore

from CentralWidget import CentralWidget


class MainWindow(QMainWindow):
    write_text = pyqtSignal(str)
    write_font = pyqtSignal(QFont)

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.__font = QFont()

        self.__initial_filter = "Default files (*.txt)"
        self.__filter = self.__initial_filter + ";;All files (*)"

        self.__directory = ""

        self.__central_widget = CentralWidget(self)
        self.write_text.connect(self.__central_widget.set_text)
        self.write_font.connect(self.__central_widget.set_font)

        self.setWindowTitle("Mein Texteditor")

        self.setStatusBar(QStatusBar(self))

        menu_bar = QMenuBar(self)

        files = QMenu("Files", menu_bar)

        action_file_open = files.addAction("Open ...")
        action_file_open.triggered.connect(self.file_open)

        action_file_save = files.addAction("Save ...")
        action_file_save.triggered.connect(self.file_save)

        action_file_copy = files.addAction("Copy ...")
        action_file_copy.triggered.connect(self.file_copy)

        action_file_move = files.addAction("Move ...")
        action_file_move.triggered.connect(self.file_move)

        menu_bar.addMenu(files)

        font = QMenu("Font", menu_bar)

        action_font = font.addAction("Font")
        action_font.triggered.connect(self.font)

        menu_bar.addMenu(font)

        self.setMenuBar(menu_bar)

        self.setCentralWidget(self.__central_widget)

    @pyqtSlot()
    def file_open(self):
        (path, self.__initial_filter) = QFileDialog.getOpenFileName(self, "Open File", self.__directory, self.__filter, self.__initial_filter)

        if path:
            self.__directory = path[:path.rfind("/")]
            self.statusBar().showMessage("File opened: " + path[path.rfind("/") + 1:])

            file = QFile(path)

            if not file.open(QIODevice.OpenModeFlag.ReadOnly):
                QMessageBox.information(self, "Unable to open file", file.errorString())

                return

            stream = QTextStream(file)
            text_in_file = stream.readAll()

            self.write_text.emit(text_in_file)

            file.close()

    @pyqtSlot()
    def file_save(self):
        (path, self.__initial_filter) = QFileDialog.getSaveFileName(self, "Save File", self.__directory, self.__filter, self.__initial_filter)

        if path:
            self.__directory = path[:path.rfind("/")]
            self.statusBar().showMessage("File saved: " + path[path.rfind("/") + 1:])

            file = QFile(path)

            if not file.open(QIODevice.OpenModeFlag.WriteOnly):
                QMessageBox.information(self, "Unable to save file", file.errorString())

                return

            stream = QTextStream(file)
            stream << self.__central_widget.get_text()

            stream.flush()
            file.close()

    @pyqtSlot()
    def file_copy(self):
        pass

    @pyqtSlot()
    def file_move(self):
        pass

    @pyqtSlot()
    def font(self):
        [changed_font, changed] =QFontDialog.getFont(self.__font, self, "Select your font")

        if changed:
            self.__font = changed_font

            self.write_font.emit(self.__font)
