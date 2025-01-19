from PyQt6.QtCore import pyqtSlot  # pyqtSlot wird verwendet, um Funktionen (Slots) für PyQt-Signale zu definieren
from PyQt6.QtGui import QFont  # QFont hilft uns, mit Schriftarten zu arbeiten (z. B. fett, kursiv)
from PyQt6.QtWidgets import QWidget, QTextEdit, QVBoxLayout, QHBoxLayout, QPushButton  # PyQt-Widgets für die GUI

# Diese Klasse ist das Hauptwidget, das die Benutzeroberfläche erstellt.
class CentralWidget(QWidget):
    def __init__(self, parent=None):
        super(CentralWidget, self).__init__(parent)  # Ruft den Konstruktor der Elternklasse auf

        # Layout für die Formatierungs-Schaltflächen (fett, kursiv, unterstreichen)
        bar_layout = QHBoxLayout()

        # Erstellt drei Schaltflächen mit den Beschriftungen 'Bold', 'Italic' und 'Underline'
        self.__pushbutton_bold = QPushButton('Bold')
        self.__pushbutton_italic = QPushButton('Italic')
        self.__pushbutton_underline = QPushButton('Underline')

        # Verbindet die Schaltflächen mit ihren jeweiligen Funktionen
        self.__pushbutton_bold.pressed.connect(self.__bold)
        self.__pushbutton_italic.pressed.connect(self.__italic)
        self.__pushbutton_underline.pressed.connect(self.__underline)

        # Fügt die Schaltflächen in das horizontale Layout ein
        bar_layout.addWidget(self.__pushbutton_bold)
        bar_layout.addWidget(self.__pushbutton_italic)
        bar_layout.addWidget(self.__pushbutton_underline)

        # Erstellt ein großes Textfeld, in dem der Benutzer Text eingeben kann
        self.__text_edit = QTextEdit()

        # Layout für die gesamte Benutzeroberfläche (vertikal)
        layout = QVBoxLayout()

        # Fügt die Schaltflächen und das Textfeld in das vertikale Layout ein
        layout.addLayout(bar_layout)  # Schaltflächenleiste oben
        layout.addWidget(self.__text_edit)  # Textfeld darunter

        # Setzt das Layout für dieses Widget
        self.setLayout(layout)

    # Funktion, um den Text im Textfeld zu setzen
    @pyqtSlot(str)  # Diese Funktion akzeptiert einen String als Eingabe
    def set_text(self, text):
        self.__text_edit.setText(text)  # Setzt den Text im Textfeld

    # Funktion, um den aktuellen Text aus dem Textfeld zu bekommen
    def get_text(self):
        return self.__text_edit.toPlainText()  # Gibt den reinen Text (ohne Formatierung) zurück

    # Funktion, um die Schriftart des Textfeldes zu setzen
    @pyqtSlot(QFont)  # Diese Funktion akzeptiert ein QFont-Objekt als Eingabe
    def set_font(self, font):
        self.__text_edit.setFont(font)  # Setzt die Schriftart des Textfelds

    # Funktion, die ausgeführt wird, wenn die 'Bold'-Schaltfläche gedrückt wird
    @pyqtSlot()
    def __bold(self):
        cursor = self.__text_edit.textCursor()  # Holt den aktuellen Cursor (wo der Benutzer schreibt)
        format = cursor.charFormat()  # Holt das aktuelle Zeichenformat

        font = self.__pushbutton_bold.font()  # Holt die aktuelle Schriftart der 'Bold'-Schaltfläche

        if self.__pushbutton_bold.font().bold():  # Überprüft, ob die Schaltfläche fett formatiert ist
            format.setFontWeight(QFont.Weight.Normal)  # Setzt das Gewicht auf "normal" (kein Fett)
            font.setBold(False)  # Entfernt das Fett aus der Schaltflächen-Schriftart
        else:
            format.setFontWeight(QFont.Weight.Bold)  # Setzt das Gewicht auf "fett"
            font.setBold(True)  # Setzt die Schaltflächen-Schriftart auf "fett"

        cursor.setCharFormat(format)  # Aktualisiert das Zeichenformat an der Cursor-Position
        self.__text_edit.setTextCursor(cursor)  # Setzt den aktualisierten Cursor zurück

        self.__pushbutton_bold.setFont(font)  # Aktualisiert die Schaltflächen-Schriftart

    # Funktion, die ausgeführt wird, wenn die 'Italic'-Schaltfläche gedrückt wird
    @pyqtSlot()
    def __italic(self):
        cursor = self.__text_edit.textCursor()  # Holt den aktuellen Cursor
        format = cursor.charFormat()  # Holt das aktuelle Zeichenformat

        font = self.__pushbutton_italic.font()  # Holt die aktuelle Schriftart der 'Italic'-Schaltfläche

        if self.__pushbutton_italic.font().italic():  # Überprüft, ob die Schaltfläche kursiv ist
            format.setFontItalic(False)  # Setzt den Text auf "nicht kursiv"
            font.setItalic(False)  # Entfernt die kursive Formatierung von der Schaltfläche
        else:
            format.setFontItalic(True)  # Setzt den Text auf "kursiv"
            font.setItalic(True)  # Setzt die Schaltflächen-Schriftart auf "kursiv"

        cursor.setCharFormat(format)  # Aktualisiert das Zeichenformat
        self.__text_edit.setTextCursor(cursor)  # Setzt den aktualisierten Cursor zurück

        self.__pushbutton_italic.setFont(font)  # Aktualisiert die Schaltflächen-Schriftart

    # Funktion, die ausgeführt wird, wenn die 'Underline'-Schaltfläche gedrückt wird
    @pyqtSlot()
    def __underline(self):
        cursor = self.__text_edit.textCursor()  # Holt den aktuellen Cursor
        format = cursor.charFormat()  # Holt das aktuelle Zeichenformat

        font = self.__pushbutton_underline.font()  # Holt die aktuelle Schriftart der 'Underline'-Schaltfläche

        if self.__pushbutton_underline.font().underline():  # Überprüft, ob die Schaltfläche unterstrichen ist
            format.setFontUnderline(False)  # Entfernt die Unterstreichung vom Text
            font.setUnderline(False)  # Entfernt die Unterstreichung von der Schaltfläche
        else:
            format.setFontUnderline(True)  # Setzt die Unterstreichung auf den Text
            font.setUnderline(True)  # Setzt die Schaltfläche auf "unterstrichen"

        cursor.setCharFormat(format)  # Aktualisiert das Zeichenformat
        self.__text_edit.setTextCursor(cursor)  # Setzt den aktualisierten Cursor zurück

        self.__pushbutton_underline.setFont(font)  # Aktualisiert die Schaltflächen-Schriftart
