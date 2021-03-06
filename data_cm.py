import os
import subprocess
import pandas as pd

import utils
try:
    try:
        os.remove("btc.csv")
    except FileNotFoundError:
        pass
    subprocess.run("wget https://coinmetrics.io/newdata/btc.csv", shell=True, check=True)

    cm = pd.read_csv('btc.csv')

    cm = utils.get_extra_datetime_cols(cm, 'date')

    dfs = {}
    median_metrics = ['CapMrktCurUSD', 'CapRealUSD', 'CapMVRVCur', 'HashRate', 'VtyDayRet30d', 'AdrActCnt']
    sum_metrics = [
        'TxTfrValAdjUSD', 'IssTotUSD', 'FeeTotUSD', 'FeeTotNtv', 'BlkSizeByte',
        'SplyCur', 'IssTotNtv', 'TxTfrValNtv', 'TxTfrValUSD', 'HashRate'
    ]

    for date_granularity in ['day', 'week', 'rhr_week', 'month', 'year', 'halving_era', 'market_cycle']:
        medians = cm.groupby(by=date_granularity, as_index=False)[median_metrics].median()
        sums = cm.groupby(by=date_granularity, as_index=False)[sum_metrics].sum()
        sums['SecuritySpend'] = sums['IssTotUSD'] + sums['FeeTotUSD']
        sums['ThermoCap'] = sums['SecuritySpend'].cumsum()
        sums['SecuritySpendRatio'] = (sums['IssTotNtv'] + sums['FeeTotNtv']) / sums['SplyCur']
        sums['BlockSpacePrice'] = sums['FeeTotNtv'] * 10 ** 8 / sums['BlkSizeByte']
        sums['BlockSpacePriceUSD'] = sums['FeeTotUSD'] * 100 / sums['BlkSizeByte']
        sums['TransactionDensity'] = sums['TxTfrValUSD'] / sums['BlkSizeByte']
        sums['CentsPerEH'] = (sums['SecuritySpend'] / (sums['HashRate'] * 60 * 60 * 24)) * 100
        sums['DollarsPerYH'] = (sums['SecuritySpend'] / (sums['HashRate'] * 60 * 60 * 24 * (10 ** -6)))
        sums['HashRate'] = sums['HashRate'] / 1000000
        sums['HashRateCum'] = sums['HashRate'].cumsum()
        sums.drop(columns='HashRate', inplace=True)
        medians['HashRate'] = medians['HashRate'] / 1000000
        out = sums.merge(medians, how='outer', on=date_granularity)
        out['ChainRewriteDays'] = sums['HashRateCum'] / out['HashRate']
        out['date_period'] = out[date_granularity]
        out['date_granularity'] = date_granularity
        dfs[date_granularity] = out[
            ['date_granularity', 'date_period',
             'TxTfrValAdjUSD', 'SecuritySpendRatio',
             'BlockSpacePrice', 'BlockSpacePriceUSD',
             'TransactionDensity', 'ChainRewriteDays',
             'DollarsPerYH'
            ] + median_metrics
        ].copy()

    clean_data = pd.concat(dfs, ignore_index=True)
    clean_data.to_csv('./data/cm_data_clean.csv', index=False)
except:
    pass