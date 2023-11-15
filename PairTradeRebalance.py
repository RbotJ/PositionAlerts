import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Parameters
start_date = (datetime.now() - timedelta(days=2*365)).strftime('%Y-%m-%d')
end_date = datetime.now().strftime('%Y-%m-%d')
stocks = ['AAPL', 'TSLA']
initial_investment = 10000
rebalance_threshold = 0.01  # 1%

# Fetching data
data = yf.download(stocks, start=start_date, end=end_date)['Adj Close']

# Initialize Portfolio
portfolio = pd.DataFrame(index=data.index)
portfolio['cash'] = 0
portfolio['AAPL_shares'] = initial_investment / 2 / data['AAPL'].iloc[0]
portfolio['TSLA_shares'] = initial_investment / 2 / data['TSLA'].iloc[0]
portfolio['total_value'] = portfolio['AAPL_shares'] * data['AAPL'] + portfolio['TSLA_shares'] * data['TSLA']

# Backtesting Loop
for i in range(1, len(portfolio)):
    portfolio.at[portfolio.index[i], 'AAPL_shares'] = portfolio.at[portfolio.index[i-1], 'AAPL_shares']
    portfolio.at[portfolio.index[i], 'TSLA_shares'] = portfolio.at[portfolio.index[i-1], 'TSLA_shares']
    portfolio.at[portfolio.index[i], 'total_value'] = (portfolio.at[portfolio.index[i], 'AAPL_shares'] * data['AAPL'][i] + 
                                                       portfolio.at[portfolio.index[i], 'TSLA_shares'] * data['TSLA'][i])
    
    # Check for rebalancing
    aapl_value = portfolio.at[portfolio.index[i], 'AAPL_shares'] * data['AAPL'][i]
    tsla_value = portfolio.at[portfolio.index[i], 'TSLA_shares'] * data['TSLA'][i]
    total_value = aapl_value + tsla_value
    
    if abs(aapl_value - tsla_value) / total_value > rebalance_threshold:
        # Rebalance
        portfolio.at[portfolio.index[i], 'AAPL_shares'] = total_value / 2 / data['AAPL'][i]
        portfolio.at[portfolio.index[i], 'TSLA_shares'] = total_value / 2 / data['TSLA'][i]
        portfolio.at[portfolio.index[i], 'total_value'] = (portfolio.at[portfolio.index[i], 'AAPL_shares'] * data['AAPL'][i] + 
                                                           portfolio.at[portfolio.index[i], 'TSLA_shares'] * data['TSLA'][i])

# Final Portfolio Value
final_value = portfolio['total_value'].iloc[-1]
print(f"Final Portfolio Value: ${final_value:.2f}")

# To view the complete portfolio frame, use: print(portfolio)