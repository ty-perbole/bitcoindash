import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import pandas as pd
import chart_utils

CHART_HEIGHT = '400px'

def figures(start_date, end_date, date_granularity, axis_type):
    whirlpool_data_clean = pd.read_csv('data/whirlpool_data_clean.csv')
    whirlpool_data_clean_filter = whirlpool_data_clean.loc[
        (whirlpool_data_clean['date_granularity'] == date_granularity)
      & (whirlpool_data_clean['date_period'] >= start_date)
      & (whirlpool_data_clean['date_period'] <= end_date)
    ]

    unspent_data_clean = pd.read_csv('data/cj_unspent_data_clean.csv')
    unspent_data_clean_filter = unspent_data_clean.loc[
        (unspent_data_clean['date_granularity'] == date_granularity)
        & (unspent_data_clean['date_period'] >= start_date)
        & (unspent_data_clean['date_period'] <= end_date)
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
        halving_lines=False, marker_color='red')

    wasabi_volume_btc = chart_utils.single_axis_chart(
        unspent_data_clean_filter, x_series='date_period', y_series='wasabi_volume',
        title='Wasabi Volume', y_series_title='Wasabi Volume (BTC)',
        # y_series_axis_format="${n},",
        y_series_axis_type=axis_type, data_source='Proprietary (Updated weekly Thurs AM)',
        bars=len(unspent_data_clean_filter) <= 90 or date_granularity not in ['day', 'week'],
        halving_lines=False,
        marker_color='green')

    whirlpool_unspent = chart_utils.whirlpool_stacked_area_chart(
        unspent_data_clean_filter, x_series='date_period', chart='unspent_capacity',
        title='Whirlpool Unspent Capacity (BTC)', y_series_title='Unspent Capacity (BTC)',
        y_series_axis_type=axis_type, data_source='Proprietary',
        bars=len(unspent_data_clean_filter) <= 90 or date_granularity not in ['day', 'week'],
        halving_lines=False)

    whirlpool_unspent_count = chart_utils.whirlpool_stacked_area_chart(
        unspent_data_clean_filter, x_series='date_period', chart='num_outputs',
        title='Whirlpool Unspent Capacity (Output Count)', y_series_title='Unspent Capacity (Num Outputs)',
        y_series_axis_type=axis_type, data_source='Proprietary',
        bars=len(unspent_data_clean_filter) <= 90 or date_granularity not in ['day', 'week'],
        halving_lines=False)

    wasabi_unspent = chart_utils.wasabi_stacked_area_chart(
        unspent_data_clean_filter, x_series='date_period',
        title='Wasabi Post-Coinjoin UTXO Value', y_series_title='UTXO Value (BTC)',
        y_series_axis_type=axis_type, data_source='Proprietary',
        bars=len(unspent_data_clean_filter) <= 90 or date_granularity not in ['day', 'week'],
        halving_lines=False)

    whirlpool_new_btc = chart_utils.single_axis_chart(
        whirlpool_data_clean_filter, x_series='date_period', y_series='nb_new_tx0s',
        title='Whirlpool New Tx0s', y_series_title='New Tx0s Count',
        y_series_axis_type=axis_type, data_source='code.samourai.io/whirlpool/whirlpool_stats',
        bars=len(whirlpool_data_clean_filter) <= 90 or date_granularity not in ['day', 'week'],
        halving_lines=False, marker_color='red')

    whirlpool_volume_share = chart_utils.single_axis_chart(
        whirlpool_data_clean_filter, x_series='date_period', y_series=['pool_50M', 'pool_5M', 'pool_1M'],
        title='Whirlpool Volume by Pool', y_series_title='Whirlpool Volume Share',
        y_series_axis_format=".2%",
        y_series_axis_type=axis_type, data_source='code.samourai.io/whirlpool/whirlpool_stats',
        bars=False,
        halving_lines=False)

    bisq_vol = chart_utils.single_axis_chart(
        bisq_data_clean_filter, x_series='date_period', y_series='usd_volume',
        title='Bisq BTC Volume ($USD)', y_series_title='$USD Trade Volume on Bisq',
        y_series_axis_type=axis_type, data_source='monitor.bisq.network',
        bars=len(bisq_data_clean_filter) <= 90 or date_granularity not in ['day', 'week'],
        halving_lines=False)

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
                    figure=wasabi_volume_btc,
                    id='wasabi_volume_btc',
                    style={'height': CHART_HEIGHT}
                ),
                html.Details([
                    html.Summary('Tell me about Wasabi Volume'),
                    html.P('''Total volume mixed by Wasabi. Relies on a proprietary classification model and data may include both false positives and false negatives.''')
                ])
            ], width={"size": 6}),
        ], justify="center"),

        dbc.Row([
            dbc.Col([html.H4(" ")])
        ], justify="center"),

        dbc.Row([
            dbc.Col([
                dcc.Graph(
                    figure=whirlpool_unspent,
                    id='whirlpool_unspent',
                    style={'height': CHART_HEIGHT}
                ),
                html.Details([
                    html.Summary('Tell me about Whirlpool Unspent Capacity'),
                    html.P('''Unspent BTC amount of Whirlpool-coinjoined transaction outputs. ~100 BTC discrepancy from Clark Moody's dashboard may be due to impact of Tx0s, which are not counted in my unspent capacity calculation.''')
                ])
            ], width={"size": 6}),
            dbc.Col([
                dcc.Graph(
                    figure=wasabi_unspent,
                    id='wasabi_unspent',
                    style={'height': CHART_HEIGHT}
                ),
                html.Details([
                    html.Summary('Tell me about Wasabi Post-Coinjoin Unspent Transaction Outputs'),
                    html.P('''Total value of all unspent transaction outputs that went through a Wasabi Coinjoin. Broken down between direct outputs of Wasabi transactions, and UTXOs that are 1-hop away from a Wasabi CoinJoin and were spent in a 1-input 1-output transaction. 1-hop outputs are likely Wasabi coinjoined BTC in cold storage.''')
                ])
            ], width={"size": 6}),
        ], justify="center"),

        dbc.Row([
            dbc.Col([html.H4(" ")])
        ], justify="center"),

        dbc.Row([
            dbc.Col([
                dcc.Graph(
                    figure=whirlpool_unspent_count,
                    id='whirlpool_unspent_count',
                    style={'height': CHART_HEIGHT}
                ),
                html.Details([
                    html.Summary('Tell me about Whirlpool Unspent Capacity (Outputs)'),
                    html.P(
                        '''Number of unspent outputs from Whirlpool-coinjoined transactions.''')
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
                    html.P('''BTC transactoin volume on P2P exchange Bisq, denominated in $USD.''')
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
                    html.P('''Percent of Whirlpool Volume coming from different sized pools.''')
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
                    html.P('''Total number of new TXOs (Tx0s) entering Whirlpool across all pools.''')
                ])
            ], width={"size": 6}),
        ], justify="center")
    ]

    return children