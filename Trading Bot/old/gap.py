'''import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

ticker_symbol = "AAPL"
ticker = yf.Ticker(ticker_symbol)
historical_data = ticker.history(period="5y")

df = historical_data[['Open', 'Close']].copy()
buying_price = df['Open'].iloc[0]
starting_money = 10000
stocks = int(starting_money / buying_price)  
starting_money -= stocks * buying_price 

stop_loss = .95 * buying_price
take_profit = 1.2 * buying_price

prev_close = df['Close'].iloc[0]
for index, row in df.iloc[1:].iterrows():
    open_price = row['Open']
    close_price = row['Close']
    if open_price > prev_close: 
        if open_price >= take_profit:
            sell_stocks = int(.3 * stocks)
            stocks -= sell_stocks
            starting_money += sell_stocks * open_price
        else:
            money = starting_money * .6
            stocks += int(money / open_price)  
            starting_money -= money
    elif prev_close > open_price:
        if open_price <= stop_loss:
            sell_stocks = int(.7 * stocks)
            stocks -= sell_stocks
            starting_money += sell_stocks * open_price
        else:
            sell_stocks = int(.5 * stocks)
            stocks -= sell_stocks
            starting_money += sell_stocks * open_price
    prev_close = close_price
print(f"Money: {starting_money + (stocks * prev_close)}")
print(f"Stocks: {stocks}, Buying Price: ${buying_price:.2f}, Amount Left: ${starting_money:.2f}") '''

import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Download historical data for Apple (AAPL)
ticker_symbol = "NVDA"
ticker = yf.Ticker(ticker_symbol)
historical_data = ticker.history(period="5y")

# Extract relevant columns
df = historical_data[['Open', 'Close']].copy()

# Initialize variables
buying_price = df['Open'].iloc[0]
starting_money = 10000
stocks = starting_money // buying_price  # Number of stocks bought initially
starting_money -= stocks * buying_price

stop_loss = 0.95 * buying_price  # 5% drop threshold
take_profit = 1.2 * buying_price  # 20% rise threshold

prev_close = df['Close'].iloc[0]

# Track portfolio value over time
portfolio_values = []

for index, row in df.iloc[1:].iterrows():
    open_price = row['Open']
    close_price = row['Close']

    if open_price > prev_close:  # Price increased
        if open_price >= take_profit:
            sell_stocks = int(0.3 * stocks)
            stocks -= sell_stocks
            starting_money += sell_stocks * open_price
        else:
            money_to_invest = starting_money * 0.6
            additional_stocks = money_to_invest // open_price
            stocks += additional_stocks
            starting_money -= additional_stocks * open_price
        stop_loss = 0.95 * open_price  # 5% drop threshold
        take_profit = 1.2 * open_price  # 20% rise threshold
    elif prev_close > open_price:  # Price decreased
        if open_price <= stop_loss:
            sell_stocks = int(0.5 * stocks)
        else:
            sell_stocks = int(0.3 * stocks)
        stocks -= sell_stocks
        starting_money += sell_stocks * open_price
        stop_loss = 0.95 * open_price  # 5% drop threshold
        take_profit = 1.2 * open_price 
    else:
        stop_loss = 0.95 * prev_close  # 5% drop threshold
        take_profit = 1.2 * prev_close  # 20% rise threshold

    # Update the previous close price
    prev_close = close_price


    # Calculate current portfolio value
    portfolio_value = starting_money + (stocks * prev_close)
    portfolio_values.append((index, portfolio_value))

# Print final results
print(f"Final Money: ${starting_money:.2f}")
print(f"Stocks Remaining: {stocks}")
print(f"Buying Price: ${buying_price:.2f}")
print(f"Final Portfolio Value: ${portfolio_value:.2f}")

# Plot portfolio value over time
dates, values = zip(*portfolio_values)
plt.figure(figsize=(12, 6))
plt.plot(dates, values, label='Portfolio Value', linewidth=2)
plt.xlabel('Date')
plt.ylabel('Portfolio Value (USD)')
plt.title('Portfolio Value Over Time')
plt.legend()
plt.grid(True)
plt.show()