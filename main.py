import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import datetime
from flask import Flask, Response
import gc

import value, blockspace, security, privacy, layer2, cycles

server = Flask(__name__)
app = dash.Dash(__name__, server=server, external_stylesheets=[dbc.themes.SLATE], eager_loading=True)
app.title = 'Bitcoin KPIs'

app.layout = dbc.Container([
    dcc.Location(id='url-input', refresh=False),
    dcc.Location(id='url-output', refresh=False),
    html.H1("Bitcoin KPIs"),

    dbc.Container([
        dbc.Row([
                dbc.Col(html.H4("Date Range"), width=4),
                dbc.Col(html.H4("Date Granularity"), width=3),
                dbc.Col(html.H4("Log/Linear"), width=3)
            ], justify="center"),

        dbc.Row([
            dbc.Col(dcc.DatePickerRange(
                id='date-picker-range',
                min_date_allowed=datetime.date(2009, 1, 3),
                max_date_allowed=datetime.datetime.now() - datetime.timedelta(1),
                start_date=datetime.datetime.now() - datetime.timedelta(365*4),
                end_date=datetime.datetime.now()
            ), width={"size": 4}),

            dbc.Col(
                dcc.Dropdown(
                    id='date-granularity-picker',
                    options=[
                        {'label': 'Daily', 'value': 'day'},
                        {'label': 'Weekly', 'value': 'week'},
                        {'label': 'RHR Mode (Weekly Thurs-Weds)', 'value': 'rhr_week'},
                        {'label': 'Monthly', 'value': 'month'},
                        {'label': 'Yearly', 'value': 'year'},
                        {'label': 'Halving Era', 'value': 'halving_era'},
                        {'label': 'Market Cycle', 'value': 'market_cycle'}
                    ],
                    value='week'
                ), width={"size": 3}),

            dbc.Col(
                dcc.Dropdown(
                    id='log-linear-picker',
                    options=[
                        {'label': 'Log Scale', 'value': 'log'},
                        {'label': 'Linear Scale', 'value': 'linear'}
                    ],
                    value='linear'
                ), width={"size": 3})
        ], justify="center"),

        dbc.Row([
                dbc.Col([html.H4(" ")])
        ], justify="center"),

        dbc.Row([

            # dbc.Col(
            #     html.H4("KPI Snapshot as of {}".format('do this')),
            #     width={"size": 2}
            # ),

            dbc.Col([
                dbc.Tabs([
                    dbc.Tab(
                        label='🔒 Security',
                        tab_id='security'
                    ),

                    dbc.Tab(
                        label='📈 Block Space Economics',
                        tab_id='blockspace'
                    ),

                    dbc.Tab(
                        label='💰 Value & Uptake',
                        tab_id='value'
                    ),

                    dbc.Tab(
                        label='😎 Privacy & Fungibility',
                        tab_id='privacy'
                    ),

                    dbc.Tab(
                        label='⚡ Layer 2',
                        tab_id='layer2'
                    ),

                    dbc.Tab(
                        label='🔄 Cycles Comparison',
                        tab_id='cycles'
                    ),

                    dbc.Tab(
                        label='✏️ Stack Stats️',
                        tab_id='stack-stats',
                        tab_style={"color": 'rgb(242, 169, 0)'},
                        label_style={"color": 'rgb(242, 169, 0)'}
                    ),

                    dbc.Tab(
                        label='🤔 About',
                        tab_id='about',
                        # tab_style={"color": 'rgb(0, 128, 0)'},
                        # label_style={"color": 'rgb(0, 128, 0)'}
                    ),

                    dbc.Tab(
                        label='🤲 Donate',
                        tab_id='donate',
                        # tab_style={"color": 'rgb(242, 169, 0)'},
                        # label_style={"color": 'rgb(242, 169, 0)'}
                    ),
                ], id='tabs'),
                dbc.Container(id='tabs-content', fluid=True)
            ])#, width={"size": 10}
        ], justify="center")
    ], fluid=True)
], fluid=True)

@app.callback(
    [Output('date-picker-range', 'start_date'),
     Output('date-picker-range', 'end_date'),
     Output('log-linear-picker', 'value')],
    [Input('date-granularity-picker', 'value')])
def set_inputs_on_granularity(date_granularity):
    if date_granularity in ('day', 'week'):
        return [datetime.datetime.now() - datetime.timedelta(365), datetime.datetime.now() - datetime.timedelta(1), 'linear']
    elif date_granularity == 'rhr_week':
        return [datetime.datetime.now() - datetime.timedelta(28 * 6), datetime.datetime.now() - datetime.timedelta(1), 'linear']
    elif date_granularity == 'month':
        return [datetime.datetime.now() - datetime.timedelta(365 * 2), datetime.datetime.now() - datetime.timedelta(1), 'linear']
    elif date_granularity == 'year':
        return [datetime.datetime.now() - datetime.timedelta(365 * 10), datetime.datetime.now() - datetime.timedelta(1), 'log']
    return [datetime.date(2009, 1, 3), datetime.datetime.now(), 'log']

@app.callback(Output('url-output', 'pathname'), Input('tabs', 'active_tab'))
def update_url_by_tab(value):
    return f"/{value}"

@app.callback(Output('tabs', 'active_tab'), Input('url-input', 'pathname'))
def update_tab_by_url(pathname):
    return pathname[1:]

@app.callback(Output('tabs-content', 'children'),
              [Input('tabs', 'active_tab'),
               Input('date-picker-range', 'start_date'),
               Input('date-picker-range', 'end_date'),
               Input('date-granularity-picker', 'value'),
               Input('log-linear-picker', 'value')])
def render_content(tab, start_date, end_date, date_granularity, log_linear):
    gc.collect()
    if tab == 'value':
        return value.figures(start_date, end_date, date_granularity, log_linear)
    elif tab == 'blockspace':
        return blockspace.figures(start_date, end_date, date_granularity, log_linear)
    elif tab == 'security':
        return security.figures(start_date, end_date, date_granularity, log_linear)
    elif tab == 'privacy':
        return privacy.figures(start_date, end_date, date_granularity, log_linear)
    elif tab == 'layer2':
        return layer2.figures(start_date, end_date, date_granularity, log_linear)
    elif tab == 'cycles':
        return cycles.figures()
    elif tab == 'donate':
        return html.Div([
            dcc.Markdown('''
                # Donate to Bitcoin development
                Please consider supporting Bitcoin development by making a donation to a developer working on improving the network.
                - See https://bitcoindevlist.com/ for some excellent suggestions.
                - Or donate to the HRF privacy dev fund: https://hrf.org/programs_posts/devfund/
                
                # Other ways to contribute
                - Run a node: https://www.bitcoinqna.com/node
                - Normalize financial privacy: https://www.bitcoinqna.com/coinjoin
                - Use lightning: https://www.bitcoinqna.com/lightning 
                ''')
        ])
    elif tab == 'stack-stats':
        return html.Div([
            dcc.Markdown('''
                # Stack Stats
                I write about Bitcoin data analysis on my newsletter [Stack Stats](http://stack-stats.com).
                - Please consider signing up for some free Bitcoin data insights: http://stack-stats.com
                - You can also find me on [twitter](https://twitter.com/typerbole).
                - Or email me at my twitter handle at pm dot me
                ''')
        ])
    elif tab == 'about':
        return dcc.Markdown('''
                # About
                The goal of this dashboard is to help the Bitcoin community focus on the important metrics & KPIs that I think are most correlated with the success of the network and ecosystem.
                I saw a gap in the current offerings, where no one data source had all the things I wanted:
                - Focus on Bitcoin
                - Historical data
                - Data from multiple sources: on-chain, lightning, coinjoin, mempool, node count
                - Distilled to only the most important factors for network and ecosystem success, rather than NgU or trading
                
                I hope you find it useful.
                ''')
    else:
        return security.figures(start_date, end_date, date_granularity, log_linear)

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8080)
