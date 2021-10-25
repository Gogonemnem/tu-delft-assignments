import datetime
import sys

from PyQt5 import QtWidgets, Qt
from PyQt5.QtCore import QTime
from PyQt5.QtWidgets import QMessageBox, QTimeEdit, QDialog, QInputDialog, QWidget, QLayout, QVBoxLayout, \
    QDialogButtonBox


class Popup:
    @staticmethod
    def pop_up(task: dict):
        statuses = 'Do', 'Remove', 'Complete', 'Reschedule', 'Do another', 'Snooze', 'Skip', 'Redo'
        buttons = [None]
        pop_up = QMessageBox()
        pop_up.setText(task['Task'])

        # Creates buttons on the pop-up
        for status in statuses:
            button = pop_up.addButton(status + ' Task', QMessageBox.YesRole)
            buttons.append(button)

        pop_up.exec()

        for i, button in enumerate(buttons):
            if pop_up.clickedButton() == button:
                return i
        return -1


class TimeDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        # nice widget for editing the date
        self.time = QTimeEdit(self)
        self.time.setTime(QTime.currentTime())
        layout = QVBoxLayout(self)
        layout.addWidget(self.time)

        # OK and Cancel buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    # static method to create the dialog and return (time, accepted)
    @staticmethod
    def get_time(parent=None):
        dialog = TimeDialog(parent)
        result = dialog.exec_()
        time = dialog.time.time().toPyTime()
        today = datetime.date.today()
        date_time = datetime.datetime.combine(today, time)
        return date_time, result == QDialog.Accepted


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = TimeDialog()
    window.show()
    app.exec_()
# self.time.setCalendarPopup(True)
