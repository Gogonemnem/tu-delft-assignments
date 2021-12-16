import pandas as pd
from PyQt6.QtWidgets import (QComboBox, QHeaderView, QMainWindow, QPushButton,
                             QRadioButton, QTableView, QTabWidget)

from project.dataframe_model import DataFrameModel
from project.individual import Individual
from project.input import Input
from project.yfinancecrypto import apply_indicators, apply_signals

column_names = ['Ticker', 'Name', 'Price', 'Advice']
assets = [['AAPL', 'Apple Inc.', '100', 'hold'], ['AMZN', 'Amazon.com, Inc.', '100', 'hold']]
df = pd.DataFrame(assets, columns = column_names)


class Overview:
    def __init__(self, main_window: QMainWindow, input_tab: Input):
        self.main_window = main_window
        self.input = input_tab

        self.button: QPushButton = self.main_window.findChild(QPushButton, "calculate_button")
        self.button.clicked.connect(self.calculate_advices)

        # this lambda function seems necessary, I think that it has to do with
        # Python not 'compiling' the function at run-time.
        # We could not find another fix
        # pylint: disable=unnecessary-lambda
        self.confirm: QPushButton = self.main_window.findChild(QPushButton, "Confirm_button")
        self.confirm.clicked.connect(lambda: self.calculate_advices())

        self.view_stock: QTableView = self.main_window.findChild(QTableView, "tableView_stock")
        self.view_crypto: QTableView = self.main_window.findChild(QTableView, "tableView_crypto")

        self.model_stock = DataFrameModel()
        self.model_crypto = DataFrameModel()

        self.view_stock.setModel(self.model_stock)
        self.view_crypto.setModel(self.model_crypto)

        header_stock = self.view_stock.horizontalHeader()
        header_stock.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        header_crypto = self.view_crypto.horizontalHeader()
        header_crypto.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        results_button: QPushButton = self.main_window.findChild(QPushButton, "results_button")
        results_button.clicked.connect(self.get_results)

    def set_dataframes(self):
        dataframe = self.input.model.dataFrame

        self.model_stock.setDataFrame(dataframe)
        self.model_crypto.setDataFrame(dataframe)

        print(dataframe.loc[:, 'Symbol'].tolist())

        first_select: QComboBox = self.main_window.findChild(QComboBox, "first_select")
        second_select = self.main_window.findChild(QComboBox, "second_select")

        first_select.clear()
        second_select.clear()
        first_select.addItems(dataframe.loc[:, 'Symbol'].tolist())
        second_select.addItems(dataframe.loc[:, 'Symbol'].tolist())

    def calculate_advices(self):
        tab: QTabWidget = self.main_window.findChild(QTabWidget, "tabWidget")
        tab.setCurrentIndex(1)

        self.set_dataframes()

        # ADD methods to add prices
        # ADD advices

    def get_results(self):
        single_button: QRadioButton = self.main_window.findChild(QRadioButton, "single_button")
        compare_button: QRadioButton = self.main_window.findChild(QRadioButton, "compare_button")

        if single_button.isChecked():
            first_select: QComboBox = self.main_window.findChild(QComboBox, "first_select")
            symbol = first_select.currentText()

            if symbol:

                # this is temporary, needs to be changed in overview-back
                interval = '1d'
                data = apply_indicators(symbol)
                advice = apply_signals(data, symbol)
                Individual(self.main_window, data, advice, symbol, interval)

                tab: QTabWidget = self.main_window.findChild(QTabWidget, "tabWidget")
                tab.setCurrentIndex(2)


        elif compare_button.isChecked():
            first_select: QComboBox = self.main_window.findChild(QComboBox, "first_select")
            first_select.currentText()
            second_select: QComboBox = self.main_window.findChild(QComboBox, "second_select")
            second_select.currentText()

            # finish this when comparison is done!



# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     Window = Input()
#     Window.show()
#     app.exec()
