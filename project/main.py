import PyQt5
import traceback
import sys

class mainwindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(mainwindow, self).__init__(*args, **kwargs)
        self.setGeometry(400, 400, 400, 400)
        self.setWindowTitle("Breaksum")
        self.show()

    def catch_exceptions(t, val, tb):

        QMessageBox.critical(None,
                             "fout met Waarde",
                             "Een ingevulde waarde veroorzaakt een fout in de berekening\n"
                              f"type fout: {t}\n"
                             f"traceback: {format_tb(tb)[-1]}")


hook = sys.excepthook
sys.excepthook = mainwindow.catch_exceptions

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = mainwindow()
    app.exec_()