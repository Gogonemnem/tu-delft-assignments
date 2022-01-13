import pandas as pd
import yfinance as yf
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QApplication, QHeaderView, QLineEdit, QMainWindow,
                             QMessageBox, QPushButton, QTableView)

from dataframe_model import DataFrameModel


class Input:
    def __init__(self, main_window: QMainWindow, df=pd.DataFrame(columns=['Symbol', 'Name'])):
        self.main_window = main_window
        self.view: QTableView = self.main_window.findChild(QTableView, "tableView")

        self.model = DataFrameModel(df)
        self.view.setModel(self.model)
        self.view.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)

        self.remove_rows_button = self.main_window.findChild(QPushButton, "remove_selected_button")
        self.remove_rows_button.clicked.connect(self.remove_rows)

        insert = self.main_window.findChild(QLineEdit, "insert")
        insert_button = self.main_window.findChild(QPushButton, "insert_button")
        insert.returnPressed.connect(self.append_ticker)
        insert_button.clicked.connect(self.append_ticker)

        self.save_button = self.main_window.findChild(QPushButton, "save_button")
        self.save_button.clicked.connect(self.export)

        self.import_button = self.main_window.findChild(QPushButton, "import_button")
        self.import_button.clicked.connect(self.import_csv)

        header = self.view.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

    def append_ticker(self):
        line_edit: QLineEdit = self.main_window.findChild(QLineEdit, "insert")
        text = line_edit.text().upper()
        line_edit.clear()
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)

        all_tickers = [ticker.upper() for ticker in self.model.dataFrame.Symbol]
        information = yf.Ticker(text).info

        if text != '' and information['regularMarketPrice'] is not None: # check if company exists
            if text not in all_tickers:
                full_name = ''
                for key in information:
                    if 'ame' in key:
                        full_name = information[key]
                        break
                sector = 'Cryptocurrency' if text.endswith('-USD') else information['sector']
                self.model.insertRow([text, full_name, sector])
                QApplication.restoreOverrideCursor()
            else:
                QApplication.restoreOverrideCursor()
                self.show_pop_up('Something went wrong',
                                 f'Ticker {text} is already in the list')
        else:
            QApplication.restoreOverrideCursor()
            self.show_pop_up('Something went wrong',
                             f'Ticker {text} is not in our system. ' \
                             'Please check Yahoo Finance for the right ticker and try again.')

    def remove_rows(self):

        rows = [row.row() for row in self.view.selectionModel().selectedRows()]

        # if not rows:
        #     rows = range(self.model.rowCount())

        for row in reversed(rows):
            self.model.removeRow(row)

        if not rows:
            self.show_pop_up('Nothing to delete', 'No tickers were selected')

    def show_pop_up(self, title, message):
        QMessageBox.about(self.main_window, title, message)

    def export(self):
        self.model.dataFrame.to_csv('export.csv', index=False)
        self.show_pop_up("Pop-up", "Table has been saved.")

    def import_csv(self):
        try:
            df_imported = pd.read_csv("export.csv")
            self.model.setDataFrame(df_imported)
        except FileNotFoundError:
            self.show_pop_up("Pop-up", "File not found.")


# if __name__ == "__main__":
#     column_names = ['Symbol', 'Name']
#     assets = [['AAPL', 'Apple Inc.'], ['AMZN', 'Amazon.com, Inc.'], \
#             ['TSLA', 'Tesla, Inc.'], ['FB', 'Meta Platforms, Inc.'], \
#             ['Test', 'TEST'], ['LALA', 'LA'], ['CH', 'CHECK']]
#     df = pd.DataFrame(assets, columns = column_names)

#     app = QApplication(sys.argv)
#     Window = Input()
#     Window.show()
#     app.exec()
