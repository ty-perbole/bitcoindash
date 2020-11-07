import pandas as pd

import utils

node_count = pd.read_csv('https://luke.dashjr.org/programs/bitcoin/files/charts/data/history.txt', sep=' ', header=None)
node_count.columns = ['ts', 'listening_node', 'total_nodes']
node_count

node_count['datetime'] = pd.to_datetime(node_count['ts']*1000000000)
node_count['date'] = [x.strftime('%Y-%m-%d %H:%M:%S')[:10] for x in node_count['datetime']]
node_count = utils.get_extra_datetime_cols(node_count, 'date')

dfs = {}

for date_granularity in ['day', 'week', 'month', 'year', 'halving_era', 'market_cycle']:
    out = node_count.groupby(by=date_granularity, as_index=False)['total_nodes'].median()
    out['date_period'] = out[date_granularity]
    out['date_granularity'] = date_granularity
    dfs[date_granularity] = out[
        ['date_granularity', 'date_period', 'total_nodes']
    ].copy()

clean_data = pd.concat(dfs, ignore_index=True)
clean_data.to_csv('node_count_data_clean.csv', index=False)