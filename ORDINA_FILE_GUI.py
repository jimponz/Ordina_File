import datetime
import os
import sys
from datetime import datetime

from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QMessageBox

import ORDINA_FILE

#from inspect_dir_cython import inspect_dir

qtcreator_file  = "ORDINA_FILE.ui"

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtcreator_file)


class File:
    path = ""
    size = 0

    def format_bytes(self, size):
        # 2**10 = 1024
        power = 2**10
        n = 0
        power_labels = {0: '', 1: 'K', 2: 'M', 3: 'G', 4: 'T'}
        while size > power:
            size /= power
            n += 1
        return str(round(size, 2)) + " " + power_labels[n]+'B'

    def __init__(self, path):
        if os.path.isfile(path):
            self.path = path
            self.size = os.stat(path).st_size

    def __str__(self):
        return "\nPath: " + self.path + "\nSize: " + self.format_bytes(self.size)


class MyWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    input_dir = os.getcwd()
    dir_size = 0
    selected = ""
    listOfFiles = []
    list_moved = []

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.showMaximized()

        self.listWidget.itemClicked.connect(self.onClicked)

        self.buttonFolder.clicked.connect(self.onClickFolder)
        self.buttonMove.clicked.connect(self.move_to_dirs)
        self.buttonOpenFile.clicked.connect(self.onClickOpen)
        self.buttonDelete.clicked.connect(self.onClickDelete)
        self.buttonWrite.clicked.connect(self.onClickWrite)

        self.buttonDirChooser.clicked.connect(self.choose_dir)
        #self.buttonRefresh.clicked.connect(self.refresh_dir)

        self.labelPath.setText(self.input_dir)
        self.labelStatus.setText("Status: Pronto!")

        self.init_dir(self.input_dir)
        
        self.setStyleSheet("MyWindow{ background-color: rgb(54, 54, 54);}")

    def move_to_dirs(self):
        if len(self.listOfFiles) > 0:
            ret = QMessageBox.question(self, 'Stai per spostare dei file!', "Stai per spostare dei file, vuoi procedere?", QMessageBox.Yes | QMessageBox.Cancel)
            if ret == QMessageBox.Yes:
                print('Button QMessageBox.Yes clicked.')
                res = ORDINA_FILE.OrdinaFile(self.input_dir)
                res.analyze_dir()
                listMoved = res.move_to_dirs()
                self.list_moved = listMoved
                lenList = len(listMoved)

                labelStatusMessage = ""
                labelListMessage = ""
                if lenList > 0:
                    self.listWidget.clear()
                    self.listWidget.addItems(listMoved)

                    labelStatusMessage = "Status: " + str(lenList) + " file spostati!"
                    labelListMessage = "I seguenti " + str(lenList) + " file sono stati spostati in questo percorso:"
                else:
                    self.listWidget.clear()
                    self.listWidget.addItem("Non è stato spostato nessun file! Controlla il percorso di lavoro!")

                    labelListMessage = "Si è verificato un errore e nessun file è stato spostato!"
                    labelStatusMessage = "Status: Non è stato spostato nessun file!"

                self.labelList.setText(labelListMessage)
                self.labelStatus.setText(labelStatusMessage)
        else:
            QMessageBox.information(self, "Info", "Nel percorso attuale non ci sono file da spostare!")

    def init_dir(self, input_dir):
        try:
            self.listOfFiles.clear()
            self.listWidget.clear()
            self.selected = ""
            self.input_dir = input_dir
            self.inspect_dir(input_dir)

            self.labelSelected.setText(self.selected)
            self.labelPath.setText(self.input_dir)

        except Exception as ex:
            message = "Si è verificata un'eccezione in init_dir " + str(ex)
            print(message)
            self.labelStatus.setText(message)

    def choose_dir(self):
        try:
            self.input_dir = QFileDialog.getExistingDirectory(self, "Scegli la cartella da analizzare", self.input_dir)
            self.init_dir(self.input_dir)

        except Exception as ex:
            message = "Si è verificata un'eccezione in choose_dir " + str(ex)
            print(message)
            self.labelStatus.setText(message)

    def inspect_dir(self, input_dir):
        try:
            self.input_dir = input_dir
            self.labelPath.setText(input_dir)

            res = ORDINA_FILE.OrdinaFile(self.input_dir)
            res.analyze_dir()

            message = "Status: Analizzando la cartella " + self.input_dir
            self.labelStatus.setText(message)

            self.listOfFiles = res.listOfFiles
            self.listWidget.addItems(res.listOfFiles)
            lenListOfFiles = len(res.listOfFiles)
            if lenListOfFiles > 0:
                self.labelStatus.setText("Status: Pronto!")
                message = "Nella cartella attuale sono presenti i seguenti " + str(lenListOfFiles) + " file che vorrei spostare:"
                self.labelList.setText(res.message)
            else:
                self.listWidget.clear()
                self.listWidget.addItem("Non è stato trovato nessun file da spostare! Controlla il percorso di lavoro!")
                self.labelStatus.setText("Status: Non è stato trovato nessun file da spostare!")
                message = "Nella cartella attuale non è stato trovato nessun file da spostare:"
                self.labelList.setText(message)
        except Exception as ex:
            message = "Si è verificata un'eccezione in inspect_dir " + str(ex)
            print(message)
            self.labelStatus.setText(message)

    def onClicked(self, item):
        #QMessageBox.information(self, "Info", item.text())
        try:
            self.selected = item.text()
            self.labelSelected.setText(self.selected)

        except Exception as ex:
            message = "Si è verificata un'eccezione in onClicked" + str(ex)
            print(message)
            self.labelStatus.setText(message)


    def onClickDelete(self):
        try:
            filepath = self.selected

            ret = QMessageBox.question(self, 'Stai per cancellare dei file!', "Stai per cancellare " + filepath + " , vuoi procedere?", QMessageBox.Yes | QMessageBox.Cancel)
            if ret == QMessageBox.Yes:
                print('Button QMessageBox.Yes clicked.')
                index = self.listWidget.currentRow()
                self.listWidget.takeItem(index)
                os.remove(filepath)
                self.labelStatus.setText("Status: " + filepath + " ELIMINATO!")

        except Exception as ex:
            message = "\nSi è verificata un'eccezione in onClickDelete" + str(ex)
            print(message)
            self.labelStatus.setText(message)

    def onClickOpen(self):
        try:
            if self.selected:
                os.startfile(self.selected)
            else:
                message = "Status: Nessun file selezionato, seleziona un file prima!"
                self.labelStatus.setText(message)
                QMessageBox.information(self, "Info", message)

        except Exception as ex:
            message = "Si è verificata un'eccezione in onClickOpen " + str(ex)
            print(message)
            self.labelStatus.setText(message)

    def onClickFolder(self):
        try:
            os.startfile(self.input_dir)
        except Exception as ex:
            message = "Si è verificata un'eccezione in onClickFolder " + str(ex)
            print(message)
            self.labelStatus.setText(message)

    def onClickWrite(self):
        try:

                date_time = datetime.now().strftime("%m%d%Y%H%M%S")

                prefix = date_time
                suffix = "_results.txt"
                filename = prefix + suffix

                caption = ""
                source = []

                if len(self.list_moved) > 0:
                    message = "Stai per scrivere la lista dei file spostati su file, vuoi procedere?"
                    caption = "\n---------- File spostati da " + self.input_dir + " ----------\n\n"
                    source = self.list_moved
                else:
                    message = "Se procedi ora, scriverai l'analisi della cartella (non sono stati ancora spostati file), vuoi procedere?"
                    caption = "\n---------- Analisi file che vorrei spostare da " + self.input_dir + " ----------\n\n"
                    source = self.listOfFiles

                ret = QMessageBox.question(self, 'Stai per scrivere su file!', message ,
                                           QMessageBox.Yes | QMessageBox.Cancel)
                if ret == QMessageBox.Yes:
                    print('Button QMessageBox.Yes clicked.')
                    with open(filename, "a") as file:
                        file.write(caption)

                        for elem in source:
                            try:
                                file.write(str(elem))
                                file.write("\n")
                            except Exception as ex:
                                message = "Si è verificata un'eccezione scrivendo: " + str(elem) + "\n" + str(ex)
                                print(message)
                                self.labelStatus.setText(message)


                    ret = QMessageBox.question(self, 'File scritto correttamente!', "File scritto correttamente!\n\nLo trovi in " +
                                               os.path.join(self.input_dir, filename) + "\n\nLo vuoi aprire subito?",
                                               QMessageBox.Yes | QMessageBox.Cancel)
                    if ret == QMessageBox.Yes:
                        print('Button QMessageBox.Yes clicked.')
                        os.startfile(filename)

                    self.labelStatus.setText("Status: File scritto correttamente!")

        except Exception as ex:
            message = "Si è verificata un'eccezione in onClickWrite " + str(ex)
            print(message)
            self.labelStatus.setText(message)

    # def refresh_dir(self):
    #     self.init_dir(self, self.input_dir)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
