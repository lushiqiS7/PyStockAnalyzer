import matplotlib.pyplot as plt
import pandas as pd
from calculations import calculate_sma, identify_runs

def plot_stock_data(df, sma_window=5):
    """
    Plots the closing price and SMA, and highlights upward/downward runs.
    
    Args:
        df (pandas.DataFrame): DataFrame containing stock data.
        sma_window (int): The window size for the SMA calculation.
    """
    # Calculate SMA
    sma = calculate_sma(df, sma_window)
    
    # Identify runs
    runs_data = identify_runs(df)
    
    # Create the plot
    plt.figure(figsize=(12, 6))
    
    # Plot closing price
    plt.plot(df.index, df['Close'], label='Closing Price', color='blue', alpha=0.5)
    
    # Plot SMA
    plt.plot(df.index, sma, label=f'SMA ({sma_window} days)', color='red')
    
    # Highlight upward and downward runs
    current_streak = 0
    current_direction = 0
    start_index = None
    
    for i in range(1, len(df)):
        price_change = df['Close'].iloc[i] - df['Close'].iloc[i-1]
        direction = 1 if price_change > 0 else (-1 if price_change < 0 else 0)
        
        if direction == current_direction:
            current_streak += 1
        else:
            if current_streak >= 2:  # Only highlight streaks of 2+ days
                end_index = df.index[i-1]
                color = 'green' if current_direction == 1 else 'red'
                if current_direction != 0:
                    plt.axvspan(start_index, end_index, color=color, alpha=0.1)
            current_streak = 1
            current_direction = direction
            start_index = df.index[i-1]
    
    plt.title('Stock Price with SMA and Trend Highlights')
    plt.xlabel('Date')
    plt.ylabel('Price ($)')
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def display_analysis_results(df, sma_window=5):
    """
    Displays all analysis results in a formatted way.
    
    Args:
        df (pandas.DataFrame): DataFrame containing stock data.
        sma_window (int): The window size for the SMA calculation.
    """
    from calculations import calculate_sma, identify_runs, calculate_daily_returns
    from advanced_calculations import calculate_max_profit
    
    # Calculate all metrics
    sma = calculate_sma(df, sma_window)
    runs_data = identify_runs(df)
    returns = calculate_daily_returns(df)
    max_profit = calculate_max_profit(df['Close'].tolist())
    
    # Display results
    print("=" * 50)
    print("STOCK ANALYSIS RESULTS")
    print("=" * 50)
    
    print(f"\n1. SIMPLE MOVING AVERAGE ({sma_window} days):")
    print(f"   Latest SMA value: ${sma.iloc[-1]:.2f}")
    
    print(f"\n2. PRICE RUN ANALYSIS:")
    print(f"   Total upward days: {runs_data['total_up_days']}")
    print(f"   Total downward days: {runs_data['total_down_days']}")
    print(f"   Longest upward streak: {runs_data['longest_up_streak']} days")
    print(f"   Longest downward streak: {runs_data['longest_down_streak']} days")
    
    print(f"\n3. DAILY RETURNS:")
    print(f"   Average daily return: {returns.mean():.4f}")
    print(f"   Return volatility (std dev): {returns.std():.4f}")
    
    print(f"\n4. MAXIMUM PROFIT ANALYSIS:")
    print(f"   Maximum achievable profit: ${max_profit:.2f}")
    print(f"   (Multiple transactions allowed)")
    
    print("\n" + "=" * 50)

# Test the functions
if __name__ == "__main__":
    print("Visualization module loaded successfully!")
    print("Functions: plot_stock_data(), display_analysis_results()")