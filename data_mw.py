import os
import pandas as pd
import datetime
import utils

try:
    # Save latest data
    mercury_stats = pd.read_csv(
        'https://api.mercurywallet.com/summary')
    mercury_stats.fillna(0).to_csv('./data/mw/mw_stats_{}.csv'.format(datetime.date.today().strftime("%m_%d_%y")), index=False)

    mercury_hist = pd.read_csv(
        'https://api.mercurywallet.com/histogram')
    mercury_hist.fillna(0).to_csv('./data/mw/mw_hist_{}.csv'.format(datetime.date.today().strftime("%m_%d_%y")), index=False)

    # Build historical dataset
    mercury_stats = pd.DataFrame()
    mercury_hist = pd.DataFrame()

    for order_file in os.listdir("data/mw/"):
        if 'mw_stats' in order_file:
            mercury_stats_temp = pd.read_csv("data/mw/{}".format(order_file))
            mercury_stats = pd.concat([mercury_stats, mercury_stats_temp])
        elif 'mw_hist' in order_file:
            mercury_hist_temp = pd.read_csv("data/mw/{}".format(order_file))
            mercury_hist = pd.concat([mercury_hist, mercury_hist_temp])

    mercury_stats = mercury_stats.reset_index(drop=True).drop_duplicates()
    mercury_hist = mercury_hist.reset_index(drop=True).drop_duplicates()

    mercury_stats['datetime'] = [datetime.datetime.strptime(x[:15], '%a %b %d %Y') for x in mercury_stats['updated']]
    mercury_stats['date'] = [x.strftime('%Y-%m-%d %H:%M:%S')[:10] for x in mercury_stats['datetime']]
    mercury_stats = utils.get_extra_datetime_cols(mercury_stats, 'date', '%Y-%m-%d')
    mercury_hist['datetime'] = [datetime.datetime.strptime(x[:15], '%a %b %d %Y') for x in mercury_hist['updated']]
    mercury_hist['date'] = [x.strftime('%Y-%m-%d %H:%M:%S')[:10] for x in mercury_hist['datetime']]
    mercury_hist = utils.get_extra_datetime_cols(mercury_hist, 'date', '%Y-%m-%d')

    # Build metrics dataset from mercury_stats
    median_metrics = ['capacity_statechains', 'statecoins', 'liquidity']
    sum_metrics = [
        'swaps_per_day', 'swapset_per_day'
    ]

    dfs = {}

    for date_granularity in ['day', 'week', 'rhr_week', 'month', 'year', 'halving_era', 'market_cycle']:
        medians = mercury_stats.groupby(by=date_granularity, as_index=False)[median_metrics].median()
        sums = mercury_stats.groupby(by=date_granularity, as_index=False)[sum_metrics].sum()
        out = sums.merge(medians, how='outer', on=date_granularity)
        out['date_period'] = out[date_granularity]
        out['date_granularity'] = date_granularity
        dfs[date_granularity] = out[
            ['date_granularity', 'date_period',
             'swaps_per_day', 'swapset_per_day',
             'capacity_statechains', 'statecoins',
             'liquidity'
            ]
        ].copy()

    clean_data = pd.concat(dfs, ignore_index=True)
    clean_data['capacity_statechains'] = clean_data['capacity_statechains'] * 10 ** -8
    clean_data.to_csv('./data/mw_stats_data_clean.csv', index=False)

    # Build metrics dataset from mercury_hist
    median_metrics = ['100000', '500000', '1000000', '5000000', '10000000', '50000000']
    dfs = {}

    for date_granularity in ['day', 'week', 'rhr_week', 'month', 'year', 'halving_era', 'market_cycle']:
        out = mercury_hist.groupby(by=date_granularity, as_index=False)[median_metrics].median()
        out['date_period'] = out[date_granularity]
        out['date_granularity'] = date_granularity
        dfs[date_granularity] = out[
            ['date_granularity', 'date_period'] + median_metrics
        ].copy()

    clean_data = pd.concat(dfs, ignore_index=True)
    clean_data.to_csv('./data/mw_hist_data_clean.csv', index=False)
except:
    pass