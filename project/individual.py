import pandas as pd
import fear_and_greed
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWidgets import (QFrame, QHeaderView, QLabel,
                             QMainWindow, QTableView)

# from project.yfinancecrypto import apply_indicators, apply_signals
from project.dataframe_model import DataFrameModel


class Individual(QMainWindow):
    def __init__(self, main_window: QMainWindow, dataframe: pd.DataFrame,
                 advice: pd.DataFrame, symbol, interval):

        def draw_graphs():
            def clear_layout(layout):
                if layout is not None:
                    while layout.count():
                        item = layout.takeAt(0)
                        widget = item.widget()
                        if widget is not None:
                            widget.deleteLater()

            price_change_frame = self.main_window.findChild(QFrame, 'price_frame')
            price_change = QWebEngineView(self.main_window)
            price_change.setObjectName('price_change')
            clear_layout(price_change_frame.layout())
            price_change_frame.layout().addWidget(price_change)

            price_change.setHtml(GraphDesigner.show_price(
                self.price_df).to_html(include_plotlyjs='cdn'))

            price_graph_frame = self.main_window.findChild(QFrame, 'price_graph_frame')
            price_graph = QWebEngineView(self.main_window)
            price_graph.setObjectName('price_graph')
            clear_layout(price_graph_frame.layout())
            price_graph_frame.layout().addWidget(price_graph)
            price_graph.setHtml(GraphDesigner.open_graph(
                        self.dataframe, symbol).to_html(include_plotlyjs='cdn'))

            indicator_chart_view = self.main_window.findChild(QFrame, 'indicator_frame')
            indicator_chart = QWebEngineView(self.main_window)
            indicator_chart.setObjectName('indicator_chart')
            clear_layout(indicator_chart_view.layout())
            indicator_chart_view.layout().addWidget(indicator_chart)
            indicator_chart.setHtml(
                GraphDesigner.indicator_chart(advice).to_html(include_plotlyjs='cdn'))

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


class GraphDesigner:
    @staticmethod
    def open_graph(df, symbol):

        def draw_lines(fig, dataframe, symbol):
            df_columns = ['BBM', 'BBU', 'BBL']
            names = ['Middle', 'Upper', 'Lower']
            lines = ['solid', 'dot', 'dash']
            fillstyles = ['none', 'none', 'tonexty']
            fillings = ['#000000', '#000000', 'rgba(0, 191, 255, .2)']
            colors = ['red', 'deepskyblue', 'deepskyblue']

            for column, color, name, line, fillstyle, filling in \
                    zip(df_columns, colors, names, lines, fillstyles, fillings):
                label = f'{symbol} {name}'
                fig.add_trace(
                    go.Scatter(
                        x=dataframe.index,
                        y=dataframe[column],
                        line=dict(color=color, dash=line),
                        name=label,
                        fill=fillstyle,
                        fillcolor=filling
                    ),
                )

        data = df

        fig = make_subplots(
            rows=2,
            cols=1,
            shared_xaxes=True,
            subplot_titles=('IBM', 'Volume'),
            vertical_spacing=0.1,
            row_width=[0.2, 0.7]
        )

        fig.update_layout(
            title=symbol,
            yaxis_title='Price(USD)',
            plot_bgcolor='#3d3d3d'
        )

        fig.update_xaxes(
            rangeslider_visible=False,
            rangeselector=dict(
                buttons=list([dict(step='all')])
            )
        )

        fig.update(layout_xaxis_rangeslider_visible=False)

        fig.add_trace(
            go.Candlestick(
                x=data.index,
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                close=data['Close'],
                name='marketdata',
                increasing_line_color='#ff0000',
                decreasing_line_color='#0bc62a'
            )
        )

        fig.add_trace(
            go.Bar(
                x=df.index,
                y=df['Volume'],
                marker_color='red',
                showlegend=False
            ),
            row=2,
            col=1
        )

        draw_lines(fig, df, symbol)
        return fig

    @staticmethod
    def show_price(small_df):
        fig = go.Figure()

        fig.add_trace(go.Indicator(
            mode="number+delta",
            value=small_df['Close'][-1],
            number={'prefix': "$"},
            delta={'position': "top", 'reference': small_df['Close'][-2]},
            domain={'x': [0, 1], 'y': [0.4, 1]}))
        fig.add_trace(go.Indicator(
            mode="delta",
            value=small_df['Close'][-1],
            delta={'position': "top",
                   'reference': small_df['Close'][-2], 'relative': True},
            domain={'x': [0.0, 1.0], 'y': [0.0, 0.4]}))

        fig.update_layout(
            margin_b=0,
            margin_l=0,
            margin_t=0,
            margin_r=0,
            autosize=True
        )
        return fig

    @staticmethod
    def indicator_chart(advice):
        index = fear_and_greed.get()
        tot = 0
        for signal in advice['Advice']:
            if 'Hold' in signal:
                pass
            if 'Sell' in signal:
                tot -= 1
            if 'Buy' in signal:
                tot += 1

        indicator_fig = go.Indicator(
            mode='gauge',
            value=tot,
            title='Advice',
            domain={'x': [0.0, 0.4], 'y': [0.0, 1]},
            gauge={
                'axis': {'range': [-6, 6],
                         'tickmode': 'array',
                         'tickvals': list(range(-6, 7)),
                         'ticktext': ['Very strong sell' if i == -6
                                      else 'Strong sell' if i == -4
                         else 'Sell' if i == -2
                         else 'Hold' if i == 0
                         else 'Buy' if i == 2
                         else 'Strong buy' if i == 4
                         else 'Very strong buy' if i == 6

                         else '6 - high' if i == 6
                         else '' for i in range(-6, 7)],
                         },
                'bar': {'color': "black"},
                'steps': [
                    {'range': [-6, -3], 'color': '#b00000'},
                    {'range': [-3, 0], 'color': '#eb0000'},
                    {'range': [0, 3], 'color': 'green'},
                    {'range': [3, 6], 'color': 'darkgreen'}]
            })
        fear_and_greed_fig = go.Indicator(
            mode='gauge',
            value=index[0]/25,
            title=index[1],
            domain={'x': [0.6, 1.0], 'y': [0., 1.00]},
            gauge={
                'axis': {'range': [0, 4],
                         'tickmode': 'array',
                         'tickvals': list(range(0, 5)),
                         'ticktext': [
                         'Extreme Fear' if i == 0
                         else 'Fear' if i == 1
                         else 'Greed' if i == 3
                         else 'Extreme greed' if i == 4
                         else '' for i in range(0, 5)
                         ]},
                'bar': {'color': "black"},
                'steps': [
                    {'range': [0, 1], 'color': '#b00000'},
                    {'range': [1, 2], 'color': '#eb0000'},
                    {'range': [2, 3], 'color': 'green'},
                    {'range': [3, 4], 'color': 'darkgreen'}]
            })

        layout = go.Layout(
                   autosize=True,
                   title='Indicator Graph | Fear and ''Greed Graph',
        )

        fig = go.Figure(data=[indicator_fig, fear_and_greed_fig], layout=layout)
        return fig


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
