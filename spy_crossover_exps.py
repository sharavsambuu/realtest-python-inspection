#%%
import quantstats        as qs
import yfinance          as yf
import pandas            as pd
import numpy             as np
import matplotlib.pyplot as plt
import talib             as ta

pd.options.mode.copy_on_write = True


#%%


#%%


#%%
SYMBOL = "SPY"

df_ = yf.download(SYMBOL, start="1992-01-01", interval="1d", actions=True, auto_adjust=True)
df_

#%%


#%%
df = pd.DataFrame(index=df_.index)
df['Open'  ] = df_[('Open'  , SYMBOL)]
df['High'  ] = df_[('High'  , SYMBOL)]
df['Low'   ] = df_[('Low'   , SYMBOL)]
df['Close' ] = df_[('Close' , SYMBOL)]
df['Volume'] = df_[('Volume', SYMBOL)]

df['Open'  ] = df['Open' ].round(4)
df['High'  ] = df['High' ].round(4)
df['Low'   ] = df['Low'  ].round(4)
df['Close' ] = df['Close'].round(4)

df


#%%


#%%
def strat_ma_cross(df, p_ma_fast, p_ma_slow):
    c                = df['Close'  ]
    df['MA_FAST']    = ta.SMA(df['Close'], timeperiod=p_ma_fast)
    df['MA_SLOW']    = ta.SMA(df['Close'], timeperiod=p_ma_slow)
    ma_fasts         = df['MA_FAST']
    ma_slows         = df['MA_SLOW']
    position         = 0              
    entry_fill_price = 0
    rets             = []
    dates            = []
    unrealized_rets  = []
    unrealized_dates = []
    for i, date in enumerate(c.index):
        if i<p_ma_slow+1: continue
        unrealized_rets .append(((c.iloc[i]-c.iloc[i-1])/c.iloc[i-1])*position)
        unrealized_dates.append(date)
        if  position == 0 and \
            ma_fasts.iloc[i-1] <= ma_slows.iloc[i-1] and \
            ma_fasts.iloc[i  ] >  ma_slows.iloc[i  ]:
            position = 1
            entry_fill_price = c.iloc[i]
        if position == 1 and \
            ma_fasts.iloc[i-1] >= ma_slows.iloc[i-1] and \
            ma_fasts.iloc[i  ] <  ma_slows.iloc[i  ]:
            position = 0
            rets .append((c.iloc[i]-entry_fill_price)/entry_fill_price)
            dates.append(date)
    return dates, rets, unrealized_dates, unrealized_rets


#%%
MA_FAST = 50
MA_SLOW = 200

dates, rets, unrealized_dates, unrealized_rets = strat_ma_cross(df, p_ma_fast=MA_FAST, p_ma_slow=MA_SLOW)

report_df = pd.DataFrame(index=pd.DatetimeIndex(pd.to_datetime(unrealized_dates)))
report_df['unrealized_ret'] = unrealized_rets
temp_df = pd.DataFrame(index=pd.DatetimeIndex(pd.to_datetime(dates)))
temp_df  ['ret'] = rets
report_df['ret'] = temp_df['ret']
report_df.fillna(0.0, inplace=True)

report_df[['ret', 'unrealized_ret']].cumsum().plot()


#%%
average_return = float(np.mean(rets))
print(f"Average returns = {average_return}")

#%%


#%%
# Tracking capital based on order

initial_capital = 10000.0

report_df['GrowthFactor'] = (1 + report_df['ret']).cumprod()
report_df['Equity'      ] = initial_capital*report_df['GrowthFactor']

report_df['Equity'].plot()


#%%
print(f"Initial equity : {initial_capital}")
print(f"Final equity   : {round(report_df.iloc[-1]['Equity'], 2)}")


#%%


#%%



#%%
qs.plots.snapshot(report_df['unrealized_ret'], title='SPY Crossover', show=True);

#%%
qs.plots.drawdown(report_df['unrealized_ret'])

#%%
qs.plots.drawdowns_periods(report_df['unrealized_ret'])

#%%
qs.plots.histogram(report_df['unrealized_ret'])

#%%
qs.plots.monthly_heatmap(report_df['unrealized_ret'])

#%%
print(f"Sharpe Ratio : {round(float(qs.stats.sharpe(report_df['unrealized_ret'])),2)}")

#%%


#%%




