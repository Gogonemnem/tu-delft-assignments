import os
from PyQt5 import QtWidgets, QtGui, QtCore

absolute_path = os.path.abspath(__file__)
fileDirectory = os.path.dirname(absolute_path)
parent = os.path.dirname(fileDirectory)
path = os.path.join(parent, 'main', 'question_mark.png')


class HelpButton(QtWidgets.QGroupBox):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.msg = QtWidgets.QMessageBox()
        self.button = QtWidgets.QPushButton('Help')
        self.button.setIcon(QtGui.QIcon('question_mark.png'))
        self.button.setStyleSheet('border-radius : 50')
        self.button.clicked.connect(self.message_box)

    def message_box(self):
        self.msg.setWindowTitle("Help!")
        self.msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        self.msg.exec()
