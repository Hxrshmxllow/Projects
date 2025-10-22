import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Download 2 years of historical data for AAPL
ticker_symbol = "AAPL"
ticker = yf.Ticker(ticker_symbol)
historical_data = ticker.history(period="3y") 
df = historical_data[['Close']].copy()

df['SMA_50'] = df['Close'].rolling(window=50).mean()
df['SMA_200'] = df['Close'].rolling(window=200).mean()
df['Signal'] = 0  

df.loc[df['SMA_50'] > df['SMA_200'], 'Signal'] = 1  # Buy Signal
df.loc[df['SMA_50'] < df['SMA_200'], 'Signal'] = -1  # Sell Signal

# Calculate the positions where the signal changes
df['Position'] = df['Signal'].diff()

plt.figure(figsize=(12, 6))
plt.plot(df['Close'], label='Close Price', alpha=0.6)
plt.plot(df['SMA_50'], label='SMA 50', linestyle='--')
plt.plot(df['SMA_200'], label='SMA 200', linestyle='--')

buy_signals = df[df['Position'] == 2]  # Cross from 0 to 1 (Golden Cross)
sell_signals = df[df['Position'] == -2]  # Cross from 0 to -1 (Death Cross)

plt.scatter(buy_signals.index, buy_signals['Close'], label='Buy Signal', marker='^', color='green', s=100)
plt.scatter(sell_signals.index, sell_signals['Close'], label='Sell Signal', marker='v', color='red', s=100)

plt.title('Moving Average Crossover Strategy: AAPL', fontsize=16)
plt.xlabel('Date', fontsize=12)
plt.ylabel('Price (USD)', fontsize=12)
plt.legend(loc='best')
plt.grid(True)
plt.show()
