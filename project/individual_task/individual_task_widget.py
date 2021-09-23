from PyQt5 import QtWidgets


class TaskWidget(QtWidgets.QGroupBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setTitle("Individual tasks can be added here")
        self.button = QtWidgets.QPushButton('individual task input')
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.button)
        self.setLayout(layout)