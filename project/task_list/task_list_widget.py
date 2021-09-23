from PyQt5 import QtWidgets


class TaskListWidget(QtWidgets.QGroupBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setTitle("Below you can see the to do list")
        self.button = QtWidgets.QPushButton('to do list')
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.button)
        self.setLayout(layout)