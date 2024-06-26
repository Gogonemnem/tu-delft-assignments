import os

from PyQt5 import QtWidgets

from project.randomizer.time_randomizer import TimeRandomizer

absolute_path = os.path.abspath(__file__)
fileDirectory = os.path.dirname(absolute_path)
parent = os.path.dirname(fileDirectory)
path = os.path.join(parent, 'main', 'saved_settings')
path_description = os.path.join(parent, 'main', 'description_file')


class SettingsTab(QtWidgets.QWidget):
    """Visualizes the settings"""

    def __init__(self, time_randomizer: TimeRandomizer, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.settings = Settings(time_randomizer)
        self.description = Description()

        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.settings, 0, 0)
        layout.addWidget(self.description, 0, 1)
        self.setLayout(layout)


class Settings(QtWidgets.QGroupBox):
    """Ables the user to change some of the settings for the application."""

    def __init__(self, time_randomizer: TimeRandomizer, *args, file=path, **kwargs):
        super().__init__(*args, **kwargs)
        self.setTitle('Settings')
        self.layout = QtWidgets.QFormLayout()
        self.time_randomizer = time_randomizer

        # Read the saved settings and save them in self.settings
        self.file = file
        self.settings = self.read_settings(self.file)

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
        self.change_settings()

        # Set layout
        self.setLayout(self.layout)

    def change_settings(self):
        """Changes the settings and saves them externally."""
        self.settings[0] = self.time.value()
        self.settings[1] = self.snooze.value()
        self.save_settings(self.file, self.settings)

        self.time_randomizer.set_average_break_time(int(self.settings[0]) * 60000)
        self.time_randomizer.snooze_time = int(self.settings[1]) * 60000

    def set_time_breaks(self):
        """Lets the user set the average time between breaks."""
        self.time.setMinimum(15)
        self.time.setMaximum(120)
        self.time.setValue(int(self.settings[0]))
        self.layout.addRow('The average time between breaks in minutes', self.time)

    def set_snooze_time(self):
        """Lets the user set the time of the snooze."""
        self.snooze.setMinimum(1)
        self.snooze.setMaximum(20)
        self.snooze.setValue(int(self.settings[1]))
        self.layout.addRow('The time the notification is snoozed in minutes', self.snooze)

    @staticmethod
    def read_settings(file):
        """Reads the settings from the file and returns them as a list."""
        settings = []
        with open(file, encoding='utf-8') as fin:
            for line in fin:
                settings.append(int(line.strip()))

        return settings

    @staticmethod
    def save_settings(file, settings):
        """Saves the settings from the list in the file."""
        with open(file, 'w', encoding='utf-8') as fin:
            for setting in settings:
                fin.write(f'{setting}\n')


class Description(QtWidgets.QGroupBox):
    def __init__(self, *args, file=path_description, **kwargs):
        super().__init__(*args, **kwargs)

        self.setTitle('Description')
        self.layout = QtWidgets.QVBoxLayout(self)
        text = QtWidgets.QTextBrowser(self)

        # Read the text file and insert it as html in the QTextBrowser
        with open(file, encoding='utf-8') as fin:
            lines = fin.readlines()
            text.insertHtml(''.join(lines))

        # Add the text as a widget to the layout and use setLayout
        self.layout.addWidget(text)
        self.setLayout(self.layout)
