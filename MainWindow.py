# Importiere die benötigten PyQt6-Klassen
from PyQt6.QtCore import pyqtSlot, QFile, QIODevice, QTextStream, pyqtSignal  # Klassen für Signale, Dateien und Ein-/Ausgabe
from PyQt6.QtGui import QFont  # Klasse zur Handhabung von Schriftarten
from PyQt6.QtWidgets import (  # GUI-Komponenten wie Fenster, Menüs, Dialoge und Statusleisten
    QMainWindow, QMenu, QMenuBar, QFileDialog, QFontDialog, QStatusBar, QMessageBox
)
from CentralWidget import CentralWidget  # Importiert ein separates zentrales Widget (deine Texteditor-Logik)


class MainWindow(QMainWindow):  # Hauptfenster der Anwendung
    # Signale, die später an das zentrale Widget gesendet werden können
    write_text = pyqtSignal(str)  # Signal, um Text an das zentrale Widget zu senden
    write_font = pyqtSignal(QFont)  # Signal, um die Schriftart an das zentrale Widget zu senden

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)  # Konstruktor der Elternklasse aufrufen

        self.__font = QFont()  # Standard-Schriftart initialisieren
        self.__initial_filter = "Default files (*.txt)"  # Standard-Dateifilter
        self.__filter = self.__initial_filter + ";;All files (*)"  # Zusätzlicher Filter für alle Dateien
        self.__directory = ""  # Anfangsverzeichnis für Datei-Dialoge (leer)

        # Zentrales Widget instanziieren und mit den Signalen verbinden
        self.__central_widget = CentralWidget(self)
        self.write_text.connect(self.__central_widget.set_text)  # Verbindet das `write_text`-Signal mit `set_text` im Widget
        self.write_font.connect(self.__central_widget.set_font)  # Verbindet das `write_font`-Signal mit `set_font` im Widget

        self.setWindowTitle("Mein Texteditor")  # Setze den Titel des Fensters
        self.setStatusBar(QStatusBar(self))  # Erstelle eine Statusleiste am unteren Rand des Fensters

        menu_bar = QMenuBar(self)  # Erstelle eine Menüleiste

        # Menü "Files" erstellen
        files = QMenu("Files", menu_bar)

        # Aktion zum Öffnen einer Datei
        action_file_open = files.addAction("Open ...")
        action_file_open.triggered.connect(self.file_open)  # Verbindet die Aktion mit der Methode `file_open`

        # Aktion zum Speichern einer Datei
        action_file_save = files.addAction("Save ...")
        action_file_save.triggered.connect(self.file_save)  # Verbindet die Aktion mit der Methode `file_save`

        # Aktion zum Kopieren einer Datei
        action_file_copy = files.addAction("Copy ...")
        action_file_copy.triggered.connect(self.file_copy)  # Verbindet die Aktion mit der Methode `file_copy`

        # Aktion zum Verschieben einer Datei
        action_file_move = files.addAction("Move ...")
        action_file_move.triggered.connect(self.file_move)  # Verbindet die Aktion mit der Methode `file_move`

        menu_bar.addMenu(files)  # Füge das "Files"-Menü zur Menüleiste hinzu

        # Menü "Font" erstellen
        font = QMenu("Font", menu_bar)
        action_font = font.addAction("Font")  # Aktion zum Ändern der Schriftart hinzufügen
        action_font.triggered.connect(self.font)  # Verbindet die Aktion mit der Methode `font`
        menu_bar.addMenu(font)  # Füge das "Font"-Menü zur Menüleiste hinzu

        self.setMenuBar(menu_bar)  # Setze die erstellte Menüleiste im Fenster
        self.setCentralWidget(self.__central_widget)  # Setze das zentrale Widget in das Hauptfenster

    # Methode, um eine Datei zu öffnen
    @pyqtSlot()
    def file_open(self):
        # Datei-Auswahl-Dialog anzeigen
        (path, self.__initial_filter) = QFileDialog.getOpenFileName(
            self, "Open File", self.__directory, self.__filter, self.__initial_filter
        )

        if path:  # Wenn ein Pfad ausgewählt wurde
            self.__directory = path[:path.rfind("/")]  # Speichere das Verzeichnis des ausgewählten Pfads
            self.statusBar().showMessage("File opened: " + path[path.rfind("/") + 1:])  # Zeige den Dateinamen in der Statusleiste an

            file = QFile(path)  # Erstelle ein QFile-Objekt
            if not file.open(QIODevice.OpenModeFlag.ReadOnly):  # Öffne die Datei im Lesemodus
                # Zeige eine Fehlermeldung an, wenn die Datei nicht geöffnet werden kann
                QMessageBox.information(self, "Unable to open file", file.errorString())
                return

            stream = QTextStream(file)  # Erstelle einen Textstream für die Datei
            text_in_file = stream.readAll()  # Lese den gesamten Inhalt der Datei

            # Hier wird der gelesene Text aufgeteilt
            split_text = text_in_file.split('.')  # Teile den Text anhand von Punkten

            # Füge den gesamten Originaltext und die geteilten Teile ins zentrale Widget ein
            self.write_text.emit("Original Text:\n" + text_in_file)  # Original-Text anzeigen
            self.write_text.emit("\nSplit Parts:")  # Überschrift für die geteilten Teile
            for part in split_text:
                self.write_text.emit(part.strip())  # Jede geteilte Komponente hinzufügen

            file.close()  # Schließe die Datei

    # Methode, um eine Datei zu speichern
    @pyqtSlot()
    def file_save(self):
        # Datei-Speicher-Dialog anzeigen
        (path, self.__initial_filter) = QFileDialog.getSaveFileName(
            self, "Save File", self.__directory, self.__filter, self.__initial_filter
        )

        if path:  # Wenn ein Pfad ausgewählt wurde
            self.__directory = path[:path.rfind("/")]  # Speichere das Verzeichnis des ausgewählten Pfads
            self.statusBar().showMessage("File saved: " + path[path.rfind("/") + 1:])  # Zeige den Dateinamen in der Statusleiste an

            file = QFile(path)  # Erstelle ein QFile-Objekt
            if not file.open(QIODevice.OpenModeFlag.WriteOnly):  # Öffne die Datei im Schreibmodus
                # Zeige eine Fehlermeldung an, wenn die Datei nicht gespeichert werden kann
                QMessageBox.information(self, "Unable to save file", file.errorString())
                return

            stream = QTextStream(file)  # Erstelle einen Textstream für die Datei
            stream << self.__central_widget.get_text()  # Schreibe den Textinhalt aus dem zentralen Widget in die Datei
            stream.flush()  # Leere den Stream
            file.close()  # Schließe die Datei

    # Methode, um eine Datei zu kopieren
    @pyqtSlot()
    def file_copy(self):
        # Dialog, um die Quelldatei auszuwählen
        (source_path, _) = QFileDialog.getOpenFileName(self, "Select File to Copy", self.__directory, self.__filter)

        if source_path:  # Wenn ein Pfad ausgewählt wurde
            # Dialog, um den Zielort auszuwählen
            (dest_path, _) = QFileDialog.getSaveFileName(self, "Select Destination for Copy", self.__directory, self.__filter)

            if dest_path:  # Wenn ein Zielort ausgewählt wurde
                if QFile.copy(source_path, dest_path):  # Versuche, die Datei zu kopieren
                    self.statusBar().showMessage(f"File copied to: {dest_path}")  # Zeige eine Erfolgsmeldung an
                else:
                    QMessageBox.warning(self, "Copy Error", "Unable to copy the file.")  # Zeige eine Fehlermeldung an

    # Methode, um eine Datei zu verschieben
    @pyqtSlot()
    def file_move(self):
        # Dialog, um die Quelldatei auszuwählen
        (source_path, _) = QFileDialog.getOpenFileName(self, "Select File to Move", self.__directory, self.__filter)

        if source_path:  # Wenn ein Pfad ausgewählt wurde
            # Dialog, um den Zielort auszuwählen
            (dest_path, _) = QFileDialog.getSaveFileName(self, "Select Destination for Move", self.__directory, self.__filter)

            if dest_path:  # Wenn ein Zielort ausgewählt wurde
                if QFile.copy(source_path, dest_path):  # Kopiere die Datei
                    QFile.remove(source_path)  # Lösche die Quelldatei
                    self.statusBar().showMessage(f"File moved to: {dest_path}")  # Zeige eine Erfolgsmeldung an
                else:
                    QMessageBox.warning(self, "Move Error", "Unable to move the file.")  # Zeige eine Fehlermeldung an

    # Methode, um die Schriftart zu ändern
    @pyqtSlot()
    def font(self):
        # Öffne einen Schriftart-Dialog
        [changed_font, changed] = QFontDialog.getFont(self.__font, self, "Select your font")

        if changed:  # Wenn der Benutzer eine Schriftart ausgewählt hat
            self.__font = changed_font  # Aktualisiere die Schriftart
            self.write_font.emit(self.__font)  # Sende die Schriftart an das zentrale Widget
