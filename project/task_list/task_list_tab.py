from PyQt5 import QtWidgets
from PyQt5 import QtCore
from project.task_list.database_task_list import TaskListDatabase
from project.task_list.data_for_database import TaskList


class TaskListTab(QtWidgets.QTableView):
    """This class creates the task list tab and visualizes it."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.database = None
        self.model = None
        self.delete_button = None
        self.index = None
        self.edit_button = None  # those five self.statements aren't needed but pycharm is annoying

        # Visualise the database, including the delete and edit buttons
        self.refresh()

        # Creates a button to manually refresh the table
        layout = QtWidgets.QVBoxLayout()
        self.refresh_button = QtWidgets.QPushButton('Update the table')
        layout.addWidget(self.refresh_button, alignment=QtCore.Qt.AlignBottom)
        self.setLayout(layout)
        self.refresh_button.clicked.connect(self.refresh)

    def delete_button_clicked(self):
        """Deletes a row from the database and refreshes the screen"""
        # Updates self.database to make sure it deletes from the most recent version
        self.database = TaskList()

        # Gets the index of the deleted row
        button = self.sender()
        self.index = self.indexAt(button.pos())

        # If the index is valid, a row is deleted from the external database,
        # and the screen is refreshed
        if self.index.isValid():
            self.database.delete_task(self.index.row())
            self.refresh()

    def edit_button_clicked(self):
        """Gives the user the option to edit a task from the database"""
        # Updates self.database to make sure it edits the most recent version
        self.database = TaskList()

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
        """Gives a pop-up dialog to edit the title"""
        # Refreshes the self.database
        self.database = TaskList()

        # Creates the pop-up dialog with input line
        text, okay = QtWidgets.QInputDialog.getText(
            self,
            f'Edit task {self.index.row()}',
            f'Current title: {self.database.data.Task[self.index.row()]}')

        # Edits the database after the user finishes the input
        if okay:
            self.database.edit_task(
                self.index.row(),
                'Task',
                text
            )

    def edit_time_taken(self):
        """Gives a pop-up dialog to edit the estimated time"""
        # Refreshes the self.database
        self.database = TaskList()

        # Creates a pop-up with a combobox to edit the time
        lst = ['5 min', '10 min', '15 min', '30 min']
        sol = QtWidgets.QInputDialog()
        sol.setComboBoxItems(lst)
        output = sol.comboBoxItems()
        text, okay = sol.getItem(
            self,
            f'Edit estimated time taken for "{self.database.data.Task[self.index.row()]}"',
            f'Current time: {self.database.data.iloc[self.index.row()][1]} min',
            output,
            editable=False)

        # Edits the database after selection of a time
        if okay:
            self.database.edit_task(
                self.index.row(),
                'Estimated time (minutes)',
                text[:-4]
            )

    def edit_priority(self):
        """Gives a pop-up dialog to edit the priority"""
        # Refreshes the self.database
        self.database = TaskList()

        # Creates a pop-up with a combobox to edit the priority
        lst = ['low', 'normal', 'high', 'must be done today']
        sol = QtWidgets.QInputDialog()
        sol.setComboBoxItems(lst)
        output = sol.comboBoxItems()
        text, okay = sol.getItem(
            self,
            f'Edit the priority of: "{self.database.data.Task[self.index.row()]}"',
            f'Current priority: {self.database.data.iloc[self.index.row()][2]}',
            output,
            editable=False)

        # Edits the database after selection of a priority
        if okay:
            self.database.edit_task(
                self.index.row(),
                'Priority',
                text
            )

    def edit_periodic(self):
        """Gives a pop-up dialog to edit the periodicity"""
        # Refreshes the self.database
        self.database = TaskList()

        # Creates a pop-up with a combobox to edit if the task is periodic
        lst = ['True', 'False']
        sol = QtWidgets.QInputDialog()
        sol.setComboBoxItems(lst)
        output = sol.comboBoxItems()
        text, okay = sol.getItem(
            self,
            f'Edit the periodicity of: "{self.database.data.Task[self.index.row()]}"',
            f'Is the current task periodic?: {self.database.data.iloc[self.index.row()][3]}',
            output,
            editable=False)

        # Edits the database after selection of True or False
        if okay:
            self.database.edit_task(
                self.index.row(),
                'Periodic',
                text
            )

    def edit_preferred_time(self):
        """Gives a pop-up dialog to edit the preferred time frame"""
        # Refreshes the self.database
        self.database = TaskList()

        # Creates a pop-up with a combobox to edit the preferred time
        lst = ['Whole day', 'Morning', 'Afternoon', 'Evening']
        sol = QtWidgets.QInputDialog()
        sol.setComboBoxItems(lst)
        output = sol.comboBoxItems()
        text, okay = sol.getItem(
            self,
            f'Edit the preferred time of: "{self.database.data.Task[self.index.row()]}"',
            f'Current preferred time: {self.database.data.iloc[self.index.row()][4]}',
            output,
            editable=False)

        # Edits the database after selection of a preferred time
        if okay:
            self.database.edit_task(
                self.index.row(),
                'Preferred time',
                text
            )

    def refresh(self):
        """Refreshes the screen, by creating it again"""
        # Refreshes the self.database
        self.database = TaskList()

        # Creates the table for the database
        self.model = TaskListDatabase(self.database.data)
        self.setModel(self.model)
        self.resizeColumnsToContents()
        # self.horizontalHeader().setMinimumSectionSize(250)

        header = self.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        # Creates the delete and edit buttons on every row
        for index in range(len(self.database.data.index)):
            self.delete_button = QtWidgets.QPushButton('Delete')
            self.setIndexWidget(self.model.index(index, 5), self.delete_button)
            self.delete_button.clicked.connect(self.delete_button_clicked)

            self.edit_button = QtWidgets.QPushButton('Edit')
            self.setIndexWidget(self.model.index(index, 6), self.edit_button)
            self.edit_button.clicked.connect(self.edit_button_clicked)
