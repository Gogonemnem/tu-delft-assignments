from PyQt5.QtCore import QAbstractTableModel, Qt


class TaskListDatabase(QAbstractTableModel):
    """This class creates the visualisation of the database in the PyQT5 application"""

    def __init__(self, database):
        QAbstractTableModel.__init__(self)
        self._database = database

    # add underscore as it is not used,
    # so that pylint will not warn us about unused arguments
    def rowCount(self, _parent=None):
        """Returns the amount of rows"""
        return len(self._database.index)

    def columnCount(self, _parent=None):
        """Returns the amount of columns"""
        return len(self._database.columns)

    def data(self, index, role=Qt.DisplayRole):
        """Fills the empty table with values"""
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._database.iloc[index.row(), index.column()])
        return None

    def headerData(self, col, orientation, role=Qt.DisplayRole):
        """Sets the column names"""
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._database.columns[col]
        return None

    @property
    def database(self):
        """Returns the database"""
        return self._database
