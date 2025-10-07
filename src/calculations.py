"""
Core calculations module for stock analysis.

This module provides fundamental financial calculation functions including
moving averages, trend analysis, technical indicators, and statistical measures
commonly used in stock market analysis.
"""

import pandas as pd
import numpy as np


def calculate_sma(df, window=5):

    # Calculate SMA using the rolling mean of the 'Close' column
    sma = df['Close'].rolling(window=window).mean()
    return sma

def identify_runs(df):
   
    # Calculate daily price changes (today's close - yesterday's close)
    price_changes = df['Close'].diff()
    
    # Identify upward (1) and downward (-1) days. 0 means no change.
    directions = np.sign(price_changes).fillna(0).astype(int)
    
    # Find where the direction changes (start of new runs)
    change_points = (directions != directions.shift(1))
    streak_ids = change_points.cumsum()
    
    # Group by the streak ID and get the size and direction of each streak
    streaks = directions.groupby(streak_ids).agg(['size', 'first'])
    streaks.columns = ['length', 'direction']
    
    # Filter and aggregate results by direction
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

def identify_run_periods(df):

    # Calculate daily price changes (difference from previous day)
    price_changes = df['Close'].diff()
    
    # Identify upward (1) and downward (-1) days. 0 means no change.
    directions = np.sign(price_changes).fillna(0).astype(int)
    
    # Find where the direction changes (marks start of new runs)
    change_points = (directions != directions.shift(1))
    streak_ids = change_points.cumsum()
    
    # Create a DataFrame to track runs with date information
    run_data = pd.DataFrame({
        'direction': directions,
        'streak_id': streak_ids
    }, index=df.index)
    
    # Group by streak_id to get run periods with date ranges
    run_periods = []
    for streak_id in run_data['streak_id'].unique():
        streak_data = run_data[run_data['streak_id'] == streak_id]
        direction = streak_data['direction'].iloc[0]
        
        # Skip periods with no direction (direction = 0)
        if direction != 0:
            start_date = streak_data.index[0]
            end_date = streak_data.index[-1]
            length = len(streak_data)
            
            run_periods.append({
                'start_date': start_date,
                'end_date': end_date,
                'direction': direction,  # 1 for up, -1 for down
                'length': length
            })
    
    return run_periods

def calculate_daily_returns(df):
 
    # Calculate daily returns: (Today's Close - Yesterday's Close) / Yesterday's Close
    daily_returns = df['Close'].pct_change()
    return daily_returns

def calculate_rsi(df, window=14):
    
    # Handle empty or insufficient data
    if len(df) < window + 1:
        return pd.Series([np.nan] * len(df), index=df.index)
    
    # Calculate price changes (delta) from day to day
    delta = df['Close'].diff()
    
    # Separate gains and losses (gains are positive changes, losses are positive values of negative changes)
    gain = delta.where(delta > 0, 0)  # Keep positive changes, zero out negative
    loss = -delta.where(delta < 0, 0)  # Convert negative changes to positive, zero out positive
    
    # Calculate average gain and loss using exponential moving average
    avg_gain = gain.ewm(span=window, adjust=False).mean()
    avg_loss = loss.ewm(span=window, adjust=False).mean()
    
    # Calculate Relative Strength (RS) and RSI
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    
    return rsi

def calculate_bollinger_bands(df, window=20, num_std=2):
   
    # Handle empty or insufficient data
    if len(df) < window:
        empty_series = pd.Series([np.nan] * len(df), index=df.index)
        return empty_series, empty_series, empty_series
    
    # Calculate the middle line (Simple Moving Average)
    sma = df['Close'].rolling(window=window).mean()
    
    # Calculate rolling standard deviation
    std = df['Close'].rolling(window=window).std()
    
    # Calculate upper and lower bands
    upper_band = sma + (std * num_std)
    lower_band = sma - (std * num_std)
    
    return upper_band, sma, lower_band

# Entry point for direct script execution
if __name__ == "__main__":
  
    # This will only run when calculations.py is executed directly
    print("Enhanced calculations module loaded successfully!")
    print("Available functions:")
    print("- calculate_sma(): Calculate Simple Moving Average")
    print("- identify_runs(): Analyze consecutive price movement patterns") 
    print("- identify_run_periods(): Get detailed run periods with dates")
    print("- calculate_daily_returns(): Calculate daily percentage returns")
    print("- calculate_rsi(): Calculate Relative Strength Index")
    print("- calculate_bollinger_bands(): Calculate Bollinger Bands indicator")