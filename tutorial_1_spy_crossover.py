#%%
# https://mhptrading.com/docs/index.htm?context=90
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
df = yf.download("SPY", start="1992-01-01", interval="1d", actions=True)

df['Open'     ] = df['Open'     ].round(4)
df['High'     ] = df['High'     ].round(4)
df['Low'      ] = df['Low'      ].round(4)
df['Close'    ] = df['Close'    ].round(4)
df['Adj Close'] = df['Adj Close'].round(4)

df

#%%
df.info()

#%%
df[df['Dividends']>0]

#%%
df[df['Stock Splits']>0]

#%%


#%%
# Strategy 

df['FillPrice'] = df['Open' ].shift(-1)
df['Date'     ] = df.index
df['DateIn'   ] = df['Date' ].shift(-1)
df['DateOut'  ] = df['Date' ].shift(-1)

df.fillna(method='ffill', inplace=True)


df['EntrySetup'] = 0
df['ExitRule'  ] = 0

df['MaFast'] = df['Close'].rolling( 50).mean()
df['MaSlow'] = df['Close'].rolling(200).mean()

df.dropna(inplace=True)


df.loc[((df['MaFast']>df['MaSlow']) & (df['MaFast'].shift(1)<=df['MaSlow'].shift(1))), 'EntrySetup'] = 1
df.loc[((df['MaFast']<df['MaSlow']) & (df['MaFast'].shift(1)>=df['MaSlow'].shift(1))), 'ExitRule'  ] = 1

df.loc[df.index[ 0], 'EntrySetup'] = 1
df.loc[df.index[-1], 'ExitRule'  ] = 1

df


#%%


#%%
#plot_df = df.iloc[-1000:-400]
plot_df = df["1993-06-11":"1994-05-25"]
plot_df[['MaFast', 'MaSlow']].plot(legend=False)

plt.scatter(plot_df[plot_df['EntrySetup']==1].index, plot_df[plot_df['EntrySetup']==1]['MaFast'], c='g')
plt.scatter(plot_df[plot_df['ExitRule'  ]==1].index, plot_df[plot_df['ExitRule'  ]==1]['MaFast'], c='r')

plt.show();

#%%


#%%


#%%
# Position tracking

in_position      = False
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


position_df


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




