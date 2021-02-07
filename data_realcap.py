import subprocess
import pandas as pd
import utils
import os

try:
    os.remove("btc.csv")
except FileNotFoundError:
    pass
subprocess.run("wget https://coinmetrics.io/newdata/btc.csv", shell=True, check=True)
subprocess.run("bq load --autodetect dash.cm_btc btc.csv", shell=True, check=True)
subprocess.run("mv realcap.csv realcap_old.csv", shell=True, check=True)
subprocess.run("bq query --use_legacy_sql=False --format=csv --max_rows=999999 < ./queries/realcap.sql > realcap.csv", shell=True, check=True)

# waves = pd.read_csv("realcap.csv")

waves = pd.read_csv("../stack-stats/data/03_hodl_waves_real_cap.csv")

waves_new = pd.read_csv("realcap.csv")

waves = waves[:-1].append(waves_new).reset_index(drop=True)

waves_buckets = list([x for x in waves.columns.values if 'utxo_realcap' in x])
waves = utils.get_extra_datetime_cols(waves, 'date')

dfs = {}

for date_granularity in ['day', 'week', 'rhr_week', 'month', 'year', 'halving_era', 'market_cycle']:
    sums = waves.groupby(by=date_granularity, as_index=False)[waves_buckets].sum()
    price = waves.groupby(by=date_granularity, as_index=False)['price_usd'].median()
    out = sums.merge(price, how='outer', on=date_granularity)
    out['date_period'] = out[date_granularity]
    out['date_granularity'] = date_granularity
    dfs[date_granularity] = out[
        ['date_granularity', 'date_period', 'price_usd'] + waves_buckets
    ].copy()

clean_data = pd.concat(dfs, ignore_index=True)
clean_data.dropna(inplace=True)
clean_data.to_csv('./data/waves_data_clean2.csv', index=False)

