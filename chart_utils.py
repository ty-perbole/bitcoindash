import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

def single_axis_chart(df, x_series, y_series, **kwargs):
    fig = make_subplots(
        specs=[[{"secondary_y": False}]]
    )

    if kwargs.get('bars', False):
        fig.add_bar(
            x=df[x_series], y=df[y_series], name=y_series, marker_color=kwargs.get('marker_color', 'rgb(242, 169, 0)'),
            text=["{:.2%} Δ".format(x) if np.isfinite(x) else '' for x in df[y_series].pct_change()],
            textposition='auto',
        )
    else:
        if isinstance(y_series, str):
            fig.add_trace(
                go.Scatter(x=df[x_series], y=df[y_series], name=y_series, marker_color=kwargs.get('marker_color', 'rgb(242, 169, 0)')),
                secondary_y=False
            )
        elif isinstance(y_series, list):
            for y1 in y_series:
                # First trace
                fig.add_trace(
                    go.Scatter(x=df[x_series], y=df[y1], name=y1),
                    secondary_y=False
                )

    # Add figure title
    fig.update_layout(
        title_text=kwargs.get('title', kwargs.get('y_series_title', y_series)),
    )

    # Set x-axis title
    if kwargs.get('x_axis_title'):
        fig.update_xaxes(title_text=kwargs.get('x_axis_title'))

    fig.update_layout(
        annotations=[
            dict(x=1, y=-0.2,
                 text="Data: {}".format(kwargs.get('data_source', 'CoinMetrics')),
                 showarrow=False, xref='paper', yref='paper',
                 xanchor='right', yanchor='auto', xshift=0, yshift=0)
        ],
        showlegend=False,
        legend_orientation="h",
        template="plotly_dark",
        hovermode='x unified',
        xaxis_showgrid=False,
        yaxis_showgrid=False
    )

    # Set y-axes titles
    fig.update_yaxes(
        title_text=kwargs.get('y_series_title', y_series), secondary_y=False, tickformat=kwargs.get('y_series_axis_format', None),
        type=kwargs.get('y_series_axis_type', 'linear'), range=kwargs.get('y_series_axis_range'),
        showgrid=False
    )

    if kwargs.get('halving_lines', False):
        min_date, max_date = df[x_series].min(), df[x_series].max()
        for halving_date in ['2012-11-29', '2016-07-10', '2020-05-11']:
            try:
                if min_date <= halving_date <= max_date:
                    axis_min = 0 if kwargs.get('y_series_axis_type', 'linear') == 'linear' else df[y_series].min()
                    fig.add_trace(go.Scatter(
                        x=[halving_date, halving_date],
                        y=[axis_min, df[y_series].max()],
                        mode="lines",
                        showlegend=False,
                        line=dict(width=2, color='white', dash="dot"),
                        name='{} Halving'.format(halving_date)
                    ),
                        secondary_y=False
                    )
            except TypeError:
                pass

    return fig

def two_axis_chart(df, x_series, y1_series, y2_series, **kwargs):
    """
        Plot a two axis chart using Plotly library

        Arguments:
        df (dataframe): Pandas dataframe containing CoinMetrics community data
        x_series (string): Column name for x series, typically 'Date'
        y1_series (string, list): Column name, or list of column names, to plot on the left Y axis
        y2_series (string): Column name to plot on the right Y axis, typically 'price_usd'

        Keyword arguments:
        title (string): Title for the plot
        x_axis_title (string): Title for X axis, defaults to string from x_series
        y1_series_axis_type (string): Left Y axis type. Default is 'log'. Other sane option: 'linear'
        y1_series_axis_range (list): Range for left Y axis. When axis type is log, range values represent powers of 10
        y2_series_axis_type (string): Right Y axis type. Default is 'log'. Other sane option: 'linear'
        y2_series_axis_range (list): Range for right Y axis. When axis type is log, range values represent powers of 10
        y1_upper_thresh (float): Upper threshold for highlighting regions with extreme values for Y1 series
        y1_lower_thresh (float): Lower threshold for highlighting regions with extreme values for Y1 series
        thresh_inverse (bool): When true, high values of a ratio metric are highlighted green. When false, high values
            indicate poor fundamentals and are highlighted red. Inverse logic for lower threshold.

        Returns:
            Plotly figure

        """
    # Create figure with secondary y-axis
    fig = make_subplots(
        specs=[[{"secondary_y": True}]]
    )

    if isinstance(y1_series, str):
        y1_series_title = y1_series
        y1_series = [y1_series]
    elif isinstance(y1_series, list):
        if "Roll" in y1_series[0]:
            y1_series_title = y1_series[0][: y1_series[0].find("Roll")]
        else:
            y1_series_title = y1_series[0]

    if kwargs.get('y1_series_title'):
        y1_series_title = kwargs.get('y1_series_title')

    for y1 in y1_series:
        if kwargs.get('bars', False):
            fig.add_bar(
                x=df[x_series], y=df[y1], name=y1, marker_color='rgb(242, 169, 0)',
                text=["{:.2%} Δ".format(x) if np.isfinite(x) else '' for x in df[y1].pct_change()],
                textposition='auto', offsetgroup=1
            )
        else:
            # First trace
            fig.add_trace(
                go.Scatter(x=df[x_series], y=df[y1], name=y1, marker_color='rgb(242, 169, 0)'),
                secondary_y=False
            )

    # Second trace
    if kwargs.get('bars', False):
        fig.add_bar(
            x=df[x_series], y=df[y2_series], name=y2_series, marker_color='aqua',
            text=["{:.2%} Δ".format(x) if np.isfinite(x) else '' for x in df[y2_series].pct_change()],
            textposition='auto', offsetgroup=2,
            secondary_y=True
        )
    else:
        # First trace
        fig.add_trace(
            go.Scatter(x=df[x_series], y=df[y2_series], name=y2_series, marker_color='aqua'),
            secondary_y=True
        )

    # Add figure title
    fig.update_layout(
        title_text=kwargs.get('title', y1_series_title),
    )

    # Set x-axis title
    if kwargs.get('x_axis_title'):
        fig.update_xaxes(title_text=kwargs.get('x_axis_title'))

    if kwargs.get('y1_upper_thresh') or kwargs.get('y1_lower_thresh'):
        highlight_shapes = []

        if kwargs.get('y1_upper_thresh'):
            highlight_shapes.extend(create_highlighted_region_shapes(
                get_threshold_dates(df, x_series, y1_series[0], kwargs.get('y1_upper_thresh'), upper_bound=True),
                fillcolor=('LightGreen' if kwargs.get('thresh_inverse', False) else 'LightSalmon')
                )
            )

        if kwargs.get('y1_lower_thresh'):
            highlight_shapes.extend(create_highlighted_region_shapes(
                get_threshold_dates(df, x_series, y1_series[0], kwargs.get('y1_lower_thresh'), upper_bound=False),
                fillcolor=('LightSalmon' if kwargs.get('thresh_inverse', False) else 'LightGreen')
                )
            )

        fig.update_layout(
            shapes=highlight_shapes
        )

    fig.update_layout(
        annotations=[
            dict(x=1, y=-0.3,
                 text="Data: {}".format(kwargs.get('data_source', 'CoinMetrics')),
                 showarrow=False, xref='paper', yref='paper',
                 xanchor='right', yanchor='auto', xshift=0, yshift=0)
        ],
        showlegend=True,
        legend_orientation="h",
        template="plotly_dark",
        hovermode='x unified',
        xaxis_showgrid=False,
        yaxis_showgrid=False
    )

    # Set y-axes titles
    fig.update_yaxes(
        title_text=y1_series_title, secondary_y=False,
        tickformat=kwargs.get('y1_series_axis_format', None),
        type=kwargs.get('y1_series_axis_type', 'linear'), range=kwargs.get('y1_series_axis_range'),
        showgrid=False
    )

    fig.update_yaxes(
        title_text=kwargs.get('y2_series_title', y2_series), secondary_y=True,
        tickformat=kwargs.get('y2_series_axis_format', None),
        type=kwargs.get('y2_series_axis_type', 'linear'), range=kwargs.get('y2_series_axis_range'),
        showgrid=False
    )

    if kwargs.get('halving_lines', False):
        min_date, max_date = df[x_series].min(), df[x_series].max()
        for halving_date in ['2012-11-29', '2016-07-10', '2020-05-11']:
            if min_date <= halving_date <= max_date:
                fig.add_trace(go.Scatter(
                    x=[halving_date, halving_date],
                    y=[df[y2_series].min(), df[y2_series].max()],
                    mode="lines",
                    showlegend=False,
                    line=dict(width=2, color='white', dash="dot"),
                    name='{} Halving'.format(halving_date)
                ),
                    secondary_y=True
                )

    return fig

def hodl_waves_chart(df, version='value', **kwargs):
    """
            Plot a two axis chart using Plotly library

            Arguments:
            df (dataframe): Pandas dataframe containing HODL waves dataframe from 02_HODLWaves.ipynb notebook
            version: Can plot HODL waves by TXO value ('value), by total count of TXO ('count'),
                     and by TXO with balance > 0.01 BTC ('count_filter')

            Returns:
                Plotly figure

            """
    x = df['date_period']
    fig = make_subplots(
        specs=[[{"secondary_y": True}]],
    )

    fig.add_trace(go.Scatter(
        x=x, y=df['utxo_{}_under_1d'.format(version)],
        mode='lines',
        line=dict(width=0.5, color='rgb(0, 0, 0)'),
        fillcolor='rgb(229.0, 89.0, 52.0)',
        fill='tonexty',
        name='<1d',
        stackgroup='one',
        groupnorm='percent'  # sets the normalization for the sum of the stackgroup
    ))

    fig.add_trace(go.Scatter(
        x=x, y=df['utxo_{}_1d_1w'.format(version)],
        mode='lines',
        line=dict(width=0.5, color='rgb(0, 0, 0)'),
        fillcolor='rgb(228.8, 112.0, 52.6)',
        fill='tonexty',
        name='1d-1w',
        stackgroup='one',
    ))

    fig.add_trace(go.Scatter(
        x=x, y=df['utxo_{}_1w_1m'.format(version)],
        mode='lines',
        line=dict(width=0.5, color='rgb(0, 0, 0)'),
        fillcolor='rgb(228.6, 135.0, 53.2)',
        fill='tonexty',
        name='1w-1m',
        stackgroup='one',
    ))

    fig.add_trace(go.Scatter(
        x=x, y=df['utxo_{}_1m_3m'.format(version)],
        mode='lines',
        line=dict(width=0.5, color='rgb(0, 0, 0)'),
        fillcolor='rgb(228.4, 158.0, 53.8)',
        fill='tonexty',
        name='1m-3m',
        stackgroup='one',
    ))

    fig.add_trace(go.Scatter(
        x=x, y=df['utxo_{}_3m_6m'.format(version)],
        mode='lines',
        line=dict(width=0.5, color='rgb(0, 0, 0)'),
        fillcolor='rgb(228.2, 181.0, 54.4)',
        fill='tonexty',
        name='3m-6m',
        stackgroup='one',
    ))

    fig.add_trace(go.Scatter(
        x=x, y=df['utxo_{}_6m_12m'.format(version)],
        mode='lines',
        line=dict(width=0.5, color='rgb(0, 0, 0)'),
        fillcolor='rgb(228.0, 204.0, 55.0)',
        fill='tonexty',
        name='6m-12m',
        stackgroup='one',
    ))

    fig.add_trace(go.Scatter(
        x=x, y=df['utxo_{}_12m_18m'.format(version)],
        mode='lines',
        line=dict(width=0.5, color='rgb(0, 0, 0)'),
        fillcolor='rgb(182.4, 192.0, 82.2)',
        fill='tonexty',
        name='12m-18m',
        stackgroup='one',
    ))

    fig.add_trace(go.Scatter(
        x=x, y=df['utxo_{}_18m_24m'.format(version)],
        mode='lines',
        line=dict(width=0.5, color='rgb(0, 0, 0)'),
        fillcolor='rgb(136.8, 180.0, 109.4)',
        fill='tonexty',
        name='18m-2y',
        stackgroup='one',
    ))

    fig.add_trace(go.Scatter(
        x=x, y=df['utxo_{}_2y_3y'.format(version)],
        mode='lines',
        line=dict(width=0.5, color='rgb(0, 0, 0)'),
        fillcolor='rgb(91.2, 168.0, 136.6)',
        fill='tonexty',
        name='2y-3y',
        stackgroup='one',
    ))

    fig.add_trace(go.Scatter(
        x=x, y=df['utxo_{}_3y_5y'.format(version)],
        mode='lines',
        line=dict(width=0.5, color='rgb(0, 0, 0)'),
        fillcolor='rgb(45.6, 156.0, 163.8)',
        fill='tonexty',
        name='3y-5y',
        stackgroup='one',
    ))

    fig.add_trace(go.Scatter(
        x=x, y=df['utxo_{}_5y_8y'.format(version)],
        mode='lines',
        line=dict(width=0.5, color='rgb(0, 0, 0)'),
        fillcolor='rgb(0.0, 144.0, 191.0)',
        fill='tonexty',
        name='5y-8y',
        stackgroup='one',
    ))

    fig.add_trace(go.Scatter(
        x=x, y=df['utxo_{}_greater_8y'.format(version)],
        mode='lines',
        line=dict(width=0.5, color='rgb(0, 0, 0)'),
        fillcolor='rgb(0.0, 100.0, 130.0)',
        fill='tonexty',
        name='>8y',
        stackgroup='one',
    ))

    fig.update_layout(
        showlegend=True,
        legend_orientation="h",
        yaxis=dict(
            type='linear',
            range=[1, 100],
            ticksuffix='%'))

    # Second trace
    fig.add_trace(go.Scatter(
        x=x, y=df['price_usd'],
        name='price_usd',
        mode='lines',
        line=dict(width=2, color='rgb(255, 255, 255)'),
    ),
        secondary_y=True,
    )

    if kwargs.get('halving_lines', False):
        min_date, max_date = x.min(), x.max()
        for halving_date in ['2012-11-29', '2016-07-10', '2020-05-11']:
            if min_date <= halving_date <= max_date:
                fig.add_trace(go.Scatter(
                    x=[halving_date, halving_date],
                    y=[0, 1000000],
                    mode="lines",
                    showlegend=False,
                    line=dict(width=2, color='white', dash="dot"),
                    name='{} Halving'.format(halving_date)
                ))

    fig.update_yaxes(
        title_text='Price ($USD)', secondary_y=True, tickformat="${n},",
        type='log', range=[-2, 5],
        showgrid=False
    )

    # Add figure title
    fig.update_layout(
        title_text='HODL Waves: {} weighted'.format('RealizedCap' if version == 'realcap' else version),
        # annotations=[
        #     dict(x=1, y=-0.5,
        #          text="Data Source: Proprietary",
        #          showarrow=False, xref='paper', yref='paper',
        #          xanchor='right', yanchor='auto', xshift=0, yshift=0)
        # ],
        hovermode='x unified',
        template="plotly_dark",
        legend_orientation="v",
        showlegend=False,
        xaxis_showgrid=False,
        yaxis_showgrid=False
    )

    return fig

def hodl_waves_chart2(df, **kwargs):
    """
            Plot a two axis chart using Plotly library

            Arguments:
            df (dataframe): Pandas dataframe containing HODL waves dataframe from 02_HODLWaves.ipynb notebook

            Returns:
                Plotly figure

            """
    x = df['date_period']
    fig = make_subplots(
        specs=[[{"secondary_y": True}]],
    )

    fig.add_trace(go.Scatter(
        x=x, y=df['24h_rc'],
        mode='lines',
        line=dict(width=0.5, color='rgb(0, 0, 0)'),
        fillcolor='rgb(229.0, 89.0, 52.0)',
        fill='tonexty',
        name='<1d',
        stackgroup='one',
        groupnorm='percent'  # sets the normalization for the sum of the stackgroup
    ))

    fig.add_trace(go.Scatter(
        x=x, y=df['1d_1w_rc'],
        mode='lines',
        line=dict(width=0.5, color='rgb(0, 0, 0)'),
        fillcolor='rgb(228.8, 112.0, 52.6)',
        fill='tonexty',
        name='1d-1w',
        stackgroup='one',
    ))

    fig.add_trace(go.Scatter(
        x=x, y=df['1w_1m_rc'],
        mode='lines',
        line=dict(width=0.5, color='rgb(0, 0, 0)'),
        fillcolor='rgb(228.6, 135.0, 53.2)',
        fill='tonexty',
        name='1w-1m',
        stackgroup='one',
    ))

    fig.add_trace(go.Scatter(
        x=x, y=df['1m_3m_rc'],
        mode='lines',
        line=dict(width=0.5, color='rgb(0, 0, 0)'),
        fillcolor='rgb(228.4, 158.0, 53.8)',
        fill='tonexty',
        name='1m-3m',
        stackgroup='one',
    ))

    fig.add_trace(go.Scatter(
        x=x, y=df['3m_6m_rc'],
        mode='lines',
        line=dict(width=0.5, color='rgb(0, 0, 0)'),
        fillcolor='rgb(228.2, 181.0, 54.4)',
        fill='tonexty',
        name='3m-6m',
        stackgroup='one',
    ))

    fig.add_trace(go.Scatter(
        x=x, y=df['6m_12m_rc'],
        mode='lines',
        line=dict(width=0.5, color='rgb(0, 0, 0)'),
        fillcolor='rgb(228.0, 204.0, 55.0)',
        fill='tonexty',
        name='6m-12m',
        stackgroup='one',
    ))

    fig.add_trace(go.Scatter(
        x=x, y=df['1y_2y_rc'],
        mode='lines',
        line=dict(width=0.5, color='rgb(0, 0, 0)'),
        fillcolor='rgb(182.4, 192.0, 82.2)',
        fill='tonexty',
        name='1y-2y',
        stackgroup='one',
    ))

    fig.add_trace(go.Scatter(
        x=x, y=df['2y_3y_rc'],
        mode='lines',
        line=dict(width=0.5, color='rgb(0, 0, 0)'),
        fillcolor='rgb(136.8, 180.0, 109.4)',
        fill='tonexty',
        name='2y-3y',
        stackgroup='one',
    ))

    fig.add_trace(go.Scatter(
        x=x, y=df['3y_5y_rc'],
        mode='lines',
        line=dict(width=0.5, color='rgb(0, 0, 0)'),
        fillcolor='rgb(91.2, 168.0, 136.6)',
        fill='tonexty',
        name='3y-5y',
        stackgroup='one',
    ))

    fig.add_trace(go.Scatter(
        x=x, y=df['5y_7y_rc'],
        mode='lines',
        line=dict(width=0.5, color='rgb(0, 0, 0)'),
        fillcolor='rgb(45.6, 156.0, 163.8)',
        fill='tonexty',
        name='5y-7y',
        stackgroup='one',
    ))

    fig.add_trace(go.Scatter(
        x=x, y=df['7y_10y_rc'],
        mode='lines',
        line=dict(width=0.5, color='rgb(0, 0, 0)'),
        fillcolor='rgb(0.0, 144.0, 191.0)',
        fill='tonexty',
        name='7y-10y',
        stackgroup='one',
    ))

    fig.add_trace(go.Scatter(
        x=x, y=df['more_10y_rc'],
        mode='lines',
        line=dict(width=0.5, color='rgb(0, 0, 0)'),
        fillcolor='rgb(0.0, 100.0, 130.0)',
        fill='tonexty',
        name='>10y',
        stackgroup='one',
    ))

    fig.update_layout(
        showlegend=True,
        legend_orientation="h",
        yaxis=dict(
            type='linear',
            range=[1, 100],
            ticksuffix='%'))

    # Second trace
    fig.add_trace(go.Scatter(
        x=x, y=df['PriceUSD'],
        name='Price ($USD)',
        mode='lines',
        line=dict(width=2, color='rgb(255, 255, 255)'),
    ),
        secondary_y=True,
    )

    if kwargs.get('halving_lines', False):
        min_date, max_date = x.min(), x.max()
        for halving_date in ['2012-11-29', '2016-07-10', '2020-05-11']:
            if min_date <= halving_date <= max_date:
                fig.add_trace(go.Scatter(
                    x=[halving_date, halving_date],
                    y=[0, 1000000],
                    mode="lines",
                    showlegend=False,
                    line=dict(width=2, color='white', dash="dot"),
                    name='{} Halving'.format(halving_date)
                ))

    fig.update_yaxes(
        title_text='Price ($USD)', secondary_y=True, tickformat="${n},",
        type='log', range=[-2, 5],
        showgrid=False
    )

    # Add figure title
    fig.update_layout(
        title_text='RealCap Weighted HODL Waves',
        # annotations=[
        #     dict(x=1, y=-0.5,
        #          text="Data Source: Proprietary",
        #          showarrow=False, xref='paper', yref='paper',
        #          xanchor='right', yanchor='auto', xshift=0, yshift=0)
        # ],
        hovermode='x unified',
        template="plotly_dark",
        legend_orientation="v",
        showlegend=False,
        xaxis_showgrid=False,
        yaxis_showgrid=False
    )

    return fig

def hodl_waves_chart2(df, **kwargs):
    """
            Plot a two axis chart using Plotly library

            Arguments:
            df (dataframe): Pandas dataframe containing HODL waves dataframe from 02_HODLWaves.ipynb notebook

            Returns:
                Plotly figure

            """
    version = 'realcap'
    x = df['date_period']
    fig = make_subplots(
        specs=[[{"secondary_y": True}]],
    )

    fig.add_trace(go.Scatter(
        x=x, y=df['utxo_{}_under_1d'.format(version)],
        mode='lines',
        line=dict(width=0.5, color='rgb(0, 0, 0)'),
        fillcolor='rgb(229.0, 89.0, 52.0)',
        fill='tonexty',
        name='<1d',
        stackgroup='one',
        groupnorm='percent'  # sets the normalization for the sum of the stackgroup
    ))

    fig.add_trace(go.Scatter(
        x=x, y=df['utxo_{}_1d_1w'.format(version)],
        mode='lines',
        line=dict(width=0.5, color='rgb(0, 0, 0)'),
        fillcolor='rgb(228.8, 112.0, 52.6)',
        fill='tonexty',
        name='1d-1w',
        stackgroup='one',
    ))

    fig.add_trace(go.Scatter(
        x=x, y=df['utxo_{}_1w_1m'.format(version)],
        mode='lines',
        line=dict(width=0.5, color='rgb(0, 0, 0)'),
        fillcolor='rgb(228.6, 135.0, 53.2)',
        fill='tonexty',
        name='1w-1m',
        stackgroup='one',
    ))

    fig.add_trace(go.Scatter(
        x=x, y=df['utxo_{}_1m_3m'.format(version)],
        mode='lines',
        line=dict(width=0.5, color='rgb(0, 0, 0)'),
        fillcolor='rgb(228.4, 158.0, 53.8)',
        fill='tonexty',
        name='1m-3m',
        stackgroup='one',
    ))

    fig.add_trace(go.Scatter(
        x=x, y=df['utxo_{}_3m_6m'.format(version)],
        mode='lines',
        line=dict(width=0.5, color='rgb(0, 0, 0)'),
        fillcolor='rgb(228.2, 181.0, 54.4)',
        fill='tonexty',
        name='3m-6m',
        stackgroup='one',
    ))

    fig.add_trace(go.Scatter(
        x=x, y=df['utxo_{}_6m_12m'.format(version)],
        mode='lines',
        line=dict(width=0.5, color='rgb(0, 0, 0)'),
        fillcolor='rgb(228.0, 204.0, 55.0)',
        fill='tonexty',
        name='6m-12m',
        stackgroup='one',
    ))

    fig.add_trace(go.Scatter(
        x=x, y=df['utxo_{}_12m_18m'.format(version)],
        mode='lines',
        line=dict(width=0.5, color='rgb(0, 0, 0)'),
        fillcolor='rgb(182.4, 192.0, 82.2)',
        fill='tonexty',
        name='12m-18m',
        stackgroup='one',
    ))

    fig.add_trace(go.Scatter(
        x=x, y=df['utxo_{}_18m_24m'.format(version)],
        mode='lines',
        line=dict(width=0.5, color='rgb(0, 0, 0)'),
        fillcolor='rgb(136.8, 180.0, 109.4)',
        fill='tonexty',
        name='18m-2y',
        stackgroup='one',
    ))

    fig.add_trace(go.Scatter(
        x=x, y=df['utxo_{}_2y_3y'.format(version)],
        mode='lines',
        line=dict(width=0.5, color='rgb(0, 0, 0)'),
        fillcolor='rgb(91.2, 168.0, 136.6)',
        fill='tonexty',
        name='2y-3y',
        stackgroup='one',
    ))

    fig.add_trace(go.Scatter(
        x=x, y=df['utxo_{}_3y_5y'.format(version)],
        mode='lines',
        line=dict(width=0.5, color='rgb(0, 0, 0)'),
        fillcolor='rgb(45.6, 156.0, 163.8)',
        fill='tonexty',
        name='3y-5y',
        stackgroup='one',
    ))

    fig.add_trace(go.Scatter(
        x=x, y=df['utxo_{}_5y_8y'.format(version)],
        mode='lines',
        line=dict(width=0.5, color='rgb(0, 0, 0)'),
        fillcolor='rgb(0.0, 144.0, 191.0)',
        fill='tonexty',
        name='5y-8y',
        stackgroup='one',
    ))

    fig.add_trace(go.Scatter(
        x=x, y=df['utxo_{}_greater_8y'.format(version)],
        mode='lines',
        line=dict(width=0.5, color='rgb(0, 0, 0)'),
        fillcolor='rgb(0.0, 100.0, 130.0)',
        fill='tonexty',
        name='>8y',
        stackgroup='one',
    ))

    fig.update_layout(
        showlegend=True,
        legend_orientation="h",
        yaxis=dict(
            type='linear',
            range=[1, 100],
            ticksuffix='%'))

    # Second trace
    fig.add_trace(go.Scatter(
        x=x, y=df['price_usd'],
        name='price_usd',
        mode='lines',
        line=dict(width=2, color='rgb(255, 255, 255)'),
    ),
        secondary_y=True,
    )

    if kwargs.get('halving_lines', False):
        min_date, max_date = x.min(), x.max()
        for halving_date in ['2012-11-29', '2016-07-10', '2020-05-11']:
            if min_date <= halving_date <= max_date:
                fig.add_trace(go.Scatter(
                    x=[halving_date, halving_date],
                    y=[0, 1000000],
                    mode="lines",
                    showlegend=False,
                    line=dict(width=2, color='white', dash="dot"),
                    name='{} Halving'.format(halving_date)
                ))

    fig.update_yaxes(
        title_text='Price ($USD)', secondary_y=True, tickformat="${n},",
        type='log', range=[-2, 5],
        showgrid=False
    )

    # Add figure title
    fig.update_layout(
        title_text='RealCap Weighted HODL Waves',
        annotations=[
            dict(x=1, y=-0.2,
                 text="Data: Proprietary",
                 showarrow=False, xref='paper', yref='paper',
                 xanchor='right', yanchor='auto', xshift=0, yshift=0),
            dict(x=1, y=-0.3,
                 text="Updated weekly Thurs AM",
                 showarrow=False, xref='paper', yref='paper',
                 xanchor='right', yanchor='auto', xshift=0, yshift=0)
        ],
        hovermode='x unified',
        template="plotly_dark",
        legend_orientation="v",
        showlegend=False,
        xaxis_showgrid=False,
        yaxis_showgrid=False
    )

    # Set x-axis title
    fig.update_xaxes(title_text='Date')

    return fig

def whirlpool_stacked_area_chart(df, chart='unspent_capacity', **kwargs):
    x = df[kwargs.get('x_series', 'date_period')]
    fig = make_subplots(
        specs=[[{"secondary_y": False}]]
    )

    fig.add_trace(go.Scatter(
        x=x, y=df['{}_0hop_samourai'.format(chart)],
        mode='lines',
        line=dict(width=0.5, color='rgb(0, 0, 0)'),
        fill='tonexty',
        fillcolor='lightblue',
        name='Total',
        stackgroup='two'
    ))

    fig.add_trace(go.Scatter(
        x=x, y=df['{}_0hop_samourai_5'.format(chart)],
        mode='lines',
        line=dict(width=0.5, color='rgb(0, 0, 0)'),
        fill='tonexty',
        fillcolor='red',
        name='50M Sats Pool',
        stackgroup='one'
    ))

    fig.add_trace(go.Scatter(
        x=x, y=df['{}_0hop_samourai_05'.format(chart)],
        mode='lines',
        line=dict(width=0.5, color='rgb(0, 0, 0)'),
        fill='tonexty',
        fillcolor='darkred',
        name='5M Sats Pool',
        stackgroup='one'
    ))

    fig.add_trace(go.Scatter(
        x=x, y=df['{}_0hop_samourai_01'.format(chart)],
        mode='lines',
        line=dict(width=0.5, color='rgb(0, 0, 0)'),
        fill='tonexty',
        fillcolor='indianred',
        name='1M Sats Pool',
        stackgroup='one'
    ))

    # Add figure title
    fig.update_layout(
        title_text=kwargs.get('title', ''),
    )

    # Set x-axis title
    if kwargs.get('x_axis_title'):
        fig.update_xaxes(title_text=kwargs.get('x_axis_title'))

    fig.update_layout(
        annotations=[
            dict(x=1, y=-0.2,
                 text="Data: Proprietary",
                 showarrow=False, xref='paper', yref='paper',
                 xanchor='right', yanchor='auto', xshift=0, yshift=0),
            dict(x=1, y=-0.3,
                 text="Updated weekly Thurs AM",
                 showarrow=False, xref='paper', yref='paper',
                 xanchor='right', yanchor='auto', xshift=0, yshift=0)
        ],
        showlegend=True,
        legend_orientation="h",
        template="plotly_dark",
        hovermode='x unified',
        xaxis_showgrid=False,
        yaxis_showgrid=False
    )

    # Set y-axes titles
    fig.update_yaxes(
        title_text=kwargs.get('y_series_title', ''), secondary_y=False,
        tickformat=kwargs.get('y_series_axis_format', None),
        type=kwargs.get('y_series_axis_type', 'linear'), range=kwargs.get('y_series_axis_range'),
        showgrid=False
    )

    return fig

def wasabi_stacked_area_chart(df, **kwargs):
    x = df[kwargs.get('x_series', 'date_period')]
    total = df['unspent_capacity_0hop_wasabi'] + df['unspent_capacity_1hop_wasabi']
    fig = make_subplots(
        specs=[[{"secondary_y": False}]]
    )

    fig.add_trace(go.Scatter(
        x=x, y=total,
        mode='lines',
        line=dict(width=0.5, color='rgb(0, 0, 0)'),
        fill='tonexty',
        fillcolor='lightblue',
        name='Total',
        stackgroup='two'
    ))

    fig.add_trace(go.Scatter(
        x=x, y=df['unspent_capacity_0hop_wasabi'],
        mode='lines',
        line=dict(width=0.5, color='rgb(0, 0, 0)'),
        fill='tonexty',
        fillcolor='lightgreen',
        name='Coinjoin Transaction Outputs',
        stackgroup='one'
    ))

    fig.add_trace(go.Scatter(
        x=x, y=df['unspent_capacity_1hop_wasabi'],
        mode='lines',
        line=dict(width=0.5, color='rgb(0, 0, 0)'),
        fill='tonexty',
        fillcolor='green',
        name='1-Hop from Coinjoin Transaction Outputs',
        stackgroup='one'
    ))

    # Add figure title
    fig.update_layout(
        title_text=kwargs.get('title', ''),
    )

    # Set x-axis title
    if kwargs.get('x_axis_title'):
        fig.update_xaxes(title_text=kwargs.get('x_axis_title'))

    fig.update_layout(
        annotations=[
            dict(x=1, y=-0.2,
                 text="Data: Proprietary",
                 showarrow=False, xref='paper', yref='paper',
                 xanchor='right', yanchor='auto', xshift=0, yshift=0),
            dict(x=1, y=-0.3,
                 text="Updated weekly Thurs AM",
                 showarrow=False, xref='paper', yref='paper',
                 xanchor='right', yanchor='auto', xshift=0, yshift=0)
        ],
        showlegend=True,
        legend_orientation="h",
        template="plotly_dark",
        hovermode='x unified',
        xaxis_showgrid=False,
        yaxis_showgrid=False
    )

    # Set y-axes titles
    fig.update_yaxes(
        title_text=kwargs.get('y_series_title', ''), secondary_y=False,
        tickformat=kwargs.get('y_series_axis_format', None),
        type=kwargs.get('y_series_axis_type', 'linear'), range=kwargs.get('y_series_axis_range'),
        showgrid=False
    )

    return fig