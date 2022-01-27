# import pandas as pd
from PyQt6.QtWidgets import (QApplication, QComboBox, QHeaderView, QMainWindow, QMenu, QPushButton,
                             QRadioButton, QTableView, QTabWidget)
from PyQt6.QtCore import QPoint, Qt
from PyQt6.QtGui import QAction

from dataframe_model import DataFrameModel, FloatDelegate, FilterProxyModel
from individual import Individual
from input import Input
from comparison import Comparison
from yfinancecrypto import apply_indicators, apply_signals, advice

# column_names = ['Ticker', 'Name', 'Price', 'Advice']
# assets = [['AAPL', 'Apple Inc.', '100', 'hold'], ['AMZN', 'Amazon.com, Inc.', '100', 'hold']]
# df = pd.DataFrame(assets, columns = column_names)

# column_names = ['Ticker', 'Name', 'Price', 'Advice']
# assets_stock = [['AAPL', 'Apple Inc.', '100', 'hold'],
#                 ['AMZN', 'Amazon.com, Inc.', '200', 'very strong buy'],
#                 ['AMZN', 'Amazon.com, Inc.', '200', 'very strong sell'],
#                 ['AMZN', 'Amazon.com, Inc.', '200', 'strong buy']]
# df_stock = pd.DataFrame(assets_stock, columns = column_names)
# assets_crypto= [['AAPL', 'Apple Inc.', '100', 'hold'],
#                 ['AMZN', 'Amazon.com, Inc.', '200', 'very strong buy']]
# df_crypto = pd.DataFrame(assets_crypto, columns = column_names)


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

        delegate_stock = FloatDelegate(self.view_stock)
        self.view_stock.setItemDelegate(delegate_stock)
        self.model_stock = DataFrameModel()

        self.proxy = FilterProxyModel(self.main_window)
        self.proxy.setSourceModel(self.model_stock)

        self.view_stock.setModel(self.proxy)

        self.header_stock = self.view_stock.horizontalHeader()
        self.header_stock.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)


        self.filter_button: QPushButton = self.main_window.findChild(QPushButton, "filter_button")
        self.filter_button.clicked.connect(self.filter)
        # self.header_stock.sectionClicked.connect(self.filter)

        results_button: QPushButton = self.main_window.findChild(QPushButton, "results_button")
        results_button.clicked.connect(self.get_results)


        self.strategy_box = self.main_window.findChild(QComboBox, "strategy_box")
        self.interval_box = self.main_window.findChild(QComboBox, "interval_box")

    def filter(self, logical_index):
        logical_index = 2
        menu = QMenu(self.main_window)

        values = []

        for row in range(self.model_stock.rowCount()):
            value = self.model_stock.index(row, logical_index).data(self.proxy.filterRole())
            values.append(value)

        action_all = QAction("All", self.main_window)
        action_all.setData(None)
        menu.addAction(action_all)
        menu.addSeparator()

        for value in sorted(list(set(values))):
            action = QAction(str(value), self.main_window)
            action.setData(value)
            menu.addAction(action)

        button_pos = self.main_window.mapToGlobal(self.filter_button.pos())
        pos_y = button_pos.y()
        pos_x = button_pos.x()

        action = menu.exec(QPoint(pos_x, pos_y))
        if action is not None:
            self.proxy.setFilterKeyColumn(logical_index)
            self.proxy.filter_value = action.data()

    # The part we wanna keep from previous code
    # def strategy_sort(self):
    #     if self.comboBox_sorting_stocks.currentText() == IETS:
    #         df_stock["Advice"] = pd.Categorical(df_stock['Advice'],
    #             ["very strong buy", "strong buy", "buy", "hold",
    #              "sell", "strong sell", "very strong sell"])
    #         df_stock.sort_values(by='Advice', inplace=True)
    #         self.model_stock = DataFrameModel(df_stock)
    #         self.view_stock.setModel(self.model_stock)

    # Steps we have to implement
    # 1. Calculate new advices
    # 2. Replace old advices with the new advices in dataframe
    # 3. Make sure it is in pd. Categorical so it can be sorted

    def calculate_advices(self):
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        tab: QTabWidget = self.main_window.findChild(QTabWidget, "tabWidget")
        tab.setCurrentIndex(1)

        dataframe = self.input.model.dataFrame

        interval = self.get_interval()

        df_stock = dataframe.copy()
        symbols_stock = df_stock['Symbol'].tolist()
        df_indicators_stock = apply_indicators(symbols_stock, interval)
        df_signals_stock = apply_signals(df_indicators_stock, symbols_stock)

        data_stock = df_indicators_stock.xs('Close', axis=1, level=1).iloc[-1].rename('Price')
        df_stock = df_stock.merge(data_stock, left_on='Symbol', right_index=True)
        df_stock['Advice'] = df_stock['Symbol'].map(advice(df_signals_stock, symbols_stock))
        self.model_stock.setDataFrame(df_stock)

        first_select: QComboBox = self.main_window.findChild(QComboBox, "first_select")
        first_select.clear()
        first_select.addItems(df_stock.loc[:, 'Symbol'].tolist())

        second_select: QComboBox = self.main_window.findChild(QComboBox, "second_select")
        second_select.clear()
        second_select.addItems(df_stock.loc[:, 'Symbol'].tolist())

        results_button: QPushButton = self.main_window.findChild(QPushButton, "results_button")
        results_button.setEnabled(True)

        QApplication.restoreOverrideCursor()

    def get_results(self):
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        single_button: QRadioButton = self.main_window.findChild(QRadioButton, "single_button")
        compare_button: QRadioButton = self.main_window.findChild(QRadioButton, "compare_button")

        if single_button.isChecked():
            first_select: QComboBox = self.main_window.findChild(QComboBox, "first_select")
            symbol = first_select.currentText()

            # this is temporary, needs to be changed in overview-back
            interval = self.get_interval()
            data = apply_indicators([symbol], interval)
            advices = apply_signals(data, [symbol])
            overall_advice = advice(advices, [symbol])
            Individual(self.main_window, data, advices, symbol, interval, overall_advice)

            tab: QTabWidget = self.main_window.findChild(QTabWidget, "tabWidget")
            tab.setCurrentIndex(2)


        elif compare_button.isChecked():
            first_select: QComboBox = self.main_window.findChild(QComboBox, "first_select")
            symbol1 = first_select.currentText()
            second_select: QComboBox = self.main_window.findChild(QComboBox, "second_select")
            symbol2 = second_select.currentText()

            if first_select and second_select:
                # this is temporary, needs to be changed in overview-back
                interval = self.get_interval()
                data1 = apply_indicators([symbol1], interval)
                advice1 = apply_signals(data1, [symbol1])
                data2 = apply_indicators([symbol2], interval)
                advice2 = apply_signals(data2, [symbol2])
                overall_advice1 = advice(advice1, [symbol1])
                overall_advice2 = advice(advice2, [symbol2])
                Comparison(self.main_window, data1, advice1, symbol1,
                           data2, advice2, symbol2, interval, overall_advice1, overall_advice2)

                tab: QTabWidget = self.main_window.findChild(QTabWidget, "tabWidget")
                tab.setCurrentIndex(3)

        QApplication.restoreOverrideCursor()


    def get_interval(self):
        interval_labels = {
        '1 minute': '1m',
        '5 minutes': '5m',
        '15 minutes':'15m',
        '30 minutes':'30m',
        '1 hour': '1h',
        '1 day': '1d',
        '1 week': '1wk',
        '1 month': '1mo',
        }
        interval_box: QComboBox = self.main_window.findChild(QComboBox, "interval_box")

        # could also get currentindex for a miniscule efficiency increase
        return interval_labels[interval_box.currentText()]


# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     Window = Input()
#     Window.show()
#     app.exec()
