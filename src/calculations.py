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
    """
    delta = df['Close'].diff()
    
    # Separate gains and losses
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    
    # Calculate average gain and loss
    avg_gain = gain.rolling(window=window).mean()
    avg_loss = loss.rolling(window=window).mean()
    
    # Handle division by zero - when avg_loss is 0, RSI should be 100
    # When both avg_gain and avg_loss are 0, RSI should be 50
    rs = avg_gain / avg_loss
    rs.replace([np.inf, -np.inf], np.nan, inplace=True)
    
    # Calculate RSI
    rsi = 100 - (100 / (1 + rs))
    
    # Handle cases where avg_loss is 0 (all gains)
    rsi[avg_loss == 0] = 100
    
    # Handle cases where both avg_gain and avg_loss are 0 (no price change)
    rsi[(avg_gain == 0) & (avg_loss == 0)] = 50
    
    return rsi

def calculate_bollinger_bands(df, window=20, num_std=2):
    """
    Calculate Bollinger Bands
    Upper Band: SMA + (standard deviation × 2)
    Lower Band: SMA - (standard deviation × 2)
    """
    sma = df['Close'].rolling(window=window).mean()
    std = df['Close'].rolling(window=window).std()
    
    upper_band = sma + (std * num_std)
    lower_band = sma - (std * num_std)
    
    return upper_band, sma, lower_band

def calculate_var(returns, confidence_level=0.95):
    """
    Calculate Value at Risk (VaR)
    Example: "95% chance you won't lose more than X% in a day"
    """
    if len(returns) == 0:
        return 0
    
    # Historical VaR
    var = np.percentile(returns, (1 - confidence_level) * 100)
    return var

def calculate_cvar(returns, confidence_level=0.95):
    """
    Calculate Conditional Value at Risk (CVaR)
    Average loss on worst-case days
    """
    if len(returns) == 0:
        return 0
    
    var = calculate_var(returns, confidence_level)
    cvar = returns[returns <= var].mean()
    return cvar if not np.isnan(cvar) else var

def calculate_sharpe_ratio(returns, risk_free_rate=0.02):
    """
    Calculate Sharpe Ratio (risk-adjusted return)
    Higher = better risk-adjusted performance
    """
    if len(returns) == 0 or returns.std() == 0:
        return 0
    
    excess_returns = returns - risk_free_rate/252  # Daily risk-free rate
    return np.sqrt(252) * excess_returns.mean() / excess_returns.std()

def calculate_sortino_ratio(returns, risk_free_rate=0.02):
    """
    Calculate Sortino Ratio (downside risk-adjusted return)
    Like Sharpe but only penalizes downside volatility
    """
    if len(returns) == 0:
        return 0
    
    excess_returns = returns - risk_free_rate/252
    downside_returns = returns[returns < 0]
    
    if len(downside_returns) == 0 or downside_returns.std() == 0:
        return 0
    
    return np.sqrt(252) * excess_returns.mean() / downside_returns.std()

# Test the functions immediately
if __name__ == "__main__":
    # This will only run when calculations.py is executed directly
    print("Enhanced calculations module loaded successfully!")
    print("Functions defined: calculate_sma(), identify_runs(), calculate_daily_returns(), calculate_rsi(), calculate_bollinger_bands()")