from PyQt5.QtCore import QAbstractTableModel, Qt


class TaskListDatabase(QAbstractTableModel):

    def __init__(self, database):
        QAbstractTableModel.__init__(self)
        self._database = database

    # Is it possible to do this without overriding these methods?
    # Pylint doesn't like them, but I (Gonem) added manual exceptions in the config file
    # I also deleted the parent=None in rowCount and columnCount

    # Added it back again
    def rowCount(self, parent=None):
        return len(self._database.index)

    def columnCount(self, parent=None):
        return len(self._database.columns)

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._database.iloc[index.row(), index.column()])
        return None

    def headerData(self, col, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._database.columns[col]
        return None

    @property
    def database(self):
        return self._database


# The beneath code gives the option to manually edit the table.
# I don't know if it changes the database,
# but I think it can break the rest of the code if we allow it.

    # def flags(self, index):
    #     return Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable

    # def setData(self, index, value, role):
    #     if role == Qt.EditRole:
    #         self._database.iloc[index.row(), index.column()] = value
    #         return True
    #
    # def data(self, index, role=Qt.DisplayRole):
    #     if index.isValid():
    #         if role == Qt.DisplayRole or role == Qt.EditRole:
    #             value = self._database.iloc[index.row(), index.column()]
    #             return str(value)
