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

    nc_data_clean = pd.read_csv('data/node_count_data_clean.csv')
    nc_data_clean_filter = nc_data_clean.loc[
        (nc_data_clean['date_granularity'] == date_granularity)
        & (nc_data_clean['date_period'] >= start_date)
        & (nc_data_clean['date_period'] <= end_date)
        ]

    hash_rate = chart_utils.single_axis_chart(
        cm_data_clean_filter, x_series='date_period', y_series='HashRate',
        title='Hash Rate', y_series_title='Hash Rate (EH/s)',
        y_series_axis_type=axis_type,
        bars=len(cm_data_clean_filter) <= 90 and date_granularity != 'day',
        halving_lines=True if date_granularity not in ['halving_era', 'market_cycle'] else False,
        confidence_interals=['HashRateLower', 'HashRateUpper', 'HashRateL7D'] if date_granularity == 'day' else False)

    node_count = chart_utils.single_axis_chart(
        nc_data_clean_filter, x_series='date_period', y_series='total_nodes',
        title='Bitcoin Node Count', y_series_title='Number of Bitcoin Nodes',
        y_series_axis_type=axis_type, data_source='luke.dashjr.org',
        bars=len(cm_data_clean_filter) <= 90 or date_granularity not in ['day', 'week'],
        halving_lines=True if date_granularity not in ['halving_era', 'market_cycle'] else False)

    chain_rewrite_days = chart_utils.single_axis_chart(
        cm_data_clean_filter, x_series='date_period', y_series='ChainRewriteDays',
        title='Chain Rewrite Days at Period Hash Rate', y_series_title='Days to Rewrite Chain',
        y_series_axis_type=axis_type,
        bars=len(cm_data_clean_filter) <= 90 or date_granularity not in ['day', 'week'],
        halving_lines=True if date_granularity not in ['halving_era', 'market_cycle'] else False)

    dollars_per_yh = chart_utils.single_axis_chart(
        cm_data_clean_filter, x_series='date_period', y_series='DollarsPerYH',
        title='Hash Price: $USD per Yottahash', y_series_title='$USD per Yottahash',
        y_series_axis_type=axis_type,# y_series_axis_format='1.00e1',
        bars=len(cm_data_clean_filter) <= 90 or date_granularity not in ['day', 'week'],
        halving_lines=True if date_granularity not in ['halving_era', 'market_cycle'] else False)

    children = [
        dbc.Row([
            dbc.Col([
                html.Details([
                    html.Summary('⛓️ How to improve Bitcoin security ⛓️', style={'fontSize': 26}),
                    dcc.Markdown('''
                    ### Run a Bitcoin Node!
                    The best way to improve Bitcoin's security as an individual is to run your own Bitcoin node. See this guide to learn more: [node.guide](http://node.guide/)

                    ### Hold your own private keys!
                    See this guide: https://bitcoiner.guide/qna/wallets/
                    ''')
                ]),
            ]),
        ], justify="center"),

        dbc.Row([
            dbc.Col([
                html.Details([
                    html.Summary('📖 Read more about the Security KPIs️', style={'fontSize': 26}),
                    dcc.Markdown('''I wrote a deep dive into these security metrics at Stack Stats. [Click here](https://typerbole.substack.com/p/bitcoin-kpis-security) to learn more about why I chose these metrics and learn about the trends.''')
                ]),
            ]),
        ], justify="center"),

        dbc.Row([
            dbc.Col([
                dcc.Graph(
                    figure=hash_rate,
                    id='hash_rate',
                    style={'height': CHART_HEIGHT}
                ),
                html.Details([
                    html.Summary('Tell me about Hash Rate'),
                    html.P('''
                    Hash Rate is measured in EH/s. From CoinMetrics: "The mean rate at which miners are solving hashes that day. Hash rate is the speed at which computations are being completed across all miners in the network." 95% Poisson confidence bands on the daily chart are shown to demonstrate the uncertainty in the daily measurement of Hash Rate.''')
                ])
            ], width={"size": 6}),
            dbc.Col([
                dcc.Graph(
                    figure=node_count,
                    id='node_count',
                    style={'height': CHART_HEIGHT}
                ),
                html.Details([
                    html.Summary('Tell me about Node Count'),
                    html.P('''
                    The node count metric is provided by Luke Dashjr. From CoinDesk: "Tallying the number of Bitcoin nodes typically relies on estimates instead of concrete data, and opinions on the best methodology for deriving these estimates differ. Dashjr’s estimate relies on a tedious and undisclosed proprietary methodology that could compromise the reliability of the data if it was released, according to its creator. See: https://www.coindesk.com/bitcoin-node-count-falls-to-3-year-low-despite-price-surge"''')
                ])
            ], width={"size": 6}),
        ], justify="center"),

        dbc.Row([
            dbc.Col([html.H4(" ")])
        ], justify="center"),

        dbc.Row([
            dbc.Col([
                dcc.Graph(
                    figure=chain_rewrite_days,
                    id='chain_rewrite_days',
                    style={'height': CHART_HEIGHT}
                ),
                html.Details([
                    html.Summary('Tell me about Chain Rewrite Days'),
                    html.P('''
                    Chain Rewrite days is the number of days it would take to rewrite the entire Bitcoin blockchain using the current level of hashpower. It is calculated by dividing the cumulative hash by the current rate.''')
                ])
            ], width={"size": 6}),
            dbc.Col([
                dcc.Graph(
                    figure=dollars_per_yh,
                    id='dollars_per_yh',
                    style={'height': CHART_HEIGHT}
                ),
                html.Details([
                    html.Summary('Tell me about $USD per Yottahash'),
                    html.P('''
                            $USD per Yottahash is the amount miners are compensated in block rewards and fees for each Yottahash they produce during the period.''')
                ])
            ], width={"size": 6}),
        ], justify="center")
    ]

    return children