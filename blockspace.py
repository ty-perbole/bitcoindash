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

    mempool_data_clean = pd.read_csv('data/mempool_data_clean.csv')
    mempool_data_clean_filter = mempool_data_clean.loc[
        (mempool_data_clean['date_granularity'] == date_granularity)
        & (mempool_data_clean['date_period'] >= start_date)
        & (mempool_data_clean['date_period'] <= end_date)
        ]

    blockspace_fee = chart_utils.two_axis_chart(
        cm_data_clean_filter, x_series='date_period', title='Block Space Price',
        y1_series='BlockSpacePrice', y1_series_title='Blockspace Price (Sats/Byte)', y1_series_axis_type=axis_type,
        y2_series='BlockSpacePriceUSD', y2_series_title='Blockspace Price (USD Cent/Byte)', y2_series_axis_type=axis_type,
        bars=len(cm_data_clean_filter) <= 60,
        halving_lines=True if date_granularity not in ['halving_era', 'market_cycle'] else False)

    security_spend = chart_utils.single_axis_chart(
        cm_data_clean_filter, x_series='date_period', y_series='SecuritySpendRatio',
        title='Security Spend Ratio', y_series_title='Security Spend Ratio',
        y_series_axis_type=axis_type,
        bars=len(cm_data_clean_filter) <= 90 or date_granularity not in ['day', 'week'],
        halving_lines=True if date_granularity not in ['halving_era', 'market_cycle'] else False)

    mempool = chart_utils.single_axis_chart(
        mempool_data_clean_filter, x_series='date_period', y_series='total_fee_btc',
        title='Block Space Fees Queued in Mempool (Stale data)', y_series_title='Total Block Space Fees (BTC)',
        y_series_axis_type='log', data_source='mempool.space',
        bars=len(mempool_data_clean_filter) <= 90 or date_granularity not in ['day', 'week'],
        halving_lines=True if date_granularity not in ['halving_era', 'market_cycle'] else False)

    tx_density = chart_utils.single_axis_chart(
        cm_data_clean_filter, x_series='date_period', y_series='TransactionDensity',
        title='Transaction Density', y_series_title='Value ($USD) Transacted per Byte',
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
                    figure=blockspace_fee,
                    id='blockspace_fee',
                    style={'height': CHART_HEIGHT}
                ),
                html.Details([
                    html.Summary('Tell me about Block Space Price'),
                    html.P('''
                    Block space price is calculated as the total blockspace fees paid in the period divided by the total blockspace bytes in the period. When demand for blockspace increases, the price should increase due to fixed supply. I should probably use vBytes instead of Bytes.''')
                ])
            ], width={"size": 6}),
            dbc.Col([
                dcc.Graph(
                    figure=security_spend,
                    id='security_spend',
                    style={'height': CHART_HEIGHT}
                ),
                html.Details([
                    html.Summary('Tell me about Security Spend Ratio'),
                    html.P('''
                    Security Spend Ratio is the ratio of BTC miner rewards (block subsidy + blockspace fees) to BTC current supply. This ratio shows the network security budget relative to it's value.''')
                ])
            ], width={"size": 6}),
        ], justify="center"),

        dbc.Row([
            dbc.Col([html.H4(" ")])
        ], justify="center"),

        dbc.Row([
            dbc.Col([
                dcc.Graph(
                    figure=mempool,
                    id='mempool',
                    style={'height': CHART_HEIGHT}
                ),
                html.Details([
                    html.Summary('Tell me about Block Space Fees Queued in Mempool'),
                    html.P('''
                    This metric tracks the amount of block space fees that are queued in the mempool. When demand for blockspace increases more transactions get queued in the mempool.''')
                ])
            ], width={"size": 6}),
            dbc.Col([
                dcc.Graph(
                    figure=tx_density,
                    id='tx_density',
                    style={'height': CHART_HEIGHT}
                ),
                html.Details([
                    html.Summary('Tell me about Transaction Density'),
                    html.P('''
                    Transaction density is the amount of $USD value transacted on the blockchain, per byte of blockspace. If blockspace becomes increasingly valuable we would expect it to be used for the highest value use cases. See: https://www.docdroid.net/FbgH1WS/bitcoin-institution-riga-pdf''')
                ])
            ], width={"size": 6}),
        ], justify="center")
    ]

    return children