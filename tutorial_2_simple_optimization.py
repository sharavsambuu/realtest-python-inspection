
#%%
# https://mhptrading.com/docs/index.htm?context=92
#

#%%
import quantstats        as qs
import yfinance          as yf
import pandas            as pd
import numpy             as np
import matplotlib.pyplot as plt

pd.options.mode.copy_on_write = True


#%%


#%%


#%%
df_ = yf.download("SPY", start="1992-01-01", interval="1d", actions=True)

df_['Open'     ] = df_['Open'     ].round(4)
df_['High'     ] = df_['High'     ].round(4)
df_['Low'      ] = df_['Low'      ].round(4)
df_['Close'    ] = df_['Close'    ].round(4)
df_['Adj Close'] = df_['Adj Close'].round(4)

df_

#%%
df_.info()

#%%
df_[df_['Dividends']>0]

#%%
df_[df_['Stock Splits']>0]

#%%


#%%
df_['FillPrice'] = df_['Open' ].shift(-1)
df_['Date'     ] = df_.index
df_['DateIn'   ] = df_['Date' ].shift(-1)
df_['DateOut'  ] = df_['Date' ].shift(-1)

df_.fillna(method='ffill', inplace=True)


#%%
# Strategy backtester

def backtest(df_, test_number, ma_fast, ma_slow):
    print(f"Testing {test_number}, MA_FAST : {ma_fast}, MA_SLOW : {ma_slow}")
    df = df_.copy()

    df['EntrySetup'] = 0
    df['ExitRule'  ] = 0

    df['MaFast'] = df['Close'].rolling(ma_fast).mean()
    df['MaSlow'] = df['Close'].rolling(ma_slow).mean()

    df.dropna(inplace=True)

    df.loc[((df['MaFast']>df['MaSlow']) & (df['MaFast'].shift(1)<=df['MaSlow'].shift(1))), 'EntrySetup'] = 1
    df.loc[((df['MaFast']<df['MaSlow']) & (df['MaFast'].shift(1)>=df['MaSlow'].shift(1))), 'ExitRule'  ] = 1

    df.loc[df.index[ 0], 'EntrySetup'] = 1
    df.loc[df.index[-1], 'ExitRule'  ] = 1



    # Position tracking
    date_in          = None
    entry_fill_price = 0
    date_out         = None
    exit_fill_price  = 0
    position_history = []

    for index, row in df.iterrows():
        # EntrySetup
        if row['EntrySetup'] == 1:
            date_in          = row['DateIn'   ]
            entry_fill_price = row['FillPrice']
        # ExitRuel
        if row['ExitRule'  ] == 1:
            date_out        = row['DateOut'  ]
            exit_fill_price = row['FillPrice']
            pct_change      = (exit_fill_price - entry_fill_price)/entry_fill_price
            bars            = len(df[date_in:date_out])-1
            position_history.append((
                date_in, 
                date_out, 
                entry_fill_price, 
                exit_fill_price, 
                pct_change,
                bars
                ))

    position_df = pd.DataFrame(position_history, columns=['DateIn', 'DateOut', 'PriceIn', 'PriceOut', 'Return', 'Bars'])
    position_df = position_df.set_index(pd.DatetimeIndex(position_df['DateIn']))


    initial_capital = 10000.0

    df['Return'] = df['Close'].pct_change()

    df['StratReturn'] = 0.0
    for index, row in position_df.iterrows():
        sub_df = df[row['DateIn']:row['DateOut']]["Return"]
        df.loc[sub_df.index, 'StratReturn'] = sub_df

    df['GrowthFactor'] = (1 + df['StratReturn']).cumprod()
    df['DollarEquity'] = initial_capital*df['GrowthFactor']


    return {
        'final_capital'    : round(df.iloc[-1]['DollarEquity'], 2),
        'sharpe_ratio'     : round(qs.stats.sharpe(df['StratReturn']), 4),
        'maximum_drawdown' : round(qs.stats.max_drawdown(df['StratReturn']) * -100.0, 2),
        'win_rate'         : round(qs.stats.win_rate(df['StratReturn']), 4),
        'sortino_ratio'    : round(qs.stats.sortino(df['StratReturn']), 4),
        'cagr'             : round(qs.stats.cagr(df['StratReturn']), 4),
        'profit_factor'    : round(qs.stats.profit_factor(df['StratReturn']), 4),
        'prob_sr'          : round(qs.stats.probabilistic_sharpe_ratio(df['StratReturn']), 4),
    }
    


#%%



#%%
# Parameter Optimization

counter       = 0
backtest_list = []

for ma_fast in range(10, 90, 10):
    for ma_slow in range(100, 350, 50):
        counter += 1
        result   = backtest(df_=df_, test_number=counter, ma_fast=ma_fast, ma_slow=ma_slow)
        backtest_list.append((
            counter,
            result['final_capital'   ],
            result['sharpe_ratio'    ],
            result['maximum_drawdown'],
            result['win_rate'        ],
            result['sortino_ratio'   ],
            result['cagr'            ], 
            result['profit_factor'   ],
            result['prob_sr'         ],
            ma_fast,
            ma_slow
        ))

backtests_df = pd.DataFrame(backtest_list,
                            columns=[
                                'test_number',
                                'Final Capital',
                                'Sharpe Ratio',
                                'Maximum Drawdown',
                                'Win Rate',
                                'Sortino Ratio',
                                'Compounded Annual Growth Rate',
                                'Profit Factor',
                                'Probabilistic Sharpe Ratio',
                                'Fast MA',
                                'Slow MA'
                            ])

backtests_df.set_index('test_number', inplace=True)


#%%


#%%
backtests_df


#%%


#%%


#%%


#%%


#%%


#%%


#%%


#%%



#%%


#%%


#%%


#%%


#%%


#%%


#%%


#%%



#%%


#%%


#%%


#%%



#%%


#%%


#%%


#%%



#%%


#%%


#%%


#%%




#%%


#%%


#%%


#%%



#%%


#%%


#%%


#%%



#%%


#%%


#%%


#%%


#%%


#%%


#%%


#%%



#%%


#%%


#%%


#%%



#%%


#%%


#%%


#%%



#%%


#%%


#%%


#%%




#%%


#%%


#%%


#%%



#%%


#%%


#%%


#%%



#%%


#%%


#%%


#%%


#%%


#%%


#%%


#%%



#%%


#%%


#%%


#%%



#%%


#%%


#%%


#%%



#%%


#%%


#%%


#%%



#%%


#%%


#%%


#%%



#%%


#%%


#%%


#%%



#%%


#%%


#%%


#%%


#%%


#%%


#%%


#%%



#%%


#%%


#%%


#%%



#%%


#%%


#%%


#%%



#%%


#%%


#%%


#%%




#%%


#%%


#%%


#%%



#%%


#%%


#%%


#%%



#%%


#%%


#%%


#%%


#%%


#%%


#%%


#%%



#%%


#%%


#%%


#%%



#%%


#%%


#%%


#%%



#%%


#%%


#%%


#%%




#%%


#%%


#%%


#%%



#%%


#%%


#%%


#%%



#%%


#%%


#%%


#%%


#%%


#%%


#%%


#%%



#%%


#%%


#%%


#%%



#%%


#%%


#%%


#%%



#%%


#%%


#%%


#%%




