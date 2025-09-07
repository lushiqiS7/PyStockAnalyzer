import pandas as pd
import numpy as np

def calculate_sma(df, window=5):
    """
    Calculates the Simple Moving Average for the 'Close' price.
    
    Args:
        df (pandas.DataFrame): DataFrame containing stock data with a 'Close' column.
        window (int): The number of periods to average. Default is 5.
        
    Returns:
        pandas.Series: A Series containing the SMA values.
    """
    # Calculate SMA using the rolling mean of the 'Close' column
    sma = df['Close'].rolling(window=window).mean()
    return sma

def identify_runs(df):
    """
    Identifies consecutive upward and downward days based on closing price.
    Counts the number of runs and finds the longest streak for each direction.
    
    Args:
        df (pandas.DataFrame): DataFrame containing stock data with a 'Close' column.
        
    Returns:
        dict: A dictionary containing:
            - 'up_streaks': List of all upward streak lengths
            - 'down_streaks': List of all downward streak lengths
            - 'total_up_days': Total number of upward days
            - 'total_down_days': Total number of downward days
            - 'longest_up_streak': Longest consecutive upward streak
            - 'longest_down_streak': Longest consecutive downward streak
    """
    # Calculate daily price changes
    price_changes = df['Close'].diff()
    
    # Identify upward (1) and downward (-1) days. 0 means no change.
    directions = np.sign(price_changes).fillna(0).astype(int)
    
    # Find where the direction changes
    change_points = (directions != directions.shift(1))
    streak_ids = change_points.cumsum()
    
    # Group by the streak ID and get the size and direction of each streak
    streaks = directions.groupby(streak_ids).agg(['size', 'first'])
    streaks.columns = ['length', 'direction']
    
    # Filter and aggregate results
    up_streaks = streaks[streaks['direction'] == 1]['length'].tolist()
    down_streaks = streaks[streaks['direction'] == -1]['length'].tolist()
    
    return {
        'up_streaks': up_streaks,
        'down_streaks': down_streaks,
        'total_up_days': sum(up_streaks),
        'total_down_days': sum(down_streaks),
        'longest_up_streak': max(up_streaks) if up_streaks else 0,
        'longest_down_streak': max(down_streaks) if down_streaks else 0
    }

def calculate_daily_returns(df):
    """
    Computes simple daily returns.
    
    Args:
        df (pandas.DataFrame): DataFrame containing stock data with a 'Close' column.
        
    Returns:
        pandas.Series: A Series containing the daily return values.
    """
    # Calculate daily returns: (Today's Close - Yesterday's Close) / Yesterday's Close
    daily_returns = df['Close'].pct_change()
    return daily_returns

def calculate_rsi(df, window=14):
    """
    Calculate Relative Strength Index (RSI)
    RSI > 70: Overbought (potential sell signal)
    RSI < 30: Oversold (potential buy signal)
    
    Args:
        df (pandas.DataFrame): DataFrame containing stock data with a 'Close' column.
        window (int): The lookback period for RSI calculation. Default is 14.
        
    Returns:
        pandas.Series: A Series containing the RSI values.
    """
    # Handle empty or insufficient data
    if len(df) < window + 1:
        return pd.Series([np.nan] * len(df), index=df.index)
    
    delta = df['Close'].diff()
    
    # Separate gains and losses
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    
    # Calculate average gain and loss using exponential moving average
    avg_gain = gain.ewm(span=window, adjust=False).mean()
    avg_loss = loss.ewm(span=window, adjust=False).mean()
    
    # Calculate RS and RSI
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    
    return rsi

def calculate_bollinger_bands(df, window=20, num_std=2):
    """
    Calculate Bollinger Bands
    Upper Band: SMA + (standard deviation × 2)
    Lower Band: SMA - (standard deviation × 2)
    
    Args:
        df (pandas.DataFrame): DataFrame containing stock data with a 'Close' column.
        window (int): The lookback period for calculation. Default is 20.
        num_std (int): Number of standard deviations for bands. Default is 2.
        
    Returns:
        tuple: (upper_band, middle_band, lower_band) as pandas Series
    """
    # Handle empty or insufficient data
    if len(df) < window:
        empty_series = pd.Series([np.nan] * len(df), index=df.index)
        return empty_series, empty_series, empty_series
    
    sma = df['Close'].rolling(window=window).mean()
    std = df['Close'].rolling(window=window).std()
    
    upper_band = sma + (std * num_std)
    lower_band = sma - (std * num_std)
    
    return upper_band, sma, lower_band

# Test the functions immediately
if __name__ == "__main__":
    # This will only run when calculations.py is executed directly
    print("Enhanced calculations module loaded successfully!")
    print("Functions defined: calculate_sma(), identify_runs(), calculate_daily_returns(), calculate_rsi(), calculate_bollinger_bands()")