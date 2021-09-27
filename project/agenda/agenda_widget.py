from PyQt5 import QtWidgets


class AgendaWidget(QtWidgets.QGroupBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setTitle("The agenda can be seen below")
        self.button = QtWidgets.QPushButton('agenda')
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.button)
        self.setLayout(layout)
