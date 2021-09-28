from PyQt5 import QtWidgets
# from PyQt5.QtGui import QStandardItemModel
# import pandas as pd
# from PyQt5 import QtCore
from project.task_list.database_task_list import TaskListDatabase
from project.task_list.data_for_database import TaskList


class TaskListTab(QtWidgets.QTableView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model = None
        self.delete_button = None
        self.edit_button = None  # those three self.statements aren't needed but pycharm is annoying

        self.database = TaskList()
        self.refresh()
        # self.model = TaskListDatabase(self.database.data)
        # self.setModel(self.model)
        # self.resizeColumnsToContents()
        # self.horizontalHeader().setMinimumSectionSize(250)
        # self.horizontalHeader().setStretchLastSection(True)
        #
        # for index in range(len(self.database.data.index)):
        #     self.delete_button = QtWidgets.QPushButton('Delete')
        #     self.setIndexWidget(self.model.index(index, 5), self.delete_button)
        #     self.delete_button.clicked.connect(self.delete_button_clicked)
        #
        #     self.edit_button = QtWidgets.QPushButton('Edit')
        #     self.setIndexWidget(self.model.index(index, 6), self.edit_button)
        #     self.edit_button.clicked.connect(self.edit_button_clicked)

    def delete_button_clicked(self):
        button = self.sender()
        print('the delete button is clicked')
        index = self.indexAt(button.pos())
        if index.isValid():
            print(f'Row {index.row()} is deleted')
            self.database.delete_task(index.row())
            self.refresh()

        # print(self.database.data)

    def edit_button_clicked(self):
        button = self.sender()
        print('the edit button is clicked')
        index = self.indexAt(button.pos())
        if index.isValid():
            print(index.row())
            pop_up = QtWidgets.QMessageBox()
            pop_up.setText(f'You can now edit the following task:\n "{self.database.data.Task[index.row()]}"')
            pop_up.exec_()

            self.refresh()  # must happen at the end, after editing

            # TODO: finish function

            # The text should be able be edited
            # Possibilities:
            # 1. Give a pop-up where you can write data (reuse widget?), from where the original dataframe is edited
            # 2. use the edit possibility from TaskList(), but you can't control the input/ don't know how to store it?
            # 1 is probably easiest.


    def refresh(self):
        self.model = TaskListDatabase(self.database.data)
        self.setModel(self.model)
        self.resizeColumnsToContents()
        self.horizontalHeader().setMinimumSectionSize(250)
        # self.horizontalHeader().setStretchLastSection(True) ## why doesn't this work after refresh?

        for index in range(len(self.database.data.index)):
            self.delete_button = QtWidgets.QPushButton('Delete')
            self.setIndexWidget(self.model.index(index, 5), self.delete_button)
            self.delete_button.clicked.connect(self.delete_button_clicked)

            self.edit_button = QtWidgets.QPushButton('Edit')
            self.setIndexWidget(self.model.index(index, 6), self.edit_button)
            self.edit_button.clicked.connect(self.edit_button_clicked)
