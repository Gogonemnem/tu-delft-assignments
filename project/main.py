# import traceback
# import PyQt5
# from PyQt5 import QtGui
# from PyQt5 import QtCore


import sys
from PyQt5 import QtWidgets


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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
sys.excepthook = MainWindow.catch_exceptions

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    app.exec_()
