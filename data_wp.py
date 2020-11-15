import datetime
import pandas as pd

import utils

from whirlpool_stats.whirlpool_stats.utils.constants import ALL_DENOMS, TXID_PREFIX_LENGTH
from whirlpool_stats.whirlpool_stats.services.downloader import Downloader
from whirlpool_stats.whirlpool_stats.services.snapshot import Snapshot
from whirlpool_stats.whirlpool_stats.services.forward_metrics import ForwardMetrics
from whirlpool_stats.whirlpool_stats.services.backward_metrics import BackwardMetrics
from whirlpool_stats.whirlpool_stats.services.tx0s_metrics import Tx0sMetrics
from whirlpool_stats.whirlpool_stats.services.exporter import Exporter

try:
    WORKING_DIR = "."

    downloader = Downloader()
    downloader.download(WORKING_DIR, ALL_DENOMS)

    snapshot = Snapshot(WORKING_DIR)

    tx0_metrics = Tx0sMetrics(snapshot)
    fwd_metrics = ForwardMetrics(snapshot)
    bwd_metrics = BackwardMetrics(snapshot)

    exporter = Exporter(
            fwd_metrics,
            bwd_metrics,
            tx0_metrics
        )

    for denom in ALL_DENOMS:
        snapshot.set_dir(WORKING_DIR)
        snapshot.load(denom)
        tx0_metrics.compute()
        fwd_metrics.compute()
        bwd_metrics.compute()
        exporter.export(WORKING_DIR)

    pool_sizes = ['001', '005', '05']
    dfs = []
    for pool_size in pool_sizes:
        wp = pd.read_csv("./whirlpool_{}_activity_metrics.csv".format(pool_size), sep=';')
        wp['pool'] = float('.'+pool_size) * 10
        dfs.append(wp.copy())
    wp = pd.concat(dfs, ignore_index=True)
    wp['nb_new_btc'] = wp['nb_new_tx0s'] * wp['pool']
    wp['nb_active_btc'] = wp['nb_active_tx0s'] * wp['pool']
    wp['volume'] = wp['nb_mixes'] * wp['pool'] * 5

    wp['date'] = [datetime.datetime.strptime(x, "%d/%m/%Y").strftime('%Y-%m-%d') for x in wp['date']]
    wp = utils.get_extra_datetime_cols(wp, 'date')

    dfs = {}

    for date_granularity in ['day', 'week', 'rhr_week', 'month', 'year', 'halving_era', 'market_cycle']:
        out = wp.groupby(by=[date_granularity], as_index=False)['nb_new_btc', 'nb_active_btc', 'volume'].sum()
        pools = wp.groupby(by=[date_granularity, 'pool'], as_index=False)['volume'].sum().pivot(index=date_granularity, columns='pool', values='volume')
        out = out.merge(pools, on=date_granularity)
        out['pool_50M'] = out[0.5]  / out['volume']
        out['pool_5M'] = out[0.05]  / out['volume']
        out['pool_1M'] = out[0.01]  / out['volume']
        out['date_period'] = out[date_granularity]
        out['date_granularity'] = date_granularity
        dfs[date_granularity] = out[
            ['date_granularity', 'date_period', 'nb_new_btc', 'nb_active_btc', 'volume',
             'pool_50M', 'pool_5M', 'pool_1M']
        ].copy()

    clean_data = pd.concat(dfs, ignore_index=True)
    clean_data.fillna(0).to_csv('./data/whirlpool_data_clean.csv', index=False)
except:
    pass