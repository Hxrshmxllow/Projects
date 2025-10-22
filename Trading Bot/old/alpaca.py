import alpaca_trade_api as tradeapi
import time

API_KEY = 'PK762XBV3BSPN38M77AH'
SECRET_KEY = 'hS2yndNV8h7cKLletGZn3KegrLPotV7iaMcDjXWP'
BASE_URL = 'https://paper-api.alpaca.markets'  # Use paper trading endpoint

api = tradeapi.REST(API_KEY, SECRET_KEY, BASE_URL, api_version='v2')

requests = 0
symbols = ['NVDA', 'TSM']
stop_loss = 0.99
take_profit = 1.05
money_to_invest = 15000

def is_market_open():
    """Check if the market is open."""
    try:
        clock = api.get_clock()
        return clock.is_open
    except Exception as e:
        print(f"Error checking market status: {e}")
        return False

def check_rate_limit():
    """Ensure compliance with Alpaca's rate limits."""
    global requests
    if requests >= 195:
        print("Rate limit approaching, pausing for 60 seconds...")
        time.sleep(60)
        requests = 0

def place_order(qty, side, symbol):
    """Place a buy or sell order."""
    try:
        check_rate_limit()
        order = api.submit_order(
            symbol=symbol,
            qty=qty,
            side=side,
            type='market',
            time_in_force='gtc'
        )
        global requests
        requests += 1
        print(f"{side.capitalize()} order placed for {qty} shares of {symbol}.")
    except tradeapi.rest.APIError as e:
        print(f"API Error placing order for {symbol}: {e}")
    except Exception as e:
        print(f"Unexpected error placing order for {symbol}: {e}")

def logic(symbol):
    """Execute trading logic for a given symbol."""
    global requests
    try:
        # Ensure account data is fresh each iteration
        account = api.get_account()
        buying_power = float(account.buying_power)
        requests += 1

        # Fetch the latest 1-minute bar data
        check_rate_limit()
        bars = api.get_bars(symbol, timeframe='1Min', limit=1)

        if not bars:  # Ensure the bars data is not empty
            print(f"No data returned for {symbol}. Skipping...")
            return

        for bar in bars:
            current_price = bar.c
            print(f"{symbol} Current Price: {current_price}")

            # Check if there is an existing position
            try:
                position = api.get_position(symbol)
                qty = int(position.qty)
                avg_price = float(position.avg_entry_price)
                requests += 1

                # Sell if take-profit or stop-loss is triggered
                if current_price >= avg_price * take_profit:
                    print(f"Take profit triggered for {symbol}.")
                    place_order(qty, 'sell', symbol)
                elif current_price <= avg_price * stop_loss:
                    print(f"Stop loss triggered for {symbol}.")
                    place_order(qty, 'sell', symbol)

            except tradeapi.rest.APIError:
                # No existing position, proceed to buy
                qty = int(money_to_invest / current_price)
                if qty > 0 and buying_power >= qty * current_price:
                    place_order(qty, 'buy', symbol)

    except Exception as e:
        print(f"Error executing logic for {symbol}: {e}")

# Main trading loop
while True:
    if is_market_open():
        print("Market is open. Executing trades...")
        for symbol in symbols:
            logic(symbol)
            time.sleep(1)  # Small delay between symbols to avoid bursts
    else:
        print("Market is closed. Waiting...")
    time.sleep(60)  # Wait a minute before ch