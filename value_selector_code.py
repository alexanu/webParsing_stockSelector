import pandas as pd
import numpy as np

frame = pd.read_csv('/Users/marcocatania/Documents/Projects/Python/value_stocks_selector/original_table.csv')

x =  frame.where(frame['Net Asset Value per Share'] > 0)

x['Value'] = ((x['Net Asset Value per Share'] - x['Current Price per Share (pence)']) * 100) / x['Net Asset Value per Share']

x = x.set_index('Unnamed: 0')

x.loc[(x['Gearing (%)'] < 25) & (x['Net Asset Value per Share'] > 40)]
