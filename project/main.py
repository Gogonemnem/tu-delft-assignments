# import PyQt5
# from PyQt5 import QtGui
# from PyQt5 import QtCore

import traceback
import sys
from PyQt5 import QtWidgets
from project.agenda.agenda_widget import AgendaWidget


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.showMaximized()
        self.setWindowTitle("Breaksum")
        self.visual()
        self.show()
        self.agenda = AgendaWidget()

    def catch_exceptions(t, val, tb):
        QtWidgets.QMessageBox.critical(None,
                                       "fout met Waarde",
                                       "Een ingevulde waarde veroorzaakt een fout in de berekening\n"
                                       f"type fout: {t, val}\n"
                                       f"traceback: {traceback.format_tb(tb)[-1]}")

    def visual(self):
        #layout = QtWidgets.QVBoxLayout()
        #layout.addWidget(self.agenda)
        #self.setLayout(layout)
        self.setCentralWidget(self.agenda)


hook = sys.excepthook
sys.excepthook = MainWindow.catch_exceptions

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    app.exec_()
