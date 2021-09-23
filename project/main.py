import PyQt5
from PyQt5 import QtGui
from PyQt5 import QtCore
import traceback

from PyQt5 import QtWidgets
import sys

class mainwindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(mainwindow, self).__init__(*args, **kwargs)
        self.setGeometry(400, 400, 400, 400)
        self.setWindowTitle("Breaksum")
        self.show()

    def catch_exceptions(t, val, tb):

        QtWidgets.QMessageBox.critical(None,
                             "fout met Waarde",
                             "Een ingevulde waarde veroorzaakt een fout in de berekening\n"
                              f"type fout: {t}\n"
                             f"traceback: {format_tb(tb)[-1]}")


hook = sys.excepthook
sys.excepthook = mainwindow.catch_exceptions

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = mainwindow()
    app.exec_()