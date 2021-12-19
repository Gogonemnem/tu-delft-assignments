import fear_and_greed
import plotly.graph_objs as go
from plotly.subplots import make_subplots
class GraphDesigner:
    @staticmethod
    def draw_prices(df, symbol, df2=None, symbol_2=None):
        if df2 is not None:
            secondary = True
            title = f'Comparison between {symbol} and {symbol_2}'

        else:
            secondary = False
            title = symbol

        fig = make_subplots(
            rows=2,
            cols=1,
            shared_xaxes=True,
            subplot_titles=('IBM', 'Volume'),
            vertical_spacing=0.1,
            row_width=[0.2, 0.7],
            specs=[[{"secondary_y": secondary}], [{"secondary_y": secondary}]],
        )

        fig.update_layout(
            title=title,
            yaxis_title='Price(USD)',
            plot_bgcolor='#3d3d3d',
            barmode='stack', # not sure what it does
            margin_b=0,
            margin_l=0,
            margin_t=0,
            margin_r=0,
            autosize=True
        )

        fig.update_yaxes(title_text=f'{symbol} Price(USD)', secondary_y=False)
        if df2 is not None:
            fig.update_yaxes(title_text=f'{symbol_2} Price(USD)', secondary_y=True) ##

        fig.update_xaxes(
            rangeslider_visible=False,
            rangeselector=dict(
                buttons=list([dict(step='all')])
            )
        )

        if df2 is not None:
            GraphDesigner.draw_volume(fig, df2, symbol_2, secondary=True)

        GraphDesigner.draw_volume(fig, df, symbol)

        if df2 is not None:
            GraphDesigner.draw_range(fig, df2, symbol_2, secondary=True)
            GraphDesigner.draw_historical_line(fig, df2, symbol_2, secondary=True)

        GraphDesigner.draw_range(fig, df, symbol)

        if df2 is not None:
            GraphDesigner.draw_historical_line(fig, df, symbol)
        else:
            GraphDesigner.draw_historical_candle(fig, df, symbol)
        return fig

    @staticmethod
    def draw_historical_candle(fig, dataframe, symbol, secondary=False):
        colors_up = ['#ff0000', 'green']
        colors_down = ['#0bc62a', 'red']

        fig.add_trace(
            go.Candlestick(
                x=dataframe.index,
                open=dataframe['Open'],
                high=dataframe['High'],
                low=dataframe['Low'],
                close=dataframe['Close'],
                name=f'{symbol} marketdata',
                increasing_line_color= colors_up[secondary],
                decreasing_line_color= colors_down[secondary]
            )
        )
        return fig

    @staticmethod
    def draw_historical_line(fig, dataframe, symbol, secondary=False):
        colors = ['aliceblue', 'mistyrose']

        label = f'{symbol} Price'
        fig.add_trace(
            go.Scatter(
                x=dataframe.index,
                y=dataframe['Close'],
                line=dict(color=colors[secondary]),
                name=label
            ),
            secondary_y=secondary
        )
        return fig

    @staticmethod
    def draw_range(fig, dataframe, symbol, secondary=False):
        df_columns = ['BBM', 'BBU', 'BBL']
        names = ['Middle', 'Upper', 'Lower']
        lines = ['solid', 'dot', 'dash']
        fillstyles = ['none', 'none', 'tonexty']
        colors = [['cyan', 'magenta'], ['deepskyblue', 'deeppink'], ['deepskyblue', 'deeppink']]
        fillings = [['#000000', '#000000'],
                    ['#000000', '#000000'],
                    ['rgba(0, 191, 255, .2)', 'rgba(228, 113, 122, .2)']]

        for column, color, name, line, fillstyle, filling in \
            zip(df_columns, colors, names, lines, fillstyles, fillings):
            label = f'{symbol} {name}'
            fig.add_trace(
                go.Scatter(
                    x=dataframe.index,
                    y=dataframe[column],
                    line=dict(color=color[secondary], dash=line),
                    name=label,
                    fill=fillstyle,
                    fillcolor=filling[secondary]
                ),
                secondary_y=secondary
                )
        return fig

    @staticmethod
    def draw_volume(fig, dataframe, symbol, secondary=False):
        fig.update_yaxes(title_text=f'{symbol} Volume', secondary_y=secondary, row=2, col=1)
        # fig.update_yaxes(title_text=f'{self.second} Volume', secondary_y=True, row=2, col=1)

        colors = ['cyan', 'magenta']

        label = f'{symbol} Volume'
        fig.add_trace(
            go.Bar(x=dataframe.index,
                y=dataframe['Volume'],
                marker_color=colors[secondary],
                name=label,
                opacity=.7
            ),
            row=2,
            col=1,
            secondary_y=secondary
        )
        return fig


    @staticmethod
    def show_price(price_df):
        fig = go.Figure()

        fig.add_trace(go.Indicator(
            mode="number+delta",
            value=price_df['Close'][-1],
            number={'prefix': "$"},
            delta={'position': "top", 'reference': price_df['Close'][-2]},
            domain={'x': [0, 1], 'y': [0.4, 1]}))
        fig.add_trace(go.Indicator(
            mode="delta",
            value=price_df['Close'][-1],
            delta={'position': "top",
                   'reference': price_df['Close'][-2], 'relative': True},
            domain={'x': [0.0, 1], 'y': [0.0, 0.4]}))

        fig.update_layout(
            margin_b=0,
            margin_l=0,
            margin_t=0,
            margin_r=0,
            autosize=True
        )
        return fig

    @staticmethod
    def indicator_chart(advice, symbol, advice_2=None, symbol_2=None):
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
            domain={'x': [0.01, 0.3], 'y': [0.0, 1]},
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

        if advice_2 is not None:
            tot2 = 0
            for signal in advice_2['Advice']:
                if 'Hold' in signal:
                    pass
                if 'Sell' in signal:
                    tot2 -= 1
                if 'Buy' in signal:
                    tot2 += 1

            indicator_fig_2 = go.Indicator(
                mode='gauge',
                value=tot2,
                title='Advice',
                domain={'x': [0.7, 0.99], 'y': [0.0, 1]},
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

            data = [indicator_fig, indicator_fig_2]
            title=f'Indicator chart: {symbol} | {symbol_2}'

        else:
            index = fear_and_greed.get()
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

            title=f'{symbol}: Indicator Graph | Fear and Greed Graph'
            data = [indicator_fig, fear_and_greed_fig]


        layout = go.Layout(
            margin_b=0,
            margin_l=100,
            margin_t=50,
            margin_r=100,
            autosize=True,
            title=title
        )

        fig = go.Figure(data=data, layout=layout)
        return fig
