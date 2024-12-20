from PyQt6.QtCore import pyqtSlot
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QWidget, QTextEdit, QVBoxLayout, QHBoxLayout, QPushButton


class CentralWidget(QWidget):
    def __init__(self, parent=None):
        super(CentralWidget, self).__init__(parent)

        bar_layout = QHBoxLayout()

        self.__pushbutton_bold = QPushButton('Bold')
        self.__pushbutton_italic = QPushButton('Italic')
        self.__pushbutton_under = QPushButton('Underline')

        self.__pushbutton_bold.pressed.connect(self.__bold)

        bar_layout.addWidget(self.__pushbutton_bold)
        bar_layout.addWidget(self.__pushbutton_italic)
        bar_layout.addWidget(self.__pushbutton_under)

        self.__text_edit = QTextEdit()

        layout = QVBoxLayout()

        layout.addLayout(bar_layout)
        layout.addWidget(self.__text_edit)

        self.setLayout(layout)

    @pyqtSlot(str)
    def set_text(self, text):
        self.__text_edit.setText(text)

    def get_text(self):
        return self.__text_edit.toPlainText()

    @pyqtSlot(QFont)
    def set_font(self, font):
        self.__text_edit.setFont(font)

    @pyqtSlot()
    def __bold(self):
        cursor = self.__text_edit.textCursor()

        format = cursor.charFormat()

        font = self.__pushbutton_bold.font()

        if self.__pushbutton_bold.font().bold():
            format.setFontWeight(QFont.Weight.Normal)

            font.setBold(False)
        else:
            format.setFontWeight(QFont.Weight.Bold)

            font.setBold(True)

        cursor.setCharFormat(format)

        self.__text_edit.setTextCursor(cursor)

        self.__pushbutton_bold.setFont(font)
