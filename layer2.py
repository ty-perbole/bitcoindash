import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import pandas as pd
import chart_utils

CHART_HEIGHT = '400px'

def figures(start_date, end_date, date_granularity, axis_type):
    ln_data_clean = pd.read_csv('ln_data_clean.csv')
    ln_data_clean_filter = ln_data_clean.loc[
        (ln_data_clean['date_granularity'] == date_granularity)
      & (ln_data_clean['date_period'] >= start_date)
      & (ln_data_clean['date_period'] <= end_date)
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
        y_series_axis_type='log', data_source='ln.bigsun.xyz',
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

    children = [
        dbc.Row([
            dbc.Col([
                html.Details([
                    html.Summary('⚡️ How to grow L2 ⚡️', style={'fontSize': 26}),
                    dcc.Markdown('''
                            ### Run a Bitcoin Node!
                            Run a Bitcoin node, specifically one that has lightning support, open some lightning channels and use lightning. See these guides to learn more: [node.guide](http://node.guide/), https://www.bitcoinqna.com/lightning
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
                    html.P('''Total count of lightning nodes with at least one pubic channel open as of the date. Note from the data source "Why is the number of open channels here much bigger than other explorers show? Because we keep counting the channels as open until their funding transaction is spent on the chain. Apparently many channels are abandoned and nodes turned off, sometimes temporarily, and the channels remain technically open, but cease to be announced to the rest of the network. Other explorers remove these inactive channels from their count of open channels, but we don't." See: https://ln.bigsun.xyz/docs.''')
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
                    html.P('''A Herfindahl index is a common measure of concentration. This metric tries to quantify how much liquidity is dispersed among nodes in the Lightning Network. It is the Herfindahl index of total channel value per node.''')
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
                    html.P('''Total number of open **public** lightning channels as of the date. Many lightning channels are private, so this undercounts total channels in existence.''')
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
                    html.P('''Total value of all **public** lightning channels as of the date. Many lightning channels are private, so this undercounts total channels in existence.''')
                ])
            ], width={"size": 6}),
        ], justify="center")
    ]

    return children