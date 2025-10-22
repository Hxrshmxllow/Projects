import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Step 1: Download historical data for AAPL (2 years)
ticker_symbol = "AAPL"
ticker = yf.Ticker(ticker_symbol)
historical_data = ticker.history(period="5y")

# Step 2: Select 'Close' prices and prepare DataFrame
df = historical_data[['Close']].copy()

# Step 3: Calculate 50-day and 200-day EMA
df['EMA_50'] = df['Close'].ewm(span=50, adjust=False).mean()
df['EMA_200'] = df['Close'].ewm(span=200, adjust=False).mean()

# Step 4: Generate Buy/Sell signals based on EMA crossover
df['Signal'] = 0  # Initialize signal column to 0
df.loc[df['EMA_50'] > df['EMA_200'], 'Signal'] = 1  # Buy Signal
df.loc[df['EMA_50'] < df['EMA_200'], 'Signal'] = -1  # Sell Signal

# Calculate the crossover points (where signals change)
df['Position'] = df['Signal'].diff()

# Step 5: Plot the EMAs, Close Price, and Buy/Sell signals
plt.figure(figsize=(16, 8))
plt.plot(df['Close'], label='Close Price', alpha=0.5)
plt.plot(df['EMA_50'], label='50-day EMA', linestyle='--', color='blue')
plt.plot(df['EMA_200'], label='200-day EMA', linestyle='--', color='orange')

# Mark the Buy and Sell signals on the plot
buy_signals = df[df['Position'] == 2]  # From 0 to 1 (Buy signal)
sell_signals = df[df['Position'] == -2]  # From 0 to -1 (Sell signal)

plt.scatter(buy_signals.index, buy_signals['Close'], label='Buy Signal', marker='^', color='green', s=100)
plt.scatter(sell_signals.index, sell_signals['Close'], label='Sell Signal', marker='v', color='red', s=100)

# Add plot title and labels
plt.title('EMA Crossover Strategy: AAPL', fontsize=16)
plt.xlabel('Date', fontsize=12)
plt.ylabel('Price (USD)', fontsize=12)
plt.legend(loc='best')
plt.grid(True)

# Display the plot
plt.show()