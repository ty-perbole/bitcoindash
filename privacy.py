import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import pandas as pd
import chart_utils

CHART_HEIGHT = '400px'

def figures(start_date, end_date, date_granularity, axis_type):
    whirlpool_data_clean = pd.read_csv('whirlpool_data_clean.csv')
    whirlpool_data_clean_filter = whirlpool_data_clean.loc[
        (whirlpool_data_clean['date_granularity'] == date_granularity)
      & (whirlpool_data_clean['date_period'] >= start_date)
      & (whirlpool_data_clean['date_period'] <= end_date)
    ]

    bisq_data_clean = pd.read_csv('data/bisq_data_clean.csv')
    bisq_data_clean_filter = bisq_data_clean.loc[
        (bisq_data_clean['date_granularity'] == date_granularity)
        & (bisq_data_clean['date_period'] >= start_date)
        & (bisq_data_clean['date_period'] <= end_date)
        ]

    whirlpool_volume_btc = chart_utils.single_axis_chart(
        whirlpool_data_clean_filter, x_series='date_period', y_series='volume',
        title='Whirlpool Volume', y_series_title='Whirlpool Volume (BTC)',
        # y_series_axis_format="${n},",
        y_series_axis_type=axis_type, data_source='code.samourai.io/whirlpool/whirlpool_stats',
        bars=len(whirlpool_data_clean_filter) <= 90 or date_granularity not in ['day', 'week'],
        halving_lines=False)#True if date_granularity not in ['halving_era', 'market_cycle'] else False)

    whirlpool_new_btc = chart_utils.single_axis_chart(
        whirlpool_data_clean_filter, x_series='date_period', y_series='nb_new_btc',
        title='Whirlpool New Tx0s', y_series_title='New Tx0s (Total BTC)',
        # y_series_axis_format="${n},",
        y_series_axis_type=axis_type, data_source='code.samourai.io/whirlpool/whirlpool_stats',
        bars=len(whirlpool_data_clean_filter) <= 90 or date_granularity not in ['day', 'week'],
        halving_lines=False)#True if date_granularity not in ['halving_era', 'market_cycle'] else False)

    whirlpool_volume_share = chart_utils.single_axis_chart(
        whirlpool_data_clean_filter, x_series='date_period', y_series=['pool_50M', 'pool_5M', 'pool_1M'],
        title='Whirlpool Volume by Pool', y_series_title='Whirlpool Volume Share',
        y_series_axis_format=".2%",
        y_series_axis_type=axis_type, data_source='code.samourai.io/whirlpool/whirlpool_stats',
        bars=False,
        halving_lines=False)#True if date_granularity not in ['halving_era', 'market_cycle'] else False)

    bisq_vol = chart_utils.single_axis_chart(
        bisq_data_clean_filter, x_series='date_period', y_series='volume',
        title='Bisq BTC Volume', y_series_title='Trade Volume on Bisq',
        # y_series_axis_format="${n},",
        y_series_axis_type=axis_type, data_source='monitor.bisq.network',
        bars=len(bisq_data_clean_filter) <= 90 or date_granularity not in ['day', 'week'],
        halving_lines=True if date_granularity not in ['halving_era', 'market_cycle'] else False)

    children = [
        dbc.Row([
            dbc.Col([
                html.Details([
                    html.Summary('🌀️ How to improve Bitcoin privacy 🌀️', style={'fontSize': 26}),
                    dcc.Markdown('''
                            ### Use privacy enhancing software & follow best practices!
                            See this guide to learn more: [bitcoinprivacy.guide](https://bitcoinprivacy.guide/)
                            
                            ### Support the development of privacy software!
                            This is a worthy fund: https://hrf.org/programs_posts/devfund/
                            ''')
                ]),
                html.H4(" ")
            ])
        ], justify="center"),

        dbc.Row([
            dbc.Col([
                dcc.Graph(
                    figure=whirlpool_volume_btc,
                    id='whirlpool_volume_btc',
                    style={'height': CHART_HEIGHT}
                ),
                html.Details([
                    html.Summary('Tell me about Whirlpool Volume'),
                    html.P('''Total volume mixed by Whirlpool.''')
                ])
            ], width={"size": 6}),
            dbc.Col([
                dcc.Graph(
                    figure=whirlpool_new_btc,
                    id='whirlpool_new_btc',
                    style={'height': CHART_HEIGHT}
                ),
                html.Details([
                    html.Summary('Tell me about Whirlpool New TxOs'),
                    html.P('''Total value of new TXOs (Tx0s) entering Whirlpool.''')
                ])
            ], width={"size": 6}),
        ], justify="center"),

        dbc.Row([
            dbc.Col([html.H4(" ")])
        ], justify="center"),

        dbc.Row([
            dbc.Col([
                dcc.Graph(
                    figure=whirlpool_volume_share,
                    id='whirlpool_volume_share',
                    style={'height': CHART_HEIGHT}
                ),
                html.Details([
                    html.Summary('Whirlpool volume breakdown by pool size.'),
                    html.P('''foo''')
                ])
            ], width={"size": 6}),
            dbc.Col([
                dcc.Graph(
                    figure=bisq_vol,
                    id='bisq_vol',
                    style={'height': CHART_HEIGHT}
                ),
                html.Details([
                    html.Summary('Tell me about Bisq BTC Volume'),
                    html.P('''BTC transactoin volume on P2P exchange Bisq.''')
                ])
            ], width={"size": 6}),
        ], justify="center")
    ]

    return children