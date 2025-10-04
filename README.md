# 🐢 Turtle Trading System Backtest in Python

This repository contains a Python script that backtests the famous **Turtle Trading strategy** on historical stock data. The script uses `yfinance` to fetch data, `pandas` and `numpy` for data manipulation and calculations, and `matplotlib` to visualize the results.

---

## 🧠 What is the Turtle Trading Strategy?

The Turtle Trading system is a renowned **trend-following strategy** developed by legendary commodities trader **Richard Dennis** in the 1980s. He believed anyone could learn to trade successfully with the right rules — and proved it by teaching a group of novices known as the "Turtles."

The core philosophy is simple:  
**"Buy breakouts to new highs and sell breakdowns to new lows."**

The system includes strict rules for:

1. **Entry Signal** – Buy when price exceeds the highest high over `n` days.
2. **Position Sizing** – Risk a fixed percent of equity per trade using the **Average True Range (ATR)**.
3. **Pyramiding** – Add to a winning position at defined intervals.
4. **Exit Signal** – Exit when price breaks below the lowest low over a shorter period.

---

## 🔑 Key Concepts in the Script

### 📏 Donchian Channels

Entry and exit signals use **Donchian Channels**, calculated as:

- **Entry Channel**: Highest high over `entry_period` (e.g., 20 days).
- **Exit Channel**: Lowest low over `exit_period` (e.g., 10 days).

Buy signals occur when the price **crosses above** the entry channel; sell signals occur when it **crosses below** the exit channel.

### 📊 Average True Range (ATR) with EMA

The **ATR** measures market volatility and is essential for:

- Sizing trades to normalize risk.
- Timing entries and exits.

This script uses an **Exponential Moving Average (EMA)** for ATR to give more weight to recent data, making it more responsive to market changes than a simple moving average (SMA).

---

## ⚙️ How to Use and Customize the Backtest

You can easily configure the backtest by adjusting the variables at the top of the script.

### 🧪 Account and Strategy Parameters

```python
# --- Account and Strategy Parameters ---
initial_equity = 10000.0   # Initial account equity in USD
risk_percentage = 0.01     # 1% of equity to risk per unit
entry_period = 20          # Lookback period for the entry high
exit_period = 10           # Lookback period for the exit low
atr_period = 20            # ATR (N-Value) calculation period
max_units = 4              # Max number of units to pyramid into a position
```
## ⚠️ Disclaimer

This script is intended for educational and informational purposes only.
The trading signals generated are based on a simplistic technical analysis strategy and should not be considered financial advice.
Trading involves risk, and you should do your own research or consult a licensed financial advisor before making any investment decisions.



