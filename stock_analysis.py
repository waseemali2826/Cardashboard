import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import yfinance as yf
from datetime import datetime, timedelta

# Configure matplotlib style
plt.style.use('seaborn-v0_8')

# Step 1: Download stock data with robust error handling
def get_stock_data(ticker, years=1):
    """Download historical stock data for given ticker"""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365*years)
    try:
        data = yf.download(ticker, start=start_date, end=end_date, progress=False)
        if data.empty:
            data = yf.Ticker(ticker).history(period=f"{years}y")
        if not isinstance(data, pd.DataFrame) or 'Close' not in data.columns:
            raise ValueError("Invalid data format received")
        return data
    except Exception as e:
        print(f"Error downloading data for {ticker}: {str(e)}")
        return None

# Step 2: Plot trends
def plot_basic_trends(data, ticker):
    """Create basic trend visualizations"""
    # Line Chart
    plt.figure(figsize=(14, 7))
    plt.plot(data.index, data['Close'], color='blue', linewidth=2)
    plt.title(f'{ticker} Closing Price Trend (1 Year)', fontsize=16)
    plt.xlabel('Date', fontsize=14)
    plt.ylabel('Price ($)', fontsize=14)
    plt.grid(True)
    plt.show()

    # Candlestick chart
    fig = go.Figure(data=[go.Candlestick(
        x=data.index,
        open=data['Open'],
        high=data['High'],
        low=data['Low'],
        close=data['Close'],
        increasing_line_color='green',
        decreasing_line_color='red'
    )])
    fig.update_layout(
        title=f'{ticker} Candlestick Chart (1 Year)',
        xaxis_title='Date',
        yaxis_title='Price ($)',
        xaxis_rangeslider_visible=False
    )
    fig.show()

# Step 3: Moving averages
def plot_moving_averages(data, ticker):
    """Calculate and plot moving averages"""
    data['50_MA'] = data['Close'].rolling(window=50).mean()
    data['200_MA'] = data['Close'].rolling(window=200).mean()

    plt.figure(figsize=(14, 7))
    plt.plot(data.index, data['Close'], label='Closing Price', color='blue', alpha=0.5)
    plt.plot(data.index, data['50_MA'], label='50-day MA', color='orange', linewidth=2)
    plt.plot(data.index, data['200_MA'], label='200-day MA', color='green', linewidth=2)
    plt.title(f'{ticker} Price with Moving Averages', fontsize=16)
    plt.xlabel('Date', fontsize=14)
    plt.ylabel('Price ($)', fontsize=14)
    plt.legend(fontsize=12)
    plt.grid(True)
    plt.show()

# Step 4: Volume analysis
def plot_volume(data, ticker):
    """Plot trading volume"""
    plt.figure(figsize=(14, 7))
    plt.bar(data.index, data['Volume'], color='gray', alpha=0.7)
    plt.title(f'{ticker} Trading Volume', fontsize=16)
    plt.xlabel('Date', fontsize=14)
    plt.ylabel('Volume', fontsize=14)
    plt.grid(True)
    plt.show()

# Helper to extract safe price value
def get_price_value(price_data):
    if isinstance(price_data, pd.Series):
        return float(price_data.values[0])
    return float(price_data)

# Main analysis function
def analyze_stock(ticker='AAPL', years=1):
    """Complete stock analysis workflow"""
    print(f"\nAnalyzing {ticker} stock data for the past {years} year(s)...")
    data = get_stock_data(ticker, years)
    if data is None or data.empty:
        print(f"❌ Failed to retrieve data for {ticker}")
        return None

    # Basic Stats
    print("\n📈 Basic Information:")
    print(f"Date Range: {data.index[0].date()} to {data.index[-1].date()}")
    try:
        current_close = get_price_value(data['Close'].iloc[-1])
        initial_close = get_price_value(data['Close'].iloc[0])
        print(f"Recent Closing Price: ${current_close:.2f}")
        print(f"Period Change: {((current_close - initial_close)/initial_close)*100:.2f}%")
    except Exception as e:
        print(f"Error calculating price metrics: {str(e)}")

    # Plots
    try:
        plot_basic_trends(data, ticker)
        plot_moving_averages(data, ticker)
        plot_volume(data, ticker)
    except Exception as e:
        print(f"Error generating plots: {str(e)}")

    return data

# Run from terminal
if __name__ == "__main__":
    stock_data = analyze_stock(ticker='AAPL', years=1)

    if stock_data is not None:
        print("\n📊 Additional Statistics:")
        print(f"Average Daily Volume: {stock_data['Volume'].mean():,.0f} shares")
        print(f"Highest Price: ${stock_data['High'].max():.2f}")
        print(f"Lowest Price: ${stock_data['Low'].min():.2f}")
