import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import QSize


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.setMinimumSize(QSize(300, 200))
        self.setWindowTitle("PyQt button example - pythonprogramminglanguage.com")

        pybutton = QPushButton('Click me', self)
        pybutton.clicked.connect(self.click_method)
        pybutton.resize(100, 32)
        pybutton.move(50, 50)

    def click_method(self):
        print('Clicked Pyqt button.')


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
