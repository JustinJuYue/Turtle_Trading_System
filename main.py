import datetime as dt
import matplotlib.pyplot as plt
import yfinance as yf
import pandas as pd
import numpy as np

# --- Account and Strategy Parameters ---
initial_equity = 10000.0  # Initial account equity in USD
risk_percentage = 0.01   # 1% of equity to risk per unit
entry_period = 20        # Lookback period for the entry high
exit_period = 10         # Lookback period for the exit low
atr_period = 20          # ATR (N-Value) calculation period
max_units = 4            # Maximum number of units to hold in a position

# --- Data Fetching ---
# Using a longer timeframe for a more stable ATR calculation
start = dt.datetime.now() - dt.timedelta(days=365)
end = dt.datetime.now()

# Download the stock data
# Using 'META' as the modern ticker for Facebook/Meta
data = yf.download("META", start=start, end=end)

# --- Indicator Calculation ---
# 1. Calculate True Range
high_low = data['High'] - data['Low']
high_prev_close = np.abs(data['High'] - data['Close'].shift(1))
low_prev_close = np.abs(data['Low'] - data['Close'].shift(1))
data['true_range'] = pd.concat([high_low, high_prev_close, low_prev_close], axis=1).max(axis=1)

# 2. Calculate ATR (N-Value) - Using EMA is the standard method
data['atr'] = data['true_range'].ewm(alpha=1/atr_period, adjust=False).mean()

# 3. Calculate Entry and Exit Channels (Donchian Channels)
# Use .shift(1) to avoid lookahead bias (i.e., we can only make decisions based on yesterday's data)
data['entry_high'] = data['High'].rolling(window=entry_period).max().shift(1)
data['exit_low'] = data['Low'].rolling(window=exit_period).min().shift(1)

# Clean data by dropping initial NaN values
data.dropna(inplace=True)

# --- Backtest and Signal Generation ---
equity = initial_equity
position_size_shares = 0
units_held = 0
last_entry_price = 0.0
buy_signals = []
sell_signals = []
equity_curve = []

for i in range(len(data)):
    current_price = data['Close'].iloc[i]
    current_atr = data['atr'].iloc[i]
    
    # Calculate today's unit size in shares
    # Use int() to ensure we trade whole shares
    unit_size_shares = int((risk_percentage * equity) / current_atr)

    # Entry Logic (if we are flat / have no position)
    if units_held == 0:
        print(f"DEBUG: Comparing type {type(current_price)} with type {type(data['entry_high'].iloc[i])}")
        if current_price > data['entry_high'].iloc[i]:
            # Buy 1 unit
            position_size_shares = unit_size_shares
            equity -= position_size_shares * current_price
            last_entry_price = current_price
            units_held = 1
            buy_signals.append(current_price)
            sell_signals.append(np.nan)
        else:
            buy_signals.append(np.nan)
            sell_signals.append(np.nan)

    # Position Management Logic (if we are currently long)
    elif units_held > 0:
        # Pyramiding Logic (Add to the position)
        if units_held < max_units and current_price > (last_entry_price + 0.5 * current_atr):
            # Add another unit
            equity -= unit_size_shares * current_price
            position_size_shares += unit_size_shares
            last_entry_price = current_price
            units_held += 1
            buy_signals.append(current_price) # Mark as an "add" signal
            sell_signals.append(np.nan)
        
        # Exit Logic
        elif current_price < data['exit_low'].iloc[i]:
            # Sell all shares / exit the position
            equity += position_size_shares * current_price
            position_size_shares = 0
            units_held = 0
            last_entry_price = 0.0
            sell_signals.append(current_price)
            buy_signals.append(np.nan)
        else:
            buy_signals.append(np.nan)
            sell_signals.append(np.nan)

    # Record the daily portfolio value
    portfolio_value = equity + (position_size_shares * current_price)
    equity_curve.append(portfolio_value)

data['Buy Signals'] = buy_signals
data['Sell Signals'] = sell_signals
data['Portfolio Value'] = equity_curve

# --- Plotting ---
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 12), gridspec_kw={'height_ratios': [3, 1]}, sharex=True)
fig.suptitle('Turtle Trading System Backtest for META', fontsize=16)

# Plot 1: Price, Channels, and Signals
ax1.grid(True)
ax1.plot(data['Close'], label='Share Price', color='lightblue', linewidth=1.5)
ax1.plot(data['entry_high'], label=f'{entry_period}-Day High Channel', color='green', linestyle=':', alpha=0.7)
ax1.plot(data['exit_low'], label=f'{exit_period}-Day Low Channel', color='red', linestyle=':', alpha=0.7)
ax1.scatter(data.index, data['Buy Signals'], label='Buy/Add Signal', marker='^', color='lime', s=120, edgecolors='black')
ax1.scatter(data.index, data['Sell Signals'], label='Sell Signal', marker='v', color='red', s=120, edgecolors='black')
ax1.set_ylabel('Price (USD)')
ax1.legend(loc='upper left')
ax1.set_title('Price, Channels, and Trading Signals')

# Plot 2: Equity Curve
ax2.grid(True)
ax2.plot(data['Portfolio Value'], label='Portfolio Value', color='blue', linewidth=2)
ax2.set_ylabel('Portfolio Value (USD)')
ax2.set_xlabel('Date')
ax2.set_title('Equity Curve')
ax2.legend(loc='upper left')

plt.show()