import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import datetime
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import utils

CHART_HEIGHT = '400px'

def get_halving_era_string(row):
    if row['halving_era'] == datetime.date(2009, 1, 3):
        return 'The before Time'
    elif row['halving_era'] == datetime.date(2012, 11, 29):
        return '2013 Cycle'
    elif row['halving_era'] == datetime.date(2016, 7, 10):
        return '2017 Cycle'
    elif row['halving_era'] == datetime.date(2020, 5, 11):
        return '2021 Cycle'
    return 'Other'

def plot_comparison_chart(df, series, index=False, cycle='halving', **kwargs):
    if cycle == 'halving':
        x_series = 'days_since_halving'
        cols = 'halving_era_string'
        x_title = 'Days Since Halving'
        cutoff = 1425
    else:
        x_series = 'days_since_cycle'
        cols = 'cycle_string'
        x_title = 'Days Since Cycle Bottom'
        cutoff = 2000

    temp = df.loc[
        df[x_series] <= cutoff
        ].pivot(index=x_series, columns=cols, values=series).reset_index(drop=True)

    if index == True:
        for col in temp.columns:
            temp[col] = temp[col] / np.mean(temp[col][:28])

    fig = make_subplots(
        specs=[[{"secondary_y": False}]]
    )

    if kwargs.get('smooth', False):
        temp['2013 Cycle'] = temp['2013 Cycle'].rolling(14).mean()
        temp['2017 Cycle'] = temp['2017 Cycle'].rolling(14).mean()
        temp['2021 Cycle'] = temp['2021 Cycle'].rolling(14).mean()

    fig.add_trace(
        go.Scatter(x=temp.index, y=temp['2013 Cycle'], name='2013 Cycle'),
        secondary_y=False
    )

    fig.add_trace(
        go.Scatter(x=temp.index, y=temp['2017 Cycle'], name='2017 Cycle'),
        secondary_y=False
    )

    fig.add_trace(
        go.Scatter(x=temp.index, y=temp['2021 Cycle'], name='2021 Cycle'),
        secondary_y=False
    )

    fig.update_layout(
        title_text=kwargs.get('title', series),
        annotations=[
            dict(x=1, y=-0.2,
                 text="Data: {}".format(kwargs.get('data_source', 'CoinMetrics')),
                 showarrow=False, xref='paper', yref='paper',
                 xanchor='right', yanchor='auto', xshift=0, yshift=0)
        ],
        showlegend=True,
        legend_orientation="v",
        template="plotly_dark"
    )

    fig.update_xaxes(
        title_text=x_title, showgrid=False, showline=False, zeroline=False)
    fig.update_yaxes(
        title_text=series, showgrid=False, showline=False, zeroline=False,
        tickformat=kwargs.get('y_axis_format', None),
        type=kwargs.get('y_axis_type', 'linear'), range=kwargs.get('y_axis_range'), )

    return fig

def figures():
    cm_data_clean = pd.read_csv('data/cm_data_clean.csv')

    cm_data_clean_filter = cm_data_clean.loc[
        cm_data_clean['date_granularity'] == 'day'].reset_index(drop=True)
    cm_data_clean_filter = utils.get_extra_datetime_cols(cm_data_clean_filter, 'date_period')
    cm_data_clean_filter['days_since_halving'] = [(datetime.datetime.strptime(x, "%Y-%m-%d").date() - y).days for x, y
                                                  in zip(cm_data_clean_filter['date_period'],
                                                         cm_data_clean_filter['halving_era'])]
    cm_data_clean_filter['halving_era_string'] = cm_data_clean_filter.apply(get_halving_era_string, axis=1)

    market_cap = plot_comparison_chart(cm_data_clean_filter, 'CapMrktCurUSD', cycle='halving', index=True, title='Market Cap', y_axis_type='log')
    mvrv = plot_comparison_chart(cm_data_clean_filter, 'CapMVRVCur', cycle='halving', index=False, title='MVRV')
    hash_rate = plot_comparison_chart(cm_data_clean_filter, 'HashRate', cycle='halving', index=True, title='Hash Rate (14DMA)', y_axis_type='log', smooth=True)
    vol = plot_comparison_chart(cm_data_clean_filter, 'VtyDayRet30d', cycle='halving', index=False, title='30 Day Trailing Volatility')
    tx_vol = plot_comparison_chart(cm_data_clean_filter, 'TxTfrValAdjUSD', cycle='halving', index=True, title='On-Chain Transaction Volume (14DMA)', y_axis_type='log', smooth=True)
    addresses = plot_comparison_chart(cm_data_clean_filter, 'AdrActCnt', cycle='halving', index=True, title='Active On-Chain Addresses (14DMA)', smooth=True)

    children = [
        dbc.Row([
            dbc.Col([html.H4(" ")])
        ], justify="center"),

        dbc.Row([
            dcc.Markdown('''
                        ## Date filters are not functional on this tab, charts are static.
                        #### See [this thread](https://twitter.com/typerbole/status/1345435497988952067) for background.
                        ''')
        ], justify="center"),

        dbc.Row([
            dbc.Col([html.H4(" ")])
        ], justify="center"),

        dbc.Row([
            dbc.Col([
                dcc.Graph(
                    figure=market_cap,
                    id='market_cap',
                    style={'height': CHART_HEIGHT}
                ),
                # html.Details([
                #     html.Summary('Tell me about Market Cap'),
                #     html.P(
                #         '''Market Cap is the supply of Bitcoin multiplied by the price.''')
                # ])
            ], width={"size": 6}),

            dbc.Col([
                dcc.Graph(
                    figure=mvrv,
                    id='mvrv',
                    style={'height': CHART_HEIGHT}
                ),
                # html.Details([
                #     html.Summary('Tell me about Realized Cap'),
                #     html.P('''Realized Cap is a rough approximation of the cost basis for Bitcoin hodlers. If Realized Cap increases, that means more fiat has been exchanged for Bitcoin.''')
                # ])
            ], width={"size": 6}),

        ], justify="center"),

        dbc.Row([
            dbc.Col([html.H4(" ")])
        ], justify="center"),

        dbc.Row([
            dbc.Col([
                dcc.Graph(
                    figure=hash_rate,
                    id='hash_rate',
                    style={'height': CHART_HEIGHT}
                ),
                # html.Details([
                #     html.Summary('Tell me about Realized Cap HODL Waves'),
                #     html.P(
                #         '''Realized Cap HODL waves are a fun way of looking at market cycles. It tracks how much Realized Cap value is accounted for in different UTXO age bands. Honestly including this one was complete vanity as it's the only metric on this dash I contributed to. Data might be a few days stale as I have to refresh manually.''')
                # ])
            ], width={"size": 6}),
            dbc.Col([
                dcc.Graph(
                    figure=vol,
                    id='vol',
                    style={'height': CHART_HEIGHT}
                ),
                # html.Details([
                #     html.Summary('Tell me about Transaction Volume'),
                #     html.P('''$USD denominated value transacted on-chain over the relevant period.''')
                # ])
            ], width={"size": 6}),
        ], justify="center"),

        dbc.Row([
            dbc.Col([html.H4(" ")])
        ], justify="center"),

        dbc.Row([
            dbc.Col([
                dcc.Graph(
                    figure=tx_vol,
                    id='tx_vol',
                    style={'height': CHART_HEIGHT}
                ),
                # html.Details([
                #     html.Summary('Tell me about Realized Cap HODL Waves'),
                #     html.P(
                #         '''Realized Cap HODL waves are a fun way of looking at market cycles. It tracks how much Realized Cap value is accounted for in different UTXO age bands. Honestly including this one was complete vanity as it's the only metric on this dash I contributed to. Data might be a few days stale as I have to refresh manually.''')
                # ])
            ], width={"size": 6}),
            dbc.Col([
                dcc.Graph(
                    figure=addresses,
                    id='addresses',
                    style={'height': CHART_HEIGHT}
                ),
                # html.Details([
                #     html.Summary('Tell me about Transaction Volume'),
                #     html.P('''$USD denominated value transacted on-chain over the relevant period.''')
                # ])
            ], width={"size": 6}),
        ], justify="center")
    ]

    return children