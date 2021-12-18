import json
import os
import numpy as np
import pandas as pd

import utils

df_dict = {}

for order_file in os.listdir("data/jm/"):
    with open("data/jm/{}".format(order_file), "r") as json_file:
        orderbook = json.load(json_file)
        counterparties = []
        liquidity = []
        fees = []
        if isinstance(orderbook, list):
            pass
        else:
            orderbook = orderbook.get('offers')
        for order in orderbook:
            if order['counterparty'] not in counterparties:
                counterparties.append(order['counterparty'])
                liquidity.append(order['maxsize'])
                fees.append(order['cjfee'])

        fees = np.float64(fees)

        df_dict[order_file[10:14] + '-' + order_file[14:16] + '-' + order_file[16:18]] = {
            'maker_count': len(counterparties),
            'maker_liquidity': np.sum(liquidity) * (10 ** -8),
            'mean_liquidity_per_maker': np.sum(liquidity) * (10 ** -8) / len(counterparties),
            'median_liquidity_per_maker': np.median(liquidity) * (10 ** -8),
            'cj_fee': np.median(fees[fees < 0.01])
        }

jm_orderbook = pd.DataFrame.from_dict(df_dict, orient='index')
jm_orderbook['date'] = jm_orderbook.index
jm_orderbook = utils.get_extra_datetime_cols(jm_orderbook, 'date', '%Y-%m-%d')

dfs = {}

columns = [
    'maker_count', 'maker_liquidity', 'mean_liquidity_per_maker',
    'median_liquidity_per_maker', 'cj_fee'
]

for date_granularity in ['day', 'week', 'rhr_week', 'month', 'year', 'halving_era', 'market_cycle']:
    out = jm_orderbook.groupby(by=[date_granularity], as_index=False)[columns].median()
    out['date_period'] = out[date_granularity]
    out['date_granularity'] = date_granularity

    dfs[date_granularity] = out[
        ['date_granularity', 'date_period'] + columns
        ].copy()

clean_data = pd.concat(dfs, ignore_index=True)
clean_data['cj_fee'] *= 100
clean_data.fillna(0).to_csv('./data/jm_orderbook.csv', index=False)