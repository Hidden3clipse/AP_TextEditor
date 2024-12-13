from PyQt6.QtCore import pyqtSlot
from PyQt6.QtWidgets import QWidget, QTextEdit, QVBoxLayout, QHBoxLayout, QPushButton


class CentralWidget(QWidget):
    def __init__(self, parent=None):
        super(CentralWidget, self).__init__(parent)

        bar_layout = QHBoxLayout()

        pushbutton_bold = QPushButton('Bold')
        pushbutton_italic = QPushButton('Italic')
        pushbutton_under = QPushButton('Underline')

        bar_layout.addWidget(pushbutton_bold)
        bar_layout.addWidget(pushbutton_italic)
        bar_layout.addWidget(pushbutton_under)

        self.__text_edit = QTextEdit()

        layout = QVBoxLayout()

        layout.addLayout(bar_layout)
        layout.addWidget(self.__text_edit)

        self.setLayout(layout)

    @pyqtSlot(str)
    def set_text(self, text):
        self.__text_edit.setText(text)
