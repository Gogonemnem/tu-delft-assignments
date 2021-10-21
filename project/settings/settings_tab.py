import os
from PyQt5 import QtWidgets

absolute_path = os.path.abspath(__file__)
fileDirectory = os.path.dirname(absolute_path)
parent = os.path.dirname(fileDirectory)
path = os.path.join(parent, 'main', 'saved_settings')
path_description = os.path.join(parent, 'main', 'description_file')


class SettingsTab(QtWidgets.QWidget):
    """Visualizes the settings"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.settings = Settings()
        self.description = Description()

        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.settings, 0, 0)
        layout.addWidget(self.description, 0, 1)
        self.setLayout(layout)


class Settings(QtWidgets.QGroupBox):
    """Ables the user to change some of the settings for the application"""

    def __init__(self, file=path, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setTitle('Settings')
        self.layout = QtWidgets.QFormLayout()

        # Read the saved settings and save them in self.settings
        self.file = file
        self.settings = []
        self.read_settings()

        # Change the time between tasks
        self.time = QtWidgets.QSpinBox(self)
        self.set_time_breaks()

        # Change the time for a snooze
        self.snooze = QtWidgets.QSpinBox(self)
        self.set_snooze_time()

        # Add done button after changing settings
        self.change = QtWidgets.QPushButton('Change settings')
        self.change.clicked.connect(self.change_settings)
        self.layout.addWidget(self.change)

        # Set layout
        self.setLayout(self.layout)

    def change_settings(self):
        """Changes the settings and saves them externally"""
        self.settings[0] = self.time.value()
        self.settings[1] = self.snooze.value()
        self.save_settings()

    def set_time_breaks(self):
        """Lets the user set the average time between breaks"""
        self.time.setMinimum(15)
        self.time.setMaximum(120)
        self.time.setValue(int(self.settings[0]))
        self.layout.addRow('The average time between breaks in minutes', self.time)

    def set_snooze_time(self):
        """Lets the user set the time of the snooze"""
        self.snooze.setMinimum(1)
        self.snooze.setMaximum(20)
        self.snooze.setValue(int(self.settings[1]))
        self.layout.addRow('The time of the a snooze', self.snooze)

    def read_settings(self):
        """Reads the settings from the file and saves them in a list"""
        with open(self.file) as fin:
            for line in fin:
                self.settings.append(line.strip())

    def save_settings(self):
        """Saves the settings from the list in the file"""
        with open(self.file, 'w') as fin:
            for setting in self.settings:
                fin.write(f'{setting}\n')


class Description(QtWidgets.QGroupBox):
    def __init__(self, file=path_description, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setTitle('Description')
        self.layout = QtWidgets.QVBoxLayout(self)
        text = QtWidgets.QTextBrowser(self)

        # Read the text file and insert it as html in the QTextBrowser
        with open(file) as fin:
            lines = fin.readlines()
            print(''.join(lines))
            text.insertHtml(''.join(lines))

        self.layout.addWidget(text)

        self.setLayout(self.layout)
