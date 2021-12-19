import pandas as pd
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWidgets import QHeaderView, QLabel, QMainWindow, QTableView

from project.dataframe_model import DataFrameModel
from project.graphdesigner import GraphDesigner


class Individual:
    def __init__(self, main_window: QMainWindow, dataframe: pd.DataFrame,
                 advice: pd.DataFrame, symbol, interval):

        def draw_graphs():
            price_change = self.main_window.findChild(QWebEngineView, 'price_change')
            price_graph = self.main_window.findChild(QWebEngineView, 'price_graph')
            indicator_chart = self.main_window.findChild(QWebEngineView, 'indicator_chart')

            price_change.setHtml(GraphDesigner.show_price(
                self.price_df).to_html(include_plotlyjs='cdn'))

            price_graph.setHtml(GraphDesigner.draw_prices(
                        self.dataframe, symbol).to_html(include_plotlyjs='cdn'))

            indicator_chart.setHtml(
                GraphDesigner.indicator_chart(advice, symbol).to_html(include_plotlyjs='cdn'))

        self.main_window = main_window

        self.dataframe = dataframe
        self.advice = advice
        self.price_df = dataframe[['High', 'Low', 'Close', 'Volume']].round(3)

        # Prices Dataframe
        model = DataFrameModel(self.price_df)
        view: QTableView = self.main_window.findChild(QTableView, 'price_table')
        view.setModel(model)
        view.resizeRowsToContents()
        header = view.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # Advice Dataframe
        model2 = DataFrameModel(self.advice)
        advice_view: QTableView = self.main_window.findChild(QTableView, 'tableView_2')
        advice_view.setModel(model2)
        advice_view.resizeRowsToContents()
        horizontal_header = advice_view.horizontalHeader()
        vertical_header = advice_view.verticalHeader()
        horizontal_header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        vertical_header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        symbol_label = self.main_window.findChild(QLabel, "symbol_label")
        symbol_label.setText(symbol)

        interval_label = self.main_window.findChild(QLabel, "interval_label")
        interval_label.setText(interval)

        draw_graphs()


# # main method, because we dont want accidental global variables.
# def main():
#     symbol = 'BTC-USD'
#     interval = '1d'

#     pd.options.mode.chained_assignment = None  # default='warn'

#     # ADVICES:
#     df = apply_indicators(symbol)
#     advice = apply_signals(df, symbol)

#     app = QApplication(sys.argv)
#     window = Individual(df, advice, symbol, interval)
#     window.showMaximized()
#     app.exec()

#     return advice


if __name__ == "__main__":
    raise Exception("De executie is verplaatst naar main.py")
    # import sys

    # main()
