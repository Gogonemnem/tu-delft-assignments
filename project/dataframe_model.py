import numpy as np
import pandas as pd
from PyQt6 import QtCore
from PyQt6.QtCore import QAbstractTableModel, QModelIndex, Qt, QVariant
from PyQt6.QtWidgets import (QApplication, QDoubleSpinBox, QGridLayout,
                             QPushButton, QSpinBox, QStyledItemDelegate,
                             QTableView, QWidget)


# Forked from these sites
# https://www.pythonguis.com/tutorials/pyqt6-qtableview-modelviews-numpy-pandas/
# https://www.stackoverflow.com/questions/55790561/how-to-remove-data-from-excel-file-displayed-in-pyqt5-and-refresh-it
class FloatDelegate(QStyledItemDelegate):
    @property
    def decimals(self):
        if not hasattr(self, "_decimals"):
            self._decimals = 2
        return self._decimals

    @decimals.setter
    def decimals(self, decimals):
        self._decimals = decimals

    def createEditor(self, parent, _option, _index):
        DBL_MAX = 1.7976931348623157e308
        editor = QDoubleSpinBox(
            parent, minimum=-DBL_MAX, maximum=DBL_MAX, decimals=self.decimals
        )
        return editor

    def setEditorData(self, editor, index):
        editor.setValue(index.data())

    def setModelData(self, editor, model, index):
        model.setData(index, editor.value(), QtCore.Qt.ItemDataRole.DisplayRole)

    def displayText(self, value, _locale):
        return f"{value}"


class DataFrameModel(QAbstractTableModel):
    DtypeRole = Qt.ItemDataRole.UserRole + 1000
    ValueRole = Qt.ItemDataRole.UserRole + 1001

    def __init__(self, df=pd.DataFrame(), parent=None):
        super().__init__(parent)
        self._dataframe: pd.DataFrame = df

    def setDataFrame(self, dataframe):
        self.beginResetModel()
        self._dataframe = dataframe.copy()
        self.endResetModel()

    def dataFrame(self):
        return self._dataframe.copy()

    dataFrame: pd.DataFrame = QtCore.pyqtProperty(
        pd.DataFrame, fget=dataFrame, fset=setDataFrame
    )

    @QtCore.pyqtSlot(int, Qt.Orientation, result=str)
    def headerData(
        self,
        section: int,
        orientation: Qt.Orientation,
        role: int = Qt.ItemDataRole.DisplayRole,
    ):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return self._dataframe.columns[section]
            elif orientation == Qt.Orientation.Vertical:
                return str(self._dataframe.index[section])
        return QVariant()

    def rowCount(self, parent=QModelIndex()):
        if parent.isValid():
            return 0
        return len(self._dataframe.index)

    def columnCount(self, parent=QModelIndex()):
        if parent.isValid():
            return 0
        return self._dataframe.columns.size

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid() or not (
            0 <= index.row() < self.rowCount()
            and 0 <= index.column() < self.columnCount()
        ):
            return QVariant()

        row = self._dataframe.index[index.row()]
        col = self._dataframe.columns[index.column()]
        dtype = self._dataframe[col].dtype

        if isinstance(row, int):
            val = self._dataframe.iloc[row][col]
        else:
            val = str(self._dataframe.loc[row, col])

        if role == Qt.ItemDataRole.DisplayRole:
            return val
        elif role == DataFrameModel.ValueRole:
            return val
        if role == DataFrameModel.DtypeRole:
            return dtype
        return QVariant()

    def setData(self, index, value, _role):
        row = self._dataframe.index[index.row()]
        col = self._dataframe.columns[index.column()]
        if hasattr(value, "toPyObject"):
            # PyQt gets a QVariant
            value = value.toPyObject()
        else:
            # PySide gets an unicode
            dtype = self._dataframe[col].dtype
            if dtype != object:
                value = None if value == "" else dtype.type(value)
        self._dataframe.at[row, col] = value
        return True

    def flags(self, _index):
        flags = (
            QtCore.Qt.ItemFlag.ItemIsSelectable
            | QtCore.Qt.ItemFlag.ItemIsDragEnabled
            # | QtCore.Qt.ItemFlag.ItemIsEditable
            | QtCore.Qt.ItemFlag.ItemIsEnabled
        )
        return flags

    def roleNames(self):
        roles = {
            QtCore.Qt.ItemDataRole.DisplayRole: b"display",
            DataFrameModel.DtypeRole: b"dtype",
            DataFrameModel.ValueRole: b"value",
        }
        return roles

    def insertRow(self, row):
        index = self.rowCount()

        self.beginInsertRows(QtCore.QModelIndex(), index, index)
        self._dataframe.loc[index] = row
        self.endInsertRows()
        return True

    def removeRow(self, row):
        if 0 <= row < self.rowCount():
            self.beginRemoveRows(QtCore.QModelIndex(), row, row)
            self._dataframe.drop([row], inplace=True)
            self._dataframe.reset_index(inplace=True, drop=True)
            self.endRemoveRows()
            return True
        return False

    def removeColumn(self, col):
        if 0 <= col < self.columnCount():
            self.beginRemoveRows(QtCore.QModelIndex(), col, col)
            self._dataframe.drop(
                self._dataframe.columns[[col]], axis=1, inplace=True
            )
            self._dataframe.reset_index(inplace=True, drop=True)
            self.endRemoveColumns()
            return True
        return False

    def sort(self, column, order):
        colname = self._dataframe.columns[column]
        self.layoutAboutToBeChanged.emit()
        self._dataframe.sort_values(
            colname, ascending=order == QtCore.Qt.SortOrder.AscendingOrder, inplace=True
        )
        self._dataframe.reset_index(inplace=True, drop=True)
        self.layoutChanged.emit()


class Widget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        tableview = QTableView()
        tableview.setSortingEnabled(True)
        delegate = FloatDelegate(tableview)
        tableview.setItemDelegate(delegate)
        delegate.decimals = 4
        self.spinbox_row = QSpinBox()
        self.button_row = QPushButton(
            "Delete Row", clicked=self.remove_row
        )
        self.spinbox_col = QSpinBox()
        self.button_col = QPushButton(
            "Delete Column", clicked=self.remove_col
        )

        df = pd.DataFrame(
            np.random.uniform(0, 100, size=(100, 4)), columns=list("ABCD")
        )
        self._model = DataFrameModel(df)

        tableview.setModel(self._model)

        grid = QGridLayout(self)
        grid.addWidget(tableview, 0, 0, 1, 4)
        grid.addWidget(self.spinbox_row, 1, 0)
        grid.addWidget(self.button_row, 1, 1)
        grid.addWidget(self.spinbox_col, 1, 2)
        grid.addWidget(self.button_col, 1, 3)

        self.on_rowChanged()
        self.on_columnChanged()

        self._model.rowsInserted.connect(self.on_rowChanged)
        self._model.rowsRemoved.connect(self.on_rowChanged)
        self._model.columnsInserted.connect(self.on_columnChanged)
        self._model.columnsRemoved.connect(self.on_columnChanged)

    @QtCore.pyqtSlot()
    def on_rowChanged(self):
        self.spinbox_row.setMaximum(self._model.rowCount() - 1)

    @QtCore.pyqtSlot()
    def on_columnChanged(self):
        self.spinbox_col.setMaximum(self._model.columnCount() - 1)

    @QtCore.pyqtSlot()
    def remove_row(self):
        row = self.spinbox_row.value()
        self._model.removeRow(row)

    @QtCore.pyqtSlot()
    def remove_col(self):
        col = self.spinbox_col.value()
        self._model.removeColumn(col)

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    w = Widget()
    w.resize(640, 480)
    w.show()
    sys.exit(app.exec())
