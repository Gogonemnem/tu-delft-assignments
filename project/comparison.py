import pandas as pd
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWidgets import QHeaderView, QLabel, QMainWindow, QTableView

from dataframe_model import DataFrameModel
from graphdesigner import GraphDesigner

pd.options.mode.chained_assignment = None  # default='warn'


class Comparison:
    def __init__(self, main_window: QMainWindow, dataframe1: pd.DataFrame,
                 advice1: pd.DataFrame, symbol1, dataframe2: pd.DataFrame,
                 advice2: pd.DataFrame, symbol2,  interval):

        self.main_window = main_window
        self.first = symbol1
        self.second = symbol2
        self.interval = interval

        dataframe1 = dataframe1.droplevel(0, axis=1)
        self.dataframe1 = dataframe1
        self.advice1 = advice1
        self.price_df1 = dataframe1[[
            'High', 'Low', 'Close', 'Volume']].round(3)

        dataframe2 = dataframe2.droplevel(0, axis=1)
        self.dataframe2 = dataframe2
        self.advice2 = advice2
        self.price_df2 = dataframe2[[
            'High', 'Low', 'Close', 'Volume']].round(3)

        self.set_labels()

        self.set_tables()

        self.set_graphs()

    def set_labels(self):
        self.main_window.findChild(QLabel, "comp_interval_1").setText(self.interval)
        self.main_window.findChild(QLabel, "comp_interval_2").setText(self.interval)
        self.main_window.findChild(QLabel, "comp_symbol_1").setText(self.first)
        self.main_window.findChild(QLabel, "comp_symbol_2").setText(self.second)


    def set_tables(self):
        model = DataFrameModel(self.price_df1)
        model_2 = DataFrameModel(self.price_df2)
        indicator_model = DataFrameModel(self.advice1)
        indicator_model_2 = DataFrameModel(self.advice2)

        view_p1 = self.main_window.findChild(QTableView, 'price_1')
        view_p2 = self.main_window.findChild(QTableView, 'price_2')
        view_i1 = self.main_window.findChild(QTableView, 'indicator_1')
        view_i2 = self.main_window.findChild(QTableView, 'indicator_2')

        view_p1.setModel(model)
        view_p2.setModel(model_2)
        view_i1.setModel(indicator_model)
        view_i2.setModel(indicator_model_2)

        horizontal_header_i1 = view_i1.horizontalHeader()
        vertical_header_i1 = view_i1.verticalHeader()
        horizontal_header_i1.setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch)
        vertical_header_i1.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        horizontal_header_i2 = view_i2.horizontalHeader()
        vertical_header_i2 = view_i2.verticalHeader()
        horizontal_header_i2.setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch)
        vertical_header_i2.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        view_p1.resizeRowsToContents()
        view_p2.resizeRowsToContents()

        header_p1 = view_p1.horizontalHeader()
        header_p2 = view_p2.horizontalHeader()

        header_p1.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        header_p2.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)


    def set_graphs(self):
        graph_comparison = self.main_window.findChild(QWebEngineView, 'graph_comparison')
        graph_comparison.setHtml(GraphDesigner
                        .draw_prices(self.dataframe1, self.first, self.dataframe2, self.second)
                        .to_html(include_plotlyjs='cdn'))

        # Indicator comparisons
        indicator_comparison = self.main_window.findChild(QWebEngineView, 'indicator_comparison')
        indicator_comparison.setHtml(GraphDesigner
                            .indicator_chart(self.advice1, self.first, self.advice2, self.second)
                            .to_html(include_plotlyjs='cdn'))


        # set price graphs
        price_left = self.main_window.findChild(QWebEngineView, 'price_left')
        price_left.setHtml(GraphDesigner.show_price(self.price_df1).to_html(
            include_plotlyjs='cdn'))

        price_right = self.main_window.findChild(QWebEngineView, 'price_right')
        price_right.setHtml(GraphDesigner.show_price(self.price_df2).to_html(
            include_plotlyjs='cdn'))


# if __name__ == "__main__":
#     import sys
#     from project import yfinancecrypto
#     df, indicators = yfinancecrypto.main('BTC-USD')
#     df2, indicators_2 = yfinancecrypto.main('ETH-USD')


#     full_df = df
#     small_df = df[['High', 'Low', 'Close', 'Volume']]
#     small_df = small_df.round(3)

#     small_df2 = df2[['High', 'Low', 'Close', 'Volume']]
#     small_df2 = small_df2.round(3)

#     app = QApplication(sys.argv)
#     Window = Comparison()
#     Window.showMaximized()
#     app.exec()
