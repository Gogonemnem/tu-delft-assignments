from PyQt5.QtWidgets import QMessageBox

class Popup():
    def popup_when_time_is_up(self):
        pop_up = QMessageBox()

        # Creates buttons on the pop-up
        pop_up.addButton(pop_up.Ok)
        do = pop_up.addButton('Do Task', pop_up.ActionRole)
        completed = pop_up.addButton('Task Completed', pop_up.ActionRole)
        snooze = pop_up.addButton('Snooze Task', pop_up.ActionRole)
        skip = pop_up.addButton('Skip Task', pop_up.ActionRole)
        reschedule = pop_up.addButton('Reschedule Task', pop_up.ActionRole)
        another = pop_up.addButton('Another Task', pop_up.ActionRole)
        redo = pop_up.addButton('Redo Task', pop_up.ActionRole)

        do.clicked.connect()
        completed.clicked.connect()
        snooze.clicked.connect()
        skip.clicked.connect()
        reschedule.clicked.connect()
        another.clicked.connect()
        redo.clicked.connect()


