import datetime

def get_halving_era(date):
    era = datetime.datetime.strptime('2009-01-03', "%Y-%m-%d")
    halvings = ['2012-11-29', '2016-07-10', '2020-05-11']
    for halving in halvings:
        halving = datetime.datetime.strptime(halving, "%Y-%m-%d")
        if date >= halving:
            era = halving
        else:
            return era.date()
    return era.date()

def get_market_cycle(date):
    cycle = datetime.datetime.strptime('2009-01-03', "%Y-%m-%d")
    cycle_dates = ['2011-11-18', '2015-01-14', '2018-12-16']
    for cycle_date in cycle_dates:
        cycle_date = datetime.datetime.strptime(cycle_date, "%Y-%m-%d")
        if date >= cycle_date:
            cycle = cycle_date
        else:
            return cycle.date()
    return cycle.date()

def get_extra_datetime_cols(df, datecol, date_format="%Y-%m-%d"):
    df['datetime'] = [datetime.datetime.strptime(x, date_format) for x in df[datecol]]
    df['year'] = [datetime.date(x.year, 1, 1) for x in df['datetime']]
    df['month'] = [datetime.date(x.year, x.month, 1) for x in df['datetime']]
    df['week'] = [(x - datetime.timedelta(days=(x.weekday() + 1))) for x in df['datetime']]
    df['rhr_week'] = [(x - datetime.timedelta(days=(x.weekday() - 3))) for x in df['datetime']]
    df['day'] = df['date']
    df['halving_era'] = [get_halving_era(x) for x in df['datetime']]
    df['market_cycle'] = [get_market_cycle(x) for x in df['datetime']]
    return df