from PyQt5 import QtWidgets
from PyQt5 import QtCore
from project.task_list.database_task_list import TaskListDatabase
from project.task_list.data_for_database import TaskList
from project.individual_task.individual_task_widget import TaskWidget


class TaskListTab(QtWidgets.QTableView):
    """This class creates the task list tab and visualizes it."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.database = None
        self.model = None
        self.delete_button = None
        self.index = None
        self.edit_button = None  # those five self.statements aren't needed but pycharm is annoying
        self.task = TaskWidget()
        self.refresh()

        layout = QtWidgets.QVBoxLayout()
        self.refresh_button = QtWidgets.QPushButton('Update the table')
        layout.addWidget(self.refresh_button, alignment=QtCore.Qt.AlignBottom)
        self.setLayout(layout)
        self.refresh_button.clicked.connect(self.refresh)

    def delete_button_clicked(self):
        self.database = TaskList()
        button = self.sender()
        print('the delete button is clicked')
        self.index = self.indexAt(button.pos())
        if self.index.isValid():
            print(f'Row {self.index.row()} is deleted')
            self.database.delete_task(self.index.row())
            self.refresh()

    def edit_button_clicked(self):
        self.database = TaskList()
        button = self.sender()
        print('the edit button is clicked')
        self.index = self.indexAt(button.pos())
        if self.index.isValid():
            print(f'The following will be edited: {self.index.row()}')

            pop_up = QtWidgets.QMessageBox()

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

            pop_up.exec_()

            self.refresh()

    def edit_title(self):
        self.database = TaskList()
        text, ok = QtWidgets.QInputDialog.getText(
            self,
            f'Edit task {self.index.row()}',
            f'Current title: {self.database.data.Task[self.index.row()]}')
        if ok:
            print(f'This is the new input: {text}')  # to check the input
            self.database.edit_task(
                self.index.row(),
                'Task',
                text
            )

    def edit_time_taken(self):
        self.database = TaskList()
        lst = ['5 min', '10 min', '15 min', '30 min']
        sol = QtWidgets.QInputDialog()
        sol.setComboBoxItems(lst)
        output = sol.comboBoxItems()
        text, ok = sol.getItem(
            self,
            f'Edit estimated time taken for "{self.database.data.Task[self.index.row()]}"',
            f'Current time: {self.database.data.iloc[self.index.row()][1]} min',
            output,
            editable=False)
        if ok:
            print(f'This is the new input: {text}')
            self.database.edit_task(
                self.index.row(),
                'Estimated time (minutes)',
                text[:-4]
            )

    def edit_priority(self):
        self.database = TaskList()
        lst = ['low', 'normal', 'high', 'must be done today']
        sol = QtWidgets.QInputDialog()
        sol.setComboBoxItems(lst)
        output = sol.comboBoxItems()
        text, ok = sol.getItem(
            self,
            f'Edit the priority of: "{self.database.data.Task[self.index.row()]}"',
            f'Current priority: {self.database.data.iloc[self.index.row()][2]}',
            output,
            editable=False)
        if ok:
            print(f'This is the new input: {text}')
            self.database.edit_task(
                self.index.row(),
                'Priority',
                text
            )

    def edit_periodic(self):
        self.database = TaskList()
        lst = ['True', 'False']
        sol = QtWidgets.QInputDialog()
        sol.setComboBoxItems(lst)
        output = sol.comboBoxItems()
        text, ok = sol.getItem(
            self,
            f'Edit the periodicity of: "{self.database.data.Task[self.index.row()]}"',
            f'Is the current task periodic?: {self.database.data.iloc[self.index.row()][3]}',
            output,
            editable=False)
        if ok:
            print(f'This is the new input: {text}')
            self.database.edit_task(
                self.index.row(),
                'Periodic',
                text
            )

    def edit_preferred_time(self):
        self.database = TaskList()
        lst = ['Whole day', 'Morning', 'Afternoon', 'Evening']
        sol = QtWidgets.QInputDialog()
        sol.setComboBoxItems(lst)
        output = sol.comboBoxItems()
        text, ok = sol.getItem(
            self,
            f'Edit the preferred time of: "{self.database.data.Task[self.index.row()]}"',
            f'Current preferred time: {self.database.data.iloc[self.index.row()][4]}',
            output,
            editable=False)
        if ok:
            print(f'This is the new input: {text}')
            self.database.edit_task(
                self.index.row(),
                'Preferred time',
                text
            )

    def refresh(self):
        self.database = TaskList()
        self.model = TaskListDatabase(self.database.data)
        self.setModel(self.model)
        self.resizeColumnsToContents()
        self.horizontalHeader().setMinimumSectionSize(250)

        for index in range(len(self.database.data.index)):
            self.delete_button = QtWidgets.QPushButton('Delete')
            self.setIndexWidget(self.model.index(index, 5), self.delete_button)
            self.delete_button.clicked.connect(self.delete_button_clicked)

            self.edit_button = QtWidgets.QPushButton('Edit')
            self.setIndexWidget(self.model.index(index, 6), self.edit_button)
            self.edit_button.clicked.connect(self.edit_button_clicked)
