import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import pandas as pd
import chart_utils

CHART_HEIGHT = '400px'

def figures(start_date, end_date, date_granularity, axis_type):
    ln_data_clean = pd.read_csv('data/ln_data_clean.csv')
    ln_data_clean_filter = ln_data_clean.loc[
        (ln_data_clean['date_granularity'] == date_granularity)
      & (ln_data_clean['date_period'] >= start_date)
      & (ln_data_clean['date_period'] <= end_date)
    ]

    mw_data_clean = pd.read_csv('data/mw_stats_data_clean.csv')
    mw_data_clean_filter = mw_data_clean.loc[
        (mw_data_clean['date_granularity'] == date_granularity)
        & (mw_data_clean['date_period'] >= start_date)
        & (mw_data_clean['date_period'] <= end_date)
        ]

    mw_hist_clean = pd.read_csv('data/mw_hist_data_clean.csv')
    mw_hist_clean_filter = mw_hist_clean.loc[
        (mw_hist_clean['date_granularity'] == date_granularity)
        & (mw_hist_clean['date_period'] >= start_date)
        & (mw_hist_clean['date_period'] <= end_date)
        ]

    node_count = chart_utils.single_axis_chart(
        ln_data_clean_filter, x_series='date_period', y_series='nodes_w_channels',
        title='Public Lightning Nodes', y_series_title='Public Lightning Node Count',
        # y_series_axis_format="${n},",
        y_series_axis_type=axis_type, data_source='ln.bigsun.xyz',
        bars=len(ln_data_clean_filter) <= 90 or date_granularity not in ['day', 'week'],
        halving_lines=True if date_granularity not in ['halving_era', 'market_cycle'] else False)

    herf = chart_utils.single_axis_chart(
        ln_data_clean_filter, x_series='date_period', y_series='node_liquidity_herfindahl',
        title='Public Lightning Node Liquidity Herfindahl Index', y_series_title='Herfindahl Index',
        # y_series_axis_format="${n},",
        y_series_axis_type=axis_type, data_source='ln.bigsun.xyz',
        bars=len(ln_data_clean_filter) <= 90 or date_granularity not in ['day', 'week'],
        halving_lines=True if date_granularity not in ['halving_era', 'market_cycle'] else False)

    channel_count = chart_utils.single_axis_chart(
        ln_data_clean_filter, x_series='date_period', y_series='channel_count',
        title='Lightning Node Public Channel Count', y_series_title='Channel Count',
        # y_series_axis_format="${n},",
        y_series_axis_type=axis_type, data_source='ln.bigsun.xyz',
        bars=len(ln_data_clean_filter) <= 90 or date_granularity not in ['day', 'week'],
        halving_lines=True if date_granularity not in ['halving_era', 'market_cycle'] else False)

    channel_value = chart_utils.single_axis_chart(
        ln_data_clean_filter, x_series='date_period', y_series='channel_value',
        title='Lightning Node Total Public Channel Value', y_series_title='Channel Value (BTC)',
        # y_series_axis_format="${n},",
        y_series_axis_type=axis_type, data_source='ln.bigsun.xyz',
        bars=len(ln_data_clean_filter) <= 90 or date_granularity not in ['day', 'week'],
        halving_lines=True if date_granularity not in ['halving_era', 'market_cycle'] else False)

    base_fee_millisatoshi = chart_utils.single_axis_chart(
        ln_data_clean_filter, x_series='date_period', y_series='sat_weighted_mean_base_fee_millisatoshi',
        title='Mean Base Fee (weighted by channel size)', y_series_title='Base Fee (millisat)',
        # y_series_axis_format="${n},",
        y_series_axis_type=axis_type, data_source='ln.bigsun.xyz',
        bars=len(ln_data_clean_filter) <= 90 or date_granularity not in ['day', 'week'],
        halving_lines=True if date_granularity not in ['halving_era', 'market_cycle'] else False)

    fee_per_millionth = chart_utils.single_axis_chart(
        ln_data_clean_filter, x_series='date_period', y_series='sat_weighted_mean_fee_per_millionth',
        title='Mean Proportional Fee (weighted by channel size)', y_series_title='Sats per million satoshis',
        # y_series_axis_format="${n},",
        y_series_axis_type=axis_type, data_source='ln.bigsun.xyz',
        bars=len(ln_data_clean_filter) <= 90 or date_granularity not in ['day', 'week'],
        halving_lines=True if date_granularity not in ['halving_era', 'market_cycle'] else False)

    swaps_per_day = chart_utils.single_axis_chart(
        mw_data_clean_filter, x_series='date_period', y_series='swaps_per_day',
        title='Mercury Wallet Statecoin Swap Count', y_series_title='Swap Count',
        # y_series_axis_format="${n},",
        y_series_axis_type=axis_type, data_source='api.mercurywallet.com/summary',
        bars=len(mw_data_clean_filter) <= 90 or date_granularity not in ['day', 'week'],
        halving_lines=False)

    swapset_per_day = chart_utils.single_axis_chart(
        mw_data_clean_filter, x_series='date_period', y_series='swapset_per_day',
        title='Mercury Wallet Statecoin Swap Set', y_series_title='Swap Set',
        # y_series_axis_format="${n},",
        y_series_axis_type=axis_type, data_source='api.mercurywallet.com/summary',
        bars=len(mw_data_clean_filter) <= 90 or date_granularity not in ['day', 'week'],
        halving_lines=False)

    capacity_statechains = chart_utils.single_axis_chart(
        mw_data_clean_filter, x_series='date_period', y_series='capacity_statechains',
        title='Mercury Wallet Statechain Capacity', y_series_title='Statechain Capacity (BTC)',
        # y_series_axis_format="${n},",
        y_series_axis_type=axis_type, data_source='api.mercurywallet.com/summary',
        bars=len(mw_data_clean_filter) <= 90 or date_granularity not in ['day', 'week'],
        halving_lines=False)

    # statecoins = chart_utils.single_axis_chart(
    #     mw_data_clean_filter, x_series='date_period', y_series='statecoins',
    #     title='Mercury Wallet All Time Statecoin Count', y_series_title='Statecoin Count',
    #     # y_series_axis_format="${n},",
    #     y_series_axis_type=axis_type, data_source='api.mercurywallet.com/summary',
    #     bars=len(mw_data_clean_filter) <= 90 or date_granularity not in ['day', 'week'],
    #     halving_lines=False)

    liquidity = chart_utils.single_axis_chart(
        mw_data_clean_filter, x_series='date_period', y_series='liquidity',
        title='Mercury Wallet Liquidity', y_series_title='Statecoin Count',
        # y_series_axis_format="${n},",
        y_series_axis_type=axis_type, data_source='api.mercurywallet.com/summary',
        bars=len(mw_data_clean_filter) <= 90 or date_granularity not in ['day', 'week'],
        halving_lines=False)

    # statecoin_hist = chart_utils.whirlpool_stacked_area_chart(
    #     mw_hist_clean_filter, x_series='date_period', chart='unspent_capacity',
    #     title='Whirlpool Unspent Capacity (BTC)', y_series_title='Unspent Capacity (BTC)',
    #     y_series_axis_type=axis_type, data_source='Proprietary',
    #     bars=len(unspent_data_clean_filter) <= 90 or date_granularity not in ['day', 'week'],
    #     halving_lines=False)

    lightning_content = [
        dbc.Row([
            dbc.Col([
                html.Details([
                    html.Summary('⚡️ How to grow Lightning Network ⚡️', style={'fontSize': 26}),
                    dcc.Markdown('''
                                ### Run a Bitcoin Node!
                                Run a Bitcoin node, specifically one that has lightning support, open some lightning channels and use lightning. See these guides to learn more: [node.guide](http://node.guide/), http://bitcoiner.guide/lightning
                                ''')
                ]),
                html.H4(" ")
            ])
        ], justify="center"),

        dbc.Row([
            dbc.Col([
                dcc.Graph(
                    figure=node_count,
                    id='node_count',
                    style={'height': CHART_HEIGHT}
                ),
                html.Details([
                    html.Summary('Tell me about Lightning Node Count'),
                    html.P(
                        '''Total count of lightning nodes with at least one pubic channel open as of the date. Note from the data source "Why is the number of open channels here much bigger than other explorers show? Because we keep counting the channels as open until their funding transaction is spent on the chain. Apparently many channels are abandoned and nodes turned off, sometimes temporarily, and the channels remain technically open, but cease to be announced to the rest of the network. Other explorers remove these inactive channels from their count of open channels, but we don't." See: https://ln.bigsun.xyz/docs.''')
                ])
            ], width={"size": 6}),
            dbc.Col([
                dcc.Graph(
                    figure=herf,
                    id='herf',
                    style={'height': CHART_HEIGHT}
                ),
                html.Details([
                    html.Summary('Tell me about Lightning Node Liquidity Herfindahl Index'),
                    html.P(
                        '''A Herfindahl index is a common measure of concentration. This metric tries to quantify how much liquidity is dispersed among nodes in the Lightning Network. It is the Herfindahl index of total channel value per node.''')
                ])
            ], width={"size": 6}),
        ], justify="center"),

        dbc.Row([
            dbc.Col([html.H4(" ")])
        ], justify="center"),

        dbc.Row([
            dbc.Col([
                dcc.Graph(
                    figure=channel_count,
                    id='channel_count',
                    style={'height': CHART_HEIGHT}
                ),
                html.Details([
                    html.Summary('Tell me about Channel Count'),
                    html.P(
                        '''Total number of open **public** lightning channels as of the date. Many lightning channels are private, so this undercounts total channels in existence.''')
                ])
            ], width={"size": 6}),
            dbc.Col([
                dcc.Graph(
                    figure=channel_value,
                    id='channel_value',
                    style={'height': CHART_HEIGHT}
                ),
                html.Details([
                    html.Summary('Tell me about Channel Value'),
                    html.P(
                        '''Total value of all **public** lightning channels as of the date. Many lightning channels are private, so this undercounts total channels in existence.''')
                ])
            ], width={"size": 6}),
        ], justify="center"),

        dbc.Row([
            dbc.Col([html.H4(" ")])
        ], justify="center"),

        dbc.Row([
            dbc.Col([
                dcc.Graph(
                    figure=base_fee_millisatoshi,
                    id='base_fee_millisatoshi',
                    style={'height': CHART_HEIGHT}
                ),
                html.Details([
                    html.Summary('Tell me about base fee'),
                    html.P(
                        '''The mean base fee per public lightning channel. "The default is 1000 millisat, which means 1 satoshi fee per every routed payment." (See https://openoms.gitbook.io/lightning-node-management/). Mean is weighted by channel size.''')
                ])
            ], width={"size": 6}),
            dbc.Col([
                dcc.Graph(
                    figure=fee_per_millionth,
                    id='fee_per_millionth',
                    style={'height': CHART_HEIGHT}
                ),
                html.Details([
                    html.Summary('Tell me about proportional fee'),
                    html.P(
                        '''The mean proportional fee per public lightning channel. "proportional fee (fee_rate) which is by default in lnd: 0.000001. This means there is an additional 1 sat charged for every million satoshis in the routed payment." (See https://openoms.gitbook.io/lightning-node-management/). Mean is weighted by channel size.''')
                ])
            ], width={"size": 6}),
        ], justify="center")
    ]

    mercury_content = [
        dbc.Row([
            dbc.Col([
                html.Details([
                    html.Summary('What are statechains?', style={'fontSize': 26}),
                    dcc.Markdown('''
                                    - Statechains are a novel layer two scaling protocol for Bitcoin. "The basic idea behind Statechains is that you lock up money between two parties in a 2-of-2 multisig: the Statechain entity and the user. When the user wants to transfer the money (the entire UTXO), they simply hand over their private key, which we call the transitory key, to the intended recipient. And that’s basically it. There is a lot more complexity operating in the background to decrease the potential for cheating, but in a nutshell this is the core concept, and as you will later see, it’s deceptively powerful." 
                                        See [here](https://medium.com/@RubenSomsen/statechains-non-custodial-off-chain-bitcoin-transfer-1ae4845a4a39)
                                    - [Mercury Wallet](https://mercurywallet.com/) is a statechain implementation.
                                    ''')
                ]),
                html.H4(" ")
            ])
        ], justify="center"),

        dbc.Row([
            dbc.Col([
                dcc.Graph(
                    figure=swaps_per_day,
                    id='swaps_per_day',
                    style={'height': CHART_HEIGHT}
                ),
                html.Details([
                    html.Summary('Tell me about Mercury Wallet Statecoin Swap Count'),
                    html.P(
                        '''Number of swaps completed over the time period on Mercury Wallet. See https://github.com/layer2tech/mercury-explorer/blob/main/api/API.md.''')
                ])
            ], width={"size": 6}),
            dbc.Col([
                dcc.Graph(
                    figure=swapset_per_day,
                    id='swapset_per_day',
                    style={'height': CHART_HEIGHT}
                ),
                html.Details([
                    html.Summary('Tell me about Mercury Wallet Statecoin Swap Set'),
                    html.P(
                        '''Total number of coins involved in a swap, the sum of every coin participating in every swap. See https://github.com/layer2tech/mercury-explorer/blob/main/api/API.md.''')
                ])
            ], width={"size": 6}),
        ], justify="center"),

        dbc.Row([
            dbc.Col([html.H4(" ")])
        ], justify="center"),

        dbc.Row([
            dbc.Col([
                dcc.Graph(
                    figure=capacity_statechains,
                    id='capacity_statechains',
                    style={'height': CHART_HEIGHT}
                ),
                html.Details([
                    html.Summary('Mercury Wallet Statechain Capacity'),
                    html.P(
                        '''Total value currently in mercury wallet statecoins, denominated in BTC. See https://github.com/layer2tech/mercury-explorer/blob/main/api/API.md.''')
                ])
            ], width={"size": 6}),
            dbc.Col([
                dcc.Graph(
                    figure=liquidity,
                    id='liquidity',
                    style={'height': CHART_HEIGHT}
                ),
                html.Details([
                    html.Summary('Tell me about Mercury Wallet Liquidity'),
                    html.P(
                        '''Current number of statecoins in mercury wallet. See https://github.com/layer2tech/mercury-explorer/blob/main/api/API.md.''')
                ])
            ], width={"size": 6}),
        ], justify="center"),

        # dbc.Row([
        #     dbc.Col([html.H4(" ")])
        # ], justify="center"),
        #
        # dbc.Row([
        #     dbc.Col([
        #         dcc.Graph(
        #             figure=statecoin_hist,
        #             id='statecoin_hist',
        #             style={'height': CHART_HEIGHT}
        #         ),
        #         html.Details([
        #             html.Summary('Tell me about Statecoin histogram.'),
        #             html.P(
        #                 '''Shows the number of statecoin UTXOs in Mercury Wallet by denomination. ''')
        #         ])
        #     ], width={"size": 6}),
        #     dbc.Col([
        #         dcc.Graph(
        #             figure=statecoins,
        #             id='statecoins',
        #             style={'height': CHART_HEIGHT}
        #         ),
        #         html.Details([
        #             html.Summary('Tell me about Mercury Wallet All Time Statecoin Count'),
        #             html.P(
        #                 '''All time total number of statecoins. See https://github.com/layer2tech/mercury-explorer/blob/main/api/API.md.''')
        #         ])
        #     ], width={"size": 6}),
        # ], justify="center")
    ]

    children = [

        dbc.Tabs([
            dbc.Tab(
                lightning_content,
                label='Lightning Network',
                tab_id='lightning'
            ),

            dbc.Tab(
                mercury_content,
                label='Mercury Wallet (Statechains)',
                tab_id='mercury'
            ),

        ], id='scaling-tabs', persistence=True)

    ]

    return children