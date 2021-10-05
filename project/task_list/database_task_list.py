from PyQt5.QtCore import QAbstractTableModel, Qt


class TaskListDatabase(QAbstractTableModel):

    def __init__(self, database):
        QAbstractTableModel.__init__(self)
        self._database = database

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

    def removeRow(self, row, parent=None):
        return True

    @property
    def database(self):
        return self._database
