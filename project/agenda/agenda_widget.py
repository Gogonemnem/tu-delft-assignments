# import PyQt5
# from PyQt5 import QtGui
# from PyQt5 import QtCore

import traceback
import sys
from PyQt5 import QtWidgets


class AgendaWidget(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setGeometry(800, 800)
        self.button = QtWidgets.QPushButton('test')
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.button)
        self.setLayout(layout)