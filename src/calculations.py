"""
Core calculations module for stock analysis.

This module provides fundamental financial calculation functions including
moving averages, trend analysis, technical indicators, and statistical measures
commonly used in stock market analysis.
"""

import pandas as pd
import numpy as np


def calculate_sma(df, window=5):
    """
    Calculate Simple Moving Average (SMA) for stock data.
    
    The Simple Moving Average is calculated by taking the arithmetic mean
    of a given set of closing prices over a specific number of periods.
    
    Args:
        df (pandas.DataFrame): DataFrame containing stock data with a 'Close' column.
        window (int, optional): Number of periods to include in the moving average.
                               Defaults to 5.
    
    Returns:
        pandas.Series: Series containing the SMA values. The first (window-1)
                      values will be NaN since there's insufficient data.
                      
    Example:
        >>> data = pd.DataFrame({'Close': [10, 12, 14, 16, 18]})
        >>> sma = calculate_sma(data, window=3)
        >>> print(sma.tolist())
        [nan, nan, 12.0, 14.0, 16.0]
    """
    # Calculate SMA using the rolling mean of the 'Close' column
    sma = df['Close'].rolling(window=window).mean()
    return sma

def identify_runs(df):
    """
    Identify and analyze consecutive runs of upward and downward price movements.
    
    A "run" is defined as a sequence of consecutive days where the stock price
    moves in the same direction (either up or down). This function analyzes
    these patterns to provide insights into trending behavior.
    
    Args:
        df (pandas.DataFrame): DataFrame containing stock data with a 'Close' column.
                              Must have a proper date index for accurate analysis.
    
    Returns:
        dict: Dictionary containing run analysis with the following keys:
            - 'up_streaks' (list): Lengths of all upward runs
            - 'down_streaks' (list): Lengths of all downward runs  
            - 'total_up_days' (int): Total number of days in upward trends
            - 'total_down_days' (int): Total number of days in downward trends
            - 'longest_up_streak' (int): Length of the longest upward run
            - 'longest_down_streak' (int): Length of the longest downward run
            
    Example:
        If prices move: 100 -> 102 -> 104 -> 103 -> 101 -> 103
        This creates: up, up, down, down, up (2-day up, 2-day down, 1-day up)
    """
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
    """
    Identify run periods with their start and end dates for visualization highlighting.
    
    This function extends the basic run analysis by providing specific date ranges
    for each run period, making it suitable for visualization and detailed analysis.
    Each run period includes timing information that can be used to highlight
    trends on charts or perform time-based analysis.
    
    Args:
        df (pandas.DataFrame): DataFrame containing stock data with a 'Close' column
                              and a datetime index for accurate date tracking.
    
    Returns:
        list: List of dictionaries, each representing a run period with keys:
            - 'start_date': Start date of the run period
            - 'end_date': End date of the run period  
            - 'direction' (int): 1 for upward run, -1 for downward run
            - 'length' (int): Number of days in the run
            
    Note:
        Periods with no price change (direction = 0) are excluded from results.
        This function is particularly useful for creating visualizations that
        highlight trending periods on stock charts.
    """
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
    """
    Calculate daily percentage returns for stock data.
    
    Daily return represents the percentage change in stock price from one day
    to the next. It's calculated as: (Today's Close - Yesterday's Close) / Yesterday's Close
    This is a fundamental metric for analyzing stock performance and volatility.
    
    Args:
        df (pandas.DataFrame): DataFrame containing stock data with a 'Close' column.
    
    Returns:
        pandas.Series: Series containing daily percentage returns. The first value
                      will be NaN since there's no previous day for comparison.
                      
    Example:
        If closing prices are [100, 105, 102], daily returns would be:
        [NaN, 0.05, -0.0286] representing [N/A, +5%, -2.86%]
    """
    # Calculate daily returns: (Today's Close - Yesterday's Close) / Yesterday's Close
    daily_returns = df['Close'].pct_change()
    return daily_returns

def calculate_rsi(df, window=14):
    """
    Calculate Relative Strength Index (RSI) technical indicator.
    
    RSI is a momentum oscillator that measures the speed and magnitude of price changes.
    It oscillates between 0 and 100, where values above 70 typically indicate overbought
    conditions and values below 30 indicate oversold conditions. The calculation uses
    exponential moving averages of gains and losses over the specified window period.
    
    Args:
        df (pandas.DataFrame): DataFrame containing stock data with a 'Close' column.
        window (int, optional): Number of periods for RSI calculation. Defaults to 14,
                               which is the standard period used in technical analysis.
    
    Returns:
        pandas.Series: Series containing RSI values ranging from 0 to 100.
                      Returns NaN values if insufficient data is available.
                      
    Note:
        - RSI > 70: Potentially overbought (sell signal)
        - RSI < 30: Potentially oversold (buy signal)  
        - RSI around 50: Neutral momentum
        
    Example:
        >>> rsi = calculate_rsi(df, window=14)
        >>> overbought_days = rsi[rsi > 70]  # Find overbought periods
    """
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
    """
    Calculate Bollinger Bands technical indicator.
    
    Bollinger Bands consist of a middle line (simple moving average) and two outer bands
    that are standard deviations away from the middle line. They help identify overbought
    and oversold conditions by showing when prices are relatively high or low compared
    to recent trading ranges.
    
    Args:
        df (pandas.DataFrame): DataFrame containing stock data with a 'Close' column.
        window (int, optional): Number of periods for moving average calculation. 
                               Defaults to 20 (standard period).
        num_std (int, optional): Number of standard deviations for the bands.
                               Defaults to 2 (standard setting).
    
    Returns:
        tuple: Three pandas Series containing:
            - upper_band: Upper Bollinger Band (SMA + num_std * standard deviation)
            - middle_band: Middle line (Simple Moving Average)  
            - lower_band: Lower Bollinger Band (SMA - num_std * standard deviation)
            
    Note:
        - Price touching upper band: Potentially overbought
        - Price touching lower band: Potentially oversold
        - Price squeezing between bands: Low volatility period
        - Bands expanding: Increasing volatility
        
    Example:
        >>> upper, middle, lower = calculate_bollinger_bands(df, window=20, num_std=2)
        >>> squeeze_periods = df[(upper - lower) < threshold]  # Find low volatility periods
    """
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
    """
    Entry point for direct script execution.
    
    When this module is run directly (e.g., python calculations.py), it displays
    information about the available functions rather than executing tests.
    This provides a quick reference for developers.
    """
    # This will only run when calculations.py is executed directly
    print("Enhanced calculations module loaded successfully!")
    print("Available functions:")
    print("- calculate_sma(): Calculate Simple Moving Average")
    print("- identify_runs(): Analyze consecutive price movement patterns") 
    print("- identify_run_periods(): Get detailed run periods with dates")
    print("- calculate_daily_returns(): Calculate daily percentage returns")
    print("- calculate_rsi(): Calculate Relative Strength Index")
    print("- calculate_bollinger_bands(): Calculate Bollinger Bands indicator")