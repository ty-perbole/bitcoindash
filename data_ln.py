import pandas as pd
import numpy as np

import utils
try:

    lnchan = pd.read_csv("ln_channels.csv")
    lnchan['open_ts'] = pd.to_datetime(lnchan['open_ts'] * 1000000000)
    lnchan['close_ts'] = pd.to_datetime(lnchan['close_ts'] * 1000000000)

    out_df = {}
    drange = pd.date_range(lnchan.open_ts.min(), max(lnchan.close_ts.max(), lnchan.open_ts.max()), normalize=True)
    for date in pd.date_range(lnchan.open_ts.min(), max(lnchan.close_ts.max(), lnchan.open_ts.max()), normalize=True):
        channels = lnchan.loc[
            (lnchan['open_ts'] <= date) & (
                    (lnchan['close_ts'] > date) |
                    (pd.isnull(lnchan['close_ts']))
            )]
        node1 = channels[['node1', 'satoshis']]
        node1.columns = ['node', 'satoshis']
        node2 = channels[['node2', 'satoshis']]
        node2.columns = ['node', 'satoshis']
        node_channels = pd.concat([node1, node2])
        node_channels.groupby('node', as_index=False).satoshis.sum()
        node_channels['channel_pct'] = node_channels['satoshis'] / node_channels['satoshis'].sum()
        out_df[date.strftime('%Y-%m-%d %H:%M:%S')[:10]] = {
            'channel_count': channels.satoshis.count(),
            'channel_value': channels.satoshis.sum() * (10 ** -8),
            'nodes_w_channels': len(set(list(channels['node1']) + list(channels['node2']))),
            'node_liquidity_herfindahl': np.sum(node_channels['channel_pct'] ** 2)

        }

    lnmetrics = pd.DataFrame.from_dict(out_df, orient='index')
    lnmetrics['date'] = lnmetrics.index
    lnmetrics = utils.get_extra_datetime_cols(lnmetrics, 'date')

    dfs = {}

    for date_granularity in ['day', 'week', 'rhr_week', 'month', 'year', 'halving_era', 'market_cycle']:
        out = lnmetrics.groupby(by=[date_granularity], as_index=False)[
            'channel_count', 'channel_value', 'nodes_w_channels', 'node_liquidity_herfindahl'].median()
        out['date_period'] = out[date_granularity]
        out['date_granularity'] = date_granularity
        dfs[date_granularity] = out[
            ['date_granularity', 'date_period', 'channel_count', 'channel_value', 'nodes_w_channels',
             'node_liquidity_herfindahl']
        ].copy()

    clean_data = pd.concat(dfs, ignore_index=True)
    clean_data.fillna(0).to_csv('./data/ln_data_clean.csv', index=False)
except:
    pass