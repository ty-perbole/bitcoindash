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

    jm_data_clean = pd.read_csv('data/jm_orderbook.csv')
    jm_data_clean_filter = jm_data_clean.loc[
        (jm_data_clean['date_granularity'] == date_granularity)
        & (jm_data_clean['date_period'] >= start_date)
        & (jm_data_clean['date_period'] <= end_date)
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

    whirlpool_tx_fee = chart_utils.single_axis_chart(
        unspent_data_clean_filter, x_series='date_period', y_series='whirlpool_tx_fee',
        title='Whirlpool Transactions BlockSpace Fee', y_series_title='Blockspace Fee (Sat/VByte)',
        # y_series_axis_format="${n},",
        y_series_axis_type=axis_type, data_source='Proprietary (Updated weekly Thurs AM)',
        bars=len(unspent_data_clean_filter) <= 90 or date_granularity not in ['day', 'week'],
        halving_lines=False,
        marker_color='red')

    wasabi_volume_btc = chart_utils.single_axis_chart(
        unspent_data_clean_filter, x_series='date_period', y_series='wasabi_volume',
        title='Wasabi Volume', y_series_title='Wasabi Volume (BTC)',
        # y_series_axis_format="${n},",
        y_series_axis_type=axis_type, data_source='Proprietary (Updated weekly Thurs AM)',
        bars=len(unspent_data_clean_filter) <= 90 or date_granularity not in ['day', 'week'],
        halving_lines=False,
        marker_color='green')

    jm_volume_btc = chart_utils.single_axis_chart(
        unspent_data_clean_filter, x_series='date_period', y_series='jm_volume',
        title='JoinMarket Volume', y_series_title='JoinMarket Volume (BTC)',
        # y_series_axis_format="${n},",
        y_series_axis_type=axis_type, data_source='Proprietary (Updated weekly Thurs AM)',
        bars=len(unspent_data_clean_filter) <= 90 or date_granularity not in ['day', 'week'],
        halving_lines=False)

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

    wasabi_unspent = chart_utils.wasabi_jm_stacked_area_chart(
        unspent_data_clean_filter, x_series='date_period',
        title='Wasabi Post-Coinjoin UTXO Value', y_series_title='UTXO Value (BTC)',
        y_series_axis_type=axis_type, data_source='Proprietary',
        bars=len(unspent_data_clean_filter) <= 90 or date_granularity not in ['day', 'week'],
        halving_lines=False)

    jm_unspent = chart_utils.wasabi_jm_stacked_area_chart(
        unspent_data_clean_filter, cj_type='jm', x_series='date_period',
        title='JoinMarket Post-Coinjoin UTXO Value', y_series_title='UTXO Value (BTC)',
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

    jm_volume_share = chart_utils.single_axis_chart(
        unspent_data_clean_filter, x_series='date_period', y_series=['WrappedSegwit', 'NativeSegwit'],
        title='JoinMarket Volume by OrderBook', y_series_title='JoinMarket Volume Share',
        y_series_axis_format=".2%",
        y_series_axis_type=axis_type, data_source='Proprietary',
        bars=False,
        halving_lines=False)

    jm_maker_count = chart_utils.single_axis_chart(
        jm_data_clean_filter, x_series='date_period', y_series='maker_count',
        title='JoinMarket Maker Count', y_series_title='Makers on JoinMarket',
        # y_series_axis_format="${n},",
        y_series_axis_type=axis_type, data_source='https://nixbitcoin.org/obwatcher',
        bars=len(jm_data_clean_filter) <= 90 or date_granularity not in ['day', 'week'],
        halving_lines=False)

    jm_maker_liquidity = chart_utils.single_axis_chart(
        jm_data_clean_filter, x_series='date_period', y_series='maker_liquidity',
        title='JoinMarket Maker Liquidity', y_series_title='Maker Liquidity (BTC)',
        # y_series_axis_format="${n},",
        y_series_axis_type=axis_type, data_source='https://nixbitcoin.org/obwatcher',
        bars=len(jm_data_clean_filter) <= 90 or date_granularity not in ['day', 'week'],
        halving_lines=False)

    jm_cj_fee = chart_utils.single_axis_chart(
        jm_data_clean_filter, x_series='date_period', y_series='cj_fee',
        title='JoinMarket Maker Median Fee Rate', y_series_title='Median Fee Rate',
        # y_series_axis_format="{n}%",
        y_series_axis_type=axis_type, data_source='https://nixbitcoin.org/obwatcher',
        bars=len(jm_data_clean_filter) <= 90 or date_granularity not in ['day', 'week'],
        halving_lines=False)

    jm_mean_liquidity = chart_utils.single_axis_chart(
        jm_data_clean_filter, x_series='date_period', y_series='mean_liquidity_per_maker',
        title='JoinMarket Mean Liquidity per Maker', y_series_title='Mean BTC Liquidity per Maker',
        # y_series_axis_format="${n},",
        y_series_axis_type=axis_type, data_source='https://nixbitcoin.org/obwatcher',
        bars=len(jm_data_clean_filter) <= 90 or date_granularity not in ['day', 'week'],
        halving_lines=False)

    jm_median_liquidity = chart_utils.single_axis_chart(
        jm_data_clean_filter, x_series='date_period', y_series='median_liquidity_per_maker',
        title='JoinMarket Median Liquidity per Maker', y_series_title='Median BTC Liquidity per Maker',
        # y_series_axis_format="${n},",
        y_series_axis_type=axis_type, data_source='https://nixbitcoin.org/obwatcher',
        bars=len(jm_data_clean_filter) <= 90 or date_granularity not in ['day', 'week'],
        halving_lines=False)

    bisq_vol = chart_utils.single_axis_chart(
        bisq_data_clean_filter, x_series='date_period', y_series='usd_volume',
        title='Bisq BTC Volume ($USD)', y_series_title='$USD Trade Volume on Bisq',
        y_series_axis_type=axis_type, data_source='monitor.bisq.network',
        bars=len(bisq_data_clean_filter) <= 90 or date_granularity not in ['day', 'week'],
        halving_lines=False)

    whirlpool_content = [
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
                    html.P(
                        '''Unspent BTC amount of Whirlpool-coinjoined transaction outputs. ~100 BTC discrepancy from Clark Moody's dashboard may be due to impact of Tx0s, which are not counted in my unspent capacity calculation.''')
                ])
            ], width={"size": 6}),
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
                    figure=whirlpool_volume_share,
                    id='whirlpool_volume_share',
                    style={'height': CHART_HEIGHT}
                ),
                html.Details([
                    html.Summary('Tell me about Whirlpool volume breakdown by pool size.'),
                    html.P('''Percent of Whirlpool Volume coming from different sized pools.''')
                ])
            ], width={"size": 6}),
        ], justify="center"),

        dbc.Row([
            dbc.Col([html.H4(" ")])
        ], justify="center"),

        dbc.Row([
            dbc.Col([
                dcc.Graph(
                    figure=whirlpool_tx_fee,
                    id='whirlpool_tx_fee',
                    style={'height': CHART_HEIGHT}
                ),
                html.Details([
                    html.Summary('Tell me about Whirlpool Transactions BlockSpace Fee'),
                    html.P('''The block space fee rate in Sats/VByte paid by Whirlpool transactions.''')
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

    wasabi_content = [
        dbc.Row([
            dbc.Col([html.H4(" ")])
        ], justify="center"),

        dbc.Row([
            dbc.Col([
                dcc.Graph(
                    figure=wasabi_unspent,
                    id='wasabi_unspent',
                    style={'height': CHART_HEIGHT}
                ),
                html.Details([
                    html.Summary('Tell me about Wasabi Post-Coinjoin Unspent Transaction Outputs'),
                    html.P(
                        '''Total value of all unspent transaction outputs that went through a Wasabi Coinjoin. Broken down between direct outputs of Wasabi transactions, and UTXOs that are 1-hop away from a Wasabi CoinJoin and were spent in a 1-input 1-output transaction. 1-hop outputs are likely Wasabi coinjoined BTC in cold storage.''')
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
                    html.P(
                        '''Total volume mixed by Wasabi. Relies on a proprietary classification model and data may include both false positives and false negatives.''')
                ])
            ], width={"size": 6}),
        ], justify="center"),

        dbc.Row([
            dbc.Col([html.H4(" ")])
        ], justify="center"),
    ]

    jm_content = [
        dbc.Row([
            dbc.Col([html.H4(" ")])
        ], justify="center"),

        dbc.Row([
            dbc.Col([
                dcc.Graph(
                    figure=jm_unspent,
                    id='jm_unspent',
                    style={'height': CHART_HEIGHT}
                ),
                html.Details([
                    html.Summary('Tell me about JoinMarket Post-Coinjoin Unspent Transaction Outputs'),
                    html.P(
                        '''Total value of all unspent transaction outputs that went through a JoinMarket Coinjoin. Broken down between direct outputs of JoinMarket transactions, and UTXOs that are 1-hop away from a JoinMarket CoinJoin and were spent in a 1-input 1-output transaction. 1-hop outputs are likely JoinMarket coinjoined BTC in cold storage.''')
                ])
            ], width={"size": 6}),

            dbc.Col([
                dcc.Graph(
                    figure=jm_volume_btc,
                    id='jm_volume_btc',
                    style={'height': CHART_HEIGHT}
                ),
                html.Details([
                    html.Summary('Tell me about JoinMarket Volume'),
                    html.P(
                        '''Total volume mixed by JoinMarket. Relies on a proprietary classification model and data may include both false positives and false negatives.''')
                ])
            ], width={"size": 6}),
        ], justify="center"),

        dbc.Row([
            dbc.Col([html.H4(" ")])
        ], justify="center"),

        dbc.Row([
            dbc.Col([
                dcc.Graph(
                    figure=jm_maker_count,
                    id='jm_maker_count',
                    style={'height': CHART_HEIGHT}
                ),
                html.Details([
                    html.Summary('Tell me about JoinMarket Maker Count'),
                    html.P(
                        '''Total number of entities offering JoinMarket liquidity as Makers.''')
                ])
            ], width={"size": 6}),
            dbc.Col([
                dcc.Graph(
                    figure=jm_volume_share,
                    id='jm_volume_share',
                    style={'height': CHART_HEIGHT}
                ),
                html.Details([
                    html.Summary('Tell me about JoinMarket Volume by OrderBook'),
                    html.P(
                        '''JoinMarket recently transitioned to a Native Segwit orderbook. Currently both the WrappedSegwit and NativeSegwit orderbooks are live. Ideally all volume would migrate to NativeSegwit.''')
                ])
            ], width={"size": 6})
        ], justify="center"),

        dbc.Row([
            dbc.Col([html.H4(" ")])
        ], justify="center"),

        dbc.Row([
            dbc.Col([
                dcc.Graph(
                    figure=jm_maker_liquidity,
                    id='jm_maker_liquidity',
                    style={'height': CHART_HEIGHT}
                ),
                html.Details([
                    html.Summary('Tell me about JoinMarket Maker Liquidity'),
                    html.P(
                        '''Total BTC offered as liquidity by JoinMarket Makers.''')
                ])
            ], width={"size": 6}),
            dbc.Col([
                dcc.Graph(
                    figure=jm_cj_fee,
                    id='jm_cj_fee',
                    style={'height': CHART_HEIGHT}
                ),
                html.Details([
                    html.Summary('Tell me about JoinMarket Maker Fee Rate'),
                    html.P(
                        '''Median fee rate offered by JoinMarket Makers.''')
                ])
            ], width={"size": 6})
        ], justify="center"),

        dbc.Row([
            dbc.Col([html.H4(" ")])
        ], justify="center"),

        dbc.Row([
            dbc.Col([
                dcc.Graph(
                    figure=jm_mean_liquidity,
                    id='jm_mean_liquidity',
                    style={'height': CHART_HEIGHT}
                ),
                html.Details([
                    html.Summary('Tell me about JoinMarket Mean Liquidity per Maker'),
                    html.P(
                        '''The mean BTC amount of liquidity available from JoinMarket Makers.''')
                ])
            ], width={"size": 6}),
            dbc.Col([
                dcc.Graph(
                    figure=jm_median_liquidity,
                    id='jm_median_liquidity',
                    style={'height': CHART_HEIGHT}
                ),
                html.Details([
                    html.Summary('Tell me about JoinMarket Median Liquidity per Maker'),
                    html.P(
                        '''The median BTC amount of liquidity available from JoinMarket Makers.''')
                ])
            ], width={"size": 6})
        ], justify="center"),

        dbc.Row([
            dbc.Col([html.H4(" ")])
        ], justify="center"),
    ]

    bisq_content = [
        dbc.Row([
            dbc.Col([html.H4(" ")])
        ], justify="center"),

        dcc.Graph(
            figure=bisq_vol,
            id='bisq_vol',
            style={'height': CHART_HEIGHT}
        ),

        html.Details([
            html.Summary('Tell me about Bisq BTC Volume'),
            html.P('''BTC transactoin volume on P2P exchange Bisq, denominated in $USD.''')
        ]),

        dbc.Row([
            dbc.Col([html.H4(" ")])
        ], justify="center"),

    ]

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

        dbc.Tabs([
            dbc.Tab(
                whirlpool_content,
                label='Whirlpool',
                tab_id='whirlpool'
            ),

            dbc.Tab(
                wasabi_content,
                label='Wasabi',
                tab_id='wasabi'
            ),

            dbc.Tab(
                jm_content,
                label='JoinMarket',
                tab_id='joinmarket'
            ),

            dbc.Tab(
                bisq_content,
                label='Bisq',
                tab_id='bisq'
            )
        ], id='privacy-tabs', persistence=True)
    ]

    return children