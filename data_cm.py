import os
import subprocess
import pandas as pd
from scipy.stats import poisson

import utils
try:
    try:
        os.remove("btc.csv")
    except FileNotFoundError:
        pass
    subprocess.run("wget https://coinmetrics.io/newdata/btc.csv", shell=True, check=True)

    cm = pd.read_csv('btc.csv')

    cm = utils.get_extra_datetime_cols(cm, 'date')

    cm['BlkSizeByte'] = cm['BlkCnt'] * cm['BlkSizeMeanByte']


    cm['HashRateL7DInc'] = cm['HashRate'].rolling(7).mean()
    cm['HashRateL7D'] = cm['HashRateL7DInc'].shift() / 1000000

    alpha = 0.025
    cm['BlkCntLower'] = [poisson.interval(1 - alpha, x)[0] for x in cm['BlkCnt']]
    cm['BlkCntUpper'] = [poisson.interval(1 - alpha, x)[1] for x in cm['BlkCnt']]
    cm['HashRateLower'] = [(x / 144) * y * (((2 ** 32) / (10 ** 12)) / (600 * 1000000))
                             for x, y in zip(cm['BlkCntLower'], cm['DiffMean'])]
    cm['HashRateUpper'] = [(x / 144) * y * (((2 ** 32) / (10 ** 12)) / (600 * 1000000))
                             for x, y in zip(cm['BlkCntUpper'], cm['DiffMean'])]

    dfs = {}
    median_metrics = ['CapMrktCurUSD', 'CapRealUSD', 'CapMVRVCur', 'HashRate', 'VtyDayRet30d', 'AdrActCnt',
                      'HashRateLower', 'HashRateUpper', 'HashRateL7D']
    sum_metrics = [
        'TxTfrValAdjUSD', 'IssTotUSD', 'FeeTotUSD', 'FeeTotNtv', 'BlkWghtTot', 'BlkSizeByte',
        'SplyCur', 'IssTotNtv', 'TxTfrValAdjNtv', 'HashRate'
    ]

    for date_granularity in ['day', 'week', 'rhr_week', 'month', 'year', 'halving_era', 'market_cycle']:
        medians = cm.groupby(by=date_granularity, as_index=False)[median_metrics].median()
        sums = cm.groupby(by=date_granularity, as_index=False)[sum_metrics].sum()
        sums['SecuritySpend'] = sums['IssTotUSD'] + sums['FeeTotUSD']
        sums['ThermoCap'] = sums['SecuritySpend'].cumsum()
        sums['SecuritySpendRatio'] = (sums['IssTotNtv'] + sums['FeeTotNtv']) / sums['SplyCur']
        sums['BlockSpacePrice'] = sums['FeeTotNtv'] * 10 ** 8 / sums['BlkSizeByte']
        sums['BlockSpacePriceUSD'] = sums['FeeTotUSD'] * 100 / sums['BlkSizeByte']
        sums['TransactionDensity'] = sums['TxTfrValAdjUSD'] / sums['BlkSizeByte']
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