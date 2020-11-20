import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import pandas as pd
import chart_utils

CHART_HEIGHT = '400px'

def figures(start_date, end_date, date_granularity, axis_type):
    cm_data_clean = pd.read_csv('data/cm_data_clean.csv')
    cm_data_clean_filter = cm_data_clean.loc[
        (cm_data_clean['date_granularity'] == date_granularity)
      & (cm_data_clean['date_period'] >= start_date)
      & (cm_data_clean['date_period'] <= end_date)
    ]

    wave_data = pd.read_csv('data/waves_data_clean2.csv')
    wave_data_filter = wave_data.loc[
        (wave_data['date_granularity'] == date_granularity)
        & (wave_data['date_period'] >= start_date)
        & (wave_data['date_period'] <= end_date)
        ]

    market_cap = chart_utils.single_axis_chart(
        cm_data_clean_filter, x_series='date_period', y_series='CapMrktCurUSD',
        title='Market Cap', y_series_title='Market Cap ($USD)',
        # y_series_axis_format="${n},",
        y_series_axis_type=axis_type,
        bars=len(cm_data_clean_filter) <= 90 or date_granularity not in ['day', 'week'],
        halving_lines=True if date_granularity not in ['halving_era', 'market_cycle'] else False)

    real_cap = chart_utils.single_axis_chart(
        cm_data_clean_filter, x_series='date_period', y_series='CapRealUSD',
        title='Realized Cap', y_series_title='Realized Cap ($USD)',
        # y_series_axis_format="${n},",
        y_series_axis_type=axis_type,
        bars=len(cm_data_clean_filter) <= 90 or date_granularity not in ['day', 'week'],
        halving_lines=True if date_granularity not in ['halving_era', 'market_cycle'] else False)


    hodl_wave = chart_utils.hodl_waves_chart2(
        wave_data_filter,
        halving_lines=True if date_granularity not in ['halving_era', 'market_cycle'] else False)

    # mvrv = chart_utils.single_axis_chart(
    #     cm_data_clean_filter, x_series='date_period', y_series='CapMVRVCur',
    #     title='Market Value to Realized Value', y_series_title='MVRV',
    #     y_series_axis_type=axis_type,
    #     bars=len(cm_data_clean_filter) <= 90 or date_granularity not in ['day', 'week'],
    #     halving_lines=True if date_granularity not in ['halving_era', 'market_cycle'] else False)

    tx_vol = chart_utils.single_axis_chart(
        cm_data_clean_filter, x_series='date_period', y_series='TxTfrValAdjUSD',
        title='Transaction Volume ($USD, Adjusted for Change)', y_series_title='Transaction Volume ($USD)',
        y_series_axis_type=axis_type,
        bars=len(cm_data_clean_filter) <= 90 or date_granularity not in ['day', 'week'],
        halving_lines=True if date_granularity not in ['halving_era', 'market_cycle'] else False)

    children = [
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
                html.Details([
                    html.Summary('Tell me about Market Cap'),
                    html.P(
                        '''Market Cap is the supply of Bitcoin multiplied by the price.''')
                ])
            ], width={"size": 6}),

            dbc.Col([
                dcc.Graph(
                    figure=real_cap,
                    id='real_cap',
                    style={'height': CHART_HEIGHT}
                ),
                html.Details([
                    html.Summary('Tell me about Realized Cap'),
                    html.P('''Realized Cap is a rough approximation of the cost basis for Bitcoin hodlers. If Realized Cap increases, that means more fiat has been exchanged for Bitcoin.''')
                ])
            ], width={"size": 6}),

        ], justify="center"),

        dbc.Row([
            dbc.Col([html.H4(" ")])
        ], justify="center"),

        dbc.Row([
            dbc.Col([
                dcc.Graph(
                    figure=hodl_wave,
                    id='hodl_wave',
                    style={'height': CHART_HEIGHT}
                ),
                html.Details([
                    html.Summary('Tell me about Realized Cap HODL Waves'),
                    html.P(
                        '''Realized Cap HODL waves are a fun way of looking at market cycles. It tracks how much Realized Cap value is accounted for in different UTXO age bands. Honestly including this one was complete vanity as it's the only metric on this dash I contributed to. Data might be a few days stale as I have to refresh manually.''')
                ])
            ], width={"size": 6}),
            # dbc.Col([
            #     dcc.Graph(
            #         figure=mvrv,
            #         id='mvrv',
            #         style={'height': CHART_HEIGHT}
            #     ),
            #     html.Details([
            #         html.Summary('Tell me about MVRV'),
            #         html.P('''MVRV is the ratio of the MarketCap to RealizedCap. It is a great indicator of market tops and bottoms. See: https://charts.woobull.com/bitcoin-mvrv-ratio/''')
            #     ])
            # ], width={"size": 6}),
            dbc.Col([
                dcc.Graph(
                    figure=tx_vol,
                    id='tx_volume',
                    style={'height': CHART_HEIGHT}
                ),
                html.Details([
                    html.Summary('Tell me about Transaction Volume'),
                    html.P('''$USD denominated value transacted on-chain over the relevant period.''')
                ])
            ], width={"size": 6}),
        ], justify="center")
    ]

    return children