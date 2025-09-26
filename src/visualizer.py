import matplotlib.pyplot as plt
import pandas as pd
from calculations import calculate_sma, calculate_rsi, calculate_bollinger_bands, identify_run_periods

def plot_stock_data(df, sma_window=5):
    """
    Enhanced plotting with RSI, Bollinger Bands subplots, and run highlighting
    """
    # Create figure with subplots
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 10))
    
    # Get run periods for highlighting
    run_periods = identify_run_periods(df)
    
    # Plot 1: Price with SMA and Bollinger Bands
    ax1.plot(df.index, df['Close'], label='Closing Price', color='blue', alpha=0.7)
    
    # Highlight upward and downward runs
    upward_run_labeled = False
    downward_run_labeled = False
    
    for run in run_periods:
        start_date = run['start_date']
        end_date = run['end_date']
        direction = run['direction']
        length = run['length']
        
        # Only highlight runs of 2 or more days to avoid clutter
        if length >= 2:
            if direction == 1:  # Upward run
                label = 'Upward Run' if not upward_run_labeled else ""
                ax1.axvspan(start_date, end_date, alpha=0.2, color='green', label=label)
                upward_run_labeled = True
            elif direction == -1:  # Downward run
                label = 'Downward Run' if not downward_run_labeled else ""
                ax1.axvspan(start_date, end_date, alpha=0.2, color='red', label=label)
                downward_run_labeled = True
    
    # Calculate and plot SMA
    sma = calculate_sma(df, sma_window)
    ax1.plot(df.index, sma, label=f'SMA ({sma_window} days)', color='red', linewidth=2)
    
    # Calculate and plot Bollinger Bands
    upper_band, middle_band, lower_band = calculate_bollinger_bands(df, 20, 2)
    ax1.plot(df.index, upper_band, label='Upper Bollinger Band', color='green', linestyle='--', alpha=0.7)
    ax1.plot(df.index, lower_band, label='Lower Bollinger Band', color='red', linestyle='--', alpha=0.7)
    ax1.fill_between(df.index, lower_band, upper_band, alpha=0.1, color='gray')
    
    ax1.set_title('Stock Price with Technical Indicators and Run Highlighting')
    ax1.set_ylabel('Price ($)')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: RSI
    rsi = calculate_rsi(df, 14)
    ax2.plot(df.index, rsi, label='RSI (14)', color='purple', linewidth=2)
    ax2.axhline(70, color='red', linestyle='--', alpha=0.7, label='Overbought (70)')
    ax2.axhline(30, color='green', linestyle='--', alpha=0.7, label='Oversold (30)')
    ax2.set_ylabel('RSI')
    ax2.set_ylim(0, 100)
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # Plot 3: Volume
    ax3.bar(df.index, df['Volume'], alpha=0.7, color='orange')
    ax3.set_ylabel('Volume')
    ax3.set_xlabel('Date')
    ax3.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()

def display_analysis_results(df, sma_window=5):
    """
    Enhanced results display with new indicators
    """
    from calculations import calculate_sma, identify_runs, calculate_daily_returns, calculate_rsi, calculate_bollinger_bands
    from advanced_calculations import calculate_max_profit
    
    # Calculate all metrics
    sma = calculate_sma(df, sma_window)
    runs_data = identify_runs(df)
    returns = calculate_daily_returns(df)
    max_profit = calculate_max_profit(df['Close'].tolist())
    rsi = calculate_rsi(df, 14)
    upper_band, middle_band, lower_band = calculate_bollinger_bands(df, 20, 2)
    
    # Display results
    print("=" * 60)
    print("ENHANCED STOCK ANALYSIS RESULTS")
    print("=" * 60)
    
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
    
    # NEW: RSI Analysis
    print(f"\n5. RELATIVE STRENGTH INDEX (RSI):")
    print(f"   Current RSI: {rsi.iloc[-1]:.2f}")
    print(f"   RSI Interpretation: {'Overbought (>70)' if rsi.iloc[-1] > 70 else 'Oversold (<30)' if rsi.iloc[-1] < 30 else 'Neutral'}")
    print(f"   RSI Range: {rsi.min():.2f} to {rsi.max():.2f}")
    
    # NEW: Bollinger Bands Analysis
    print(f"\n6. BOLLINGER BANDS ANALYSIS:")
    print(f"   Current Price vs Bands: ", end="")
    current_price = df['Close'].iloc[-1]
    if current_price > upper_band.iloc[-1]:
        print("Above Upper Band (Overbought)")
    elif current_price < lower_band.iloc[-1]:
        print("Below Lower Band (Oversold)")
    else:
        print("Within Bands (Neutral)")
    print(f"   Band Width: {(upper_band.iloc[-1] - lower_band.iloc[-1]) / middle_band.iloc[-1] * 100:.2f}%")
    
    print(f"\n7. DATA SUMMARY:")
    print(f"   Period: {df.index[0].date()} to {df.index[-1].date()}")
    print(f"   Total trading days: {len(df)}")
    print(f"   Starting price: ${df['Close'].iloc[0]:.2f}")
    print(f"   Ending price: ${df['Close'].iloc[-1]:.2f}")
    print(f"   Total change: {((df['Close'].iloc[-1]/df['Close'].iloc[0])-1)*100:.2f}%")
    
    print("\n" + "=" * 60)

# Test the functions
if __name__ == "__main__":
    print("Enhanced visualization module loaded successfully!")
    print("Now includes RSI and Bollinger Bands analysis!")