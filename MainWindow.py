from PyQt6.QtCore import pyqtSlot, QFile, QIODevice, QTextStream, pyqtSignal  # PyQt-Klassen für Signale, Dateien und Ein-/Ausgabe
from PyQt6.QtGui import QFont  # Klasse zur Handhabung von Schriftarten
from PyQt6.QtWidgets import (QMainWindow, QMenu, QMenuBar, QFileDialog, QFontDialog, QStatusBar, QMessageBox)  # GUI-Komponenten
from CentralWidget import CentralWidget  # Importiert dein zentrales Widget aus einer separaten Datei


class MainWindow(QMainWindow):  # Hauptfenster, das die gesamte Anwendung darstellt
    # Signale, die an das zentrale Widget gesendet werden können
    write_text = pyqtSignal(str)  # Ein Signal, um Text an das zentrale Widget zu senden
    write_font = pyqtSignal(QFont)  # Ein Signal, um die Schriftart an das zentrale Widget zu senden

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)  # Konstruktor der Elternklasse aufrufen

        self.__font = QFont()  # Standard-Schriftart setzen

        # Filtereinstellungen für Datei-Dialoge
        self.__initial_filter = "Default files (*.txt)"
        self.__filter = self.__initial_filter + ";;All files (*)"

        self.__directory = ""  # Anfangsverzeichnis leer setzen

        self.__central_widget = CentralWidget(self)  # Zentrales Widget instanziieren
        self.write_text.connect(self.__central_widget.set_text)  # Signal verbinden, um Text zu setzen
        self.write_font.connect(self.__central_widget.set_font)  # Signal verbinden, um die Schriftart zu setzen

        self.setWindowTitle("Mein Texteditor")  # Fenstertitel setzen
        self.setStatusBar(QStatusBar(self))  # Statusleiste hinzufügen

        menu_bar = QMenuBar(self)  # Menüleiste erstellen

        # Menü "Files" hinzufügen
        files = QMenu("Files", menu_bar)

        # "Open"-Aktion
        action_file_open = files.addAction("Open ...")
        action_file_open.triggered.connect(self.file_open)  # Verbindung mit der file_open-Methode

        # "Save"-Aktion
        action_file_save = files.addAction("Save ...")
        action_file_save.triggered.connect(self.file_save)  # Verbindung mit der file_save-Methode

        # "Copy"-Aktion (Platzhalter)
        action_file_copy = files.addAction("Copy ...")
        action_file_copy.triggered.connect(self.file_copy)  # Verbindung mit der file_copy-Methode (noch leer)

        # "Move"-Aktion (Platzhalter)
        action_file_move = files.addAction("Move ...")
        action_file_move.triggered.connect(self.file_move)  # Verbindung mit der file_move-Methode (noch leer)

        menu_bar.addMenu(files)  # "Files"-Menü zur Menüleiste hinzufügen

        # Menü "Font" hinzufügen
        font = QMenu("Font", menu_bar)

        # "Font"-Aktion
        action_font = font.addAction("Font")
        action_font.triggered.connect(self.font)  # Verbindung mit der font-Methode

        menu_bar.addMenu(font)  # "Font"-Menü zur Menüleiste hinzufügen

        self.setMenuBar(menu_bar)  # Menüleiste im Hauptfenster setzen
        self.setCentralWidget(self.__central_widget)  # Zentrales Widget setzen

    # Methode, um eine Datei zu öffnen
    @pyqtSlot()
    def file_open(self):
        # Datei-Auswahl-Dialog öffnen
        (path, self.__initial_filter) = QFileDialog.getOpenFileName(self, "Open File", self.__directory, self.__filter, self.__initial_filter)

        if path:  # Wenn ein Pfad ausgewählt wurde
            self.__directory = path[:path.rfind("/")]  # Verzeichnis des Pfads speichern
            self.statusBar().showMessage("File opened: " + path[path.rfind("/") + 1:])  # Statusleiste aktualisieren

            file = QFile(path)  # Datei-Objekt erstellen

            if not file.open(QIODevice.OpenModeFlag.ReadOnly):  # Datei im Lesemodus öffnen
                # Fehler anzeigen, wenn die Datei nicht geöffnet werden kann
                QMessageBox.information(self, "Unable to open file", file.errorString())
                return

            stream = QTextStream(file)  # Text-Stream für Datei-Inhalt
            text_in_file = stream.readAll()  # Dateiinhalt lesen

            self.write_text.emit(text_in_file)  # Textinhalt an das zentrale Widget senden

            file.close()  # Datei schließen

    # Methode, um eine Datei zu speichern
    @pyqtSlot()
    def file_save(self):
        # Datei-Speicher-Dialog öffnen
        (path, self.__initial_filter) = QFileDialog.getSaveFileName(self, "Save File", self.__directory, self.__filter, self.__initial_filter)

        if path:  # Wenn ein Pfad ausgewählt wurde
            self.__directory = path[:path.rfind("/")]  # Verzeichnis des Pfads speichern
            self.statusBar().showMessage("File saved: " + path[path.rfind("/") + 1:])  # Statusleiste aktualisieren

            file = QFile(path)  # Datei-Objekt erstellen

            if not file.open(QIODevice.OpenModeFlag.WriteOnly):  # Datei im Schreibmodus öffnen
                # Fehler anzeigen, wenn die Datei nicht geöffnet werden kann
                QMessageBox.information(self, "Unable to save file", file.errorString())
                return

            stream = QTextStream(file)  # Text-Stream für Datei-Inhalt
            stream << self.__central_widget.get_text()  # Textinhalt aus dem zentralen Widget schreiben

            stream.flush()  # Stream leeren
            file.close()  # Datei schließen

    # Methode, um eine Datei zu kopieren (noch nicht implementiert)
    @pyqtSlot()
    def file_copy(self):
        pass

    # Methode, um eine Datei zu verschieben (noch nicht implementiert)
    @pyqtSlot()
    def file_move(self):
        pass

    # Methode, um die Schriftart zu ändern
    @pyqtSlot()
    def font(self):
        # Schriftart-Dialog öffnen
        [changed_font, changed] = QFontDialog.getFont(self.__font, self, "Select your font")

        if changed:  # Wenn der Benutzer eine neue Schriftart ausgewählt hat
            self.__font = changed_font  # Schriftart speichern
            self.write_font.emit(self.__font)  # Schriftart an das zentrale Widget senden
