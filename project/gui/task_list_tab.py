from PyQt5 import QtWidgets
from PyQt5.QtCore import QAbstractTableModel, Qt

from project.task_list.data_for_database import TaskList


class TaskListTab(QtWidgets.QTableView):
    """This class creates the task list tab and visualizes it."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.database = TaskList()
        self.model = None
        self.index = None

        # Visualise the database, including the delete and edit buttons
        self.refresh()

        # Creates a help button, which explains the database
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)
        self.setWhatsThis('This tab shows the whole database. '
                          'This means it shows all the possible tasks '
                          'that might appear on your daily to do list. '
                          'Except the tasks you have marked as: "must be done today" '
                          'Those are certain to appear.\n'
                          'You can also edit or delete your tasks here.\n'
                          'To delete a task, simply click the delete button, '
                          'but be beware! The task will be permanently deleted once you click.\n'
                          'To edit a task, click the edit button. '
                          'You will then get the option to edit a specific part of a task.')

    def delete_button_clicked(self):
        """Delete a row from the database and refresh the screen."""

        # Gets the index of the deleted row
        button = self.sender()
        self.index = self.indexAt(button.pos())

        # If the index is valid, a row is deleted from the external database,
        # and the screen is refreshed
        if self.index.isValid():
            self.database.delete_task(self.index.row())
            self.refresh()

    def edit_button_clicked(self):
        """Give the user the option to edit a task from the database."""

        # Gets the index of the to be edited row
        button = self.sender()
        self.index = self.indexAt(button.pos())

        # If the input is valid, a pop-up will appear
        if self.index.isValid():
            pop_up = QtWidgets.QMessageBox()

            # Creates buttons on the pop-up to specify which part should be edited
            pop_up.addButton(pop_up.Ok)
            title = pop_up.addButton('Edit title', pop_up.ActionRole)
            time_taken = pop_up.addButton('Edit the estimated time', pop_up.ActionRole)
            priority = pop_up.addButton('Priority of the task', pop_up.ActionRole)
            periodic = pop_up.addButton('Periodicity of the task', pop_up.ActionRole)
            preferred_time = pop_up.addButton('Preferred time of the task', pop_up.ActionRole)

            title.clicked.connect(self.edit_title)
            time_taken.clicked.connect(self.edit_time_taken)
            priority.clicked.connect(self.edit_priority)
            periodic.clicked.connect(self.edit_periodic)
            preferred_time.clicked.connect(self.edit_preferred_time)

            # Launches the pop-up and refreshes the screen after editing
            pop_up.exec_()
            self.refresh()

    def edit_title(self):
        """Give a pop-up dialog to edit the title."""

        # Creates the pop-up dialog with input line
        text, okay = QtWidgets.QInputDialog.getText(
            self,
            f'Edit task {self.index.row()}',
            f'Current title: {self.database.data.Task[self.index.row()]}')

        # Edits the database after the user finishes the input
        if okay:
            self.database.edit_task(self.index.row(), 'Task', text)

    def edit_time_taken(self):
        """Give a pop-up dialog to edit the estimated time."""

        # Creates a pop-up with a combobox to edit the time
        lst = ['5 min', '10 min', '15 min', '20 min', '25 min', '30 min']
        sol = QtWidgets.QInputDialog()
        sol.setComboBoxItems(lst)
        text, okay = sol.getItem(
            self,
            f'Edit estimated time taken for "{self.database.data.Task[self.index.row()]}"',
            f'Current time: {self.database.data.iloc[self.index.row()][1]} min',
            lst,
            editable=False)

        # Edits the database after selection of a time
        if okay:
            self.database.edit_task(self.index.row(), 'Estimated time (minutes)', text[:-4])

    def edit_priority(self):
        """Give a pop-up dialog to edit the priority."""

        # Creates a pop-up with a combobox to edit the priority
        lst = ['low', 'normal', 'high', 'must be done today']
        sol = QtWidgets.QInputDialog()
        sol.setComboBoxItems(lst)
        text, okay = sol.getItem(
            self,
            f'Edit the priority of: "{self.database.data.Task[self.index.row()]}"',
            f'Current priority: {self.database.data.iloc[self.index.row()][2]}',
            lst,
            editable=False)

        # Edits the database after selection of a priority
        if okay:
            self.database.edit_task(self.index.row(), 'Priority', text)

    def edit_periodic(self):
        """Give a pop-up dialog to edit the periodicity."""

        # Creates a pop-up with a combobox to edit if the task is periodic
        lst = ['max once a day', 'several times a day', 'not periodic']
        sol = QtWidgets.QInputDialog()
        sol.setComboBoxItems(lst)
        text, okay = sol.getItem(
            self,
            f'Edit the periodicity of: "{self.database.data.Task[self.index.row()]}"',
            f'The current periodicity: {self.database.data.iloc[self.index.row()][3]}',
            lst,
            editable=False)

        # Edits the database after selection of True or False
        if okay:
            self.database.edit_task(self.index.row(), 'Periodic', text)

    def edit_preferred_time(self):
        """Give a pop-up dialog to edit the preferred time frame."""

        # Creates a pop-up with a combobox to edit the preferred time
        lst = ['Whole day', 'Morning', 'Afternoon', 'Evening']
        sol = QtWidgets.QInputDialog()
        sol.setComboBoxItems(lst)
        text, okay = sol.getItem(
            self,
            f'Edit the preferred time of: "{self.database.data.Task[self.index.row()]}"',
            f'Current preferred time: {self.database.data.iloc[self.index.row()][4]}',
            lst,
            editable=False)

        # Edits the database after selection of a preferred time
        if okay:
            self.database.edit_task(self.index.row(), 'Preferred time', text)

    def refresh(self):
        """Refresh the screen, by creating it again."""

        # Creates the table for the database
        self.model = TaskListDatabase(self.database.data)
        self.setModel(self.model)
        header = self.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        # Creates the delete and edit buttons on every row
        for index in range(len(self.database.data.index)):
            delete_button = QtWidgets.QPushButton('Delete', self)
            self.setIndexWidget(self.model.index(index, 5), delete_button)
            delete_button.clicked.connect(self.delete_button_clicked)

            edit_button = QtWidgets.QPushButton('Edit', self)
            self.setIndexWidget(self.model.index(index, 6), edit_button)
            edit_button.clicked.connect(self.edit_button_clicked)

    def add_task(self, task):
        self.database.add_task(task)
        self.refresh()


class TaskListDatabase(QAbstractTableModel):
    """This class creates the visualisation of the database in the PyQT5 application"""

    def __init__(self, database):
        QAbstractTableModel.__init__(self)
        self._database = database

    def rowCount(self, _parent=None):
        """Return the amount of rows."""
        return len(self._database.index)

    def columnCount(self, _parent=None):
        """Return the amount of columns."""
        return len(self._database.columns)

    def data(self, index, role=Qt.DisplayRole):
        """Fill the empty table with values."""
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._database.iloc[index.row(), index.column()])
        return None

    def headerData(self, col, orientation, role=Qt.DisplayRole):
        """Set the column names."""
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._database.columns[col]
        return None

    @property
    def database(self):
        """Return the database."""
        return self._database
