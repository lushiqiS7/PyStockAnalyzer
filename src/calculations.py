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

# Test the functions immediately
if __name__ == "__main__":
    # This will only run when calculations.py is executed directly
    print("Testing calculations module...")
    
    # You would need to fetch data first to test properly
    # For now, this just confirms the file can be run without syntax errors
    print("Functions defined: calculate_sma(), identify_runs(), calculate_daily_returns()")