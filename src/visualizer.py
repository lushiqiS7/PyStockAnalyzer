"""
Visualization module for stock data analysis.

This module provides comprehensive visualization capabilities for stock market data
including multi-panel charts with technical indicators, trend highlighting, and
detailed analysis results display. It creates professional-quality charts suitable
for technical analysis and investment decision-making.

Key Features:
- Multi-panel chart layouts with price, RSI, and volume
- Technical indicators: SMA, Bollinger Bands, RSI
- Run period highlighting for trend visualization
- Comprehensive analysis results formatting
- Professional chart styling and formatting

Dependencies:
- matplotlib: Chart creation and visualization
- pandas: Data manipulation and analysis
- Custom calculation modules for technical indicators
"""

import matplotlib.pyplot as plt
import pandas as pd
from calculations import (calculate_sma, calculate_rsi, calculate_bollinger_bands, 
                         identify_run_periods)


def plot_stock_data(df, sma_window=5):
    """
    Create comprehensive multi-panel stock analysis charts.
    
    This function generates a professional 3-panel chart layout displaying:
    1. Price chart with SMA, Bollinger Bands, and trend run highlighting
    2. RSI oscillator with overbought/oversold levels
    3. Trading volume bar chart
    
    The visualization includes trend run highlighting to identify consecutive
    periods of upward or downward price movements, making it easier to spot
    trending behavior and potential reversal points.
    
    Args:
        df (pandas.DataFrame): Stock data with columns ['Close', 'Volume'] and datetime index.
                              Must contain sufficient data for technical indicator calculations.
        sma_window (int, optional): Window size for Simple Moving Average calculation.
                                   Defaults to 5. Must be positive integer.
    
    Returns:
        None: Displays the chart using matplotlib.pyplot.show().
        
    Example:
        >>> data = fetch_stock_data("AAPL", "6mo")
        >>> plot_stock_data(data, sma_window=20)
        # Displays comprehensive 3-panel analysis chart
        
    Note:
        - Run periods of 2+ days are highlighted to reduce visual clutter
        - RSI values above 70 are considered overbought (red line)
        - RSI values below 30 are considered oversold (green line)
        - Bollinger Bands show volatility and potential support/resistance levels
    """
    # Create figure with 3 vertically stacked subplots
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 10))
    
    # =============== GET TREND RUN DATA ===============
    run_periods = identify_run_periods(df)
    
    # =============== PANEL 1: PRICE WITH TECHNICAL INDICATORS ===============
    # Plot main price line
    ax1.plot(df.index, df['Close'], label='Closing Price', color='blue', alpha=0.7)
    
    # Highlight significant trend runs (2+ days)
    upward_run_labeled = False
    downward_run_labeled = False
    
    for run in run_periods:
        start_date = run['start_date']
        end_date = run['end_date']
        direction = run['direction']
        length = run['length']
        
        # Only highlight runs of 2 or more days to avoid visual clutter
        if length >= 2:
            if direction == 1:  # Upward run
                label = 'Upward Run' if not upward_run_labeled else ""
                ax1.axvspan(start_date, end_date, alpha=0.2, color='green', label=label)
                upward_run_labeled = True
            elif direction == -1:  # Downward run
                label = 'Downward Run' if not downward_run_labeled else ""
                ax1.axvspan(start_date, end_date, alpha=0.2, color='red', label=label)
                downward_run_labeled = True
    
    # Calculate and plot Simple Moving Average
    sma = calculate_sma(df, sma_window)
    ax1.plot(df.index, sma, label=f'SMA ({sma_window} days)', color='red', linewidth=2)
    
    # Calculate and plot Bollinger Bands
    upper_band, middle_band, lower_band = calculate_bollinger_bands(df, window=20, num_std=2)
    ax1.plot(df.index, upper_band, label='Upper Bollinger Band', 
             color='green', linestyle='--', alpha=0.7)
    ax1.plot(df.index, lower_band, label='Lower Bollinger Band', 
             color='red', linestyle='--', alpha=0.7)
    ax1.fill_between(df.index, lower_band, upper_band, alpha=0.1, color='gray')
    
    # Format price panel
    ax1.set_title('Stock Price with Technical Indicators and Run Highlighting', fontweight='bold')
    ax1.set_ylabel('Price ($)', fontweight='bold')
    ax1.legend(fontsize=8)
    ax1.grid(True, alpha=0.3)
    
    # =============== PANEL 2: RSI OSCILLATOR ===============
    rsi = calculate_rsi(df, window=14)
    ax2.plot(df.index, rsi, label='RSI (14)', color='purple', linewidth=2)
    
    # Add overbought/oversold reference lines
    ax2.axhline(70, color='red', linestyle='--', alpha=0.7, label='Overbought (70)')
    ax2.axhline(30, color='green', linestyle='--', alpha=0.7, label='Oversold (30)')
    ax2.axhline(50, color='gray', linestyle='-', alpha=0.5, label='Neutral (50)')
    
    # Format RSI panel
    ax2.set_ylabel('RSI', fontweight='bold')
    ax2.set_ylim(0, 100)
    ax2.legend(fontsize=8)
    ax2.grid(True, alpha=0.3)
    
    # =============== PANEL 3: TRADING VOLUME ===============
    ax3.bar(df.index, df['Volume'], alpha=0.7, color='orange', width=1)
    
    # Format volume panel
    ax3.set_ylabel('Volume', fontweight='bold')
    ax3.set_xlabel('Date', fontweight='bold')
    ax3.grid(True, alpha=0.3)
    
    # =============== FINALIZE CHART ===============
    plt.tight_layout()
    plt.show()

def display_analysis_results(df, sma_window=5):
    """
    Display comprehensive formatted analysis results to console.
    
    This function calculates and displays a detailed analysis report including
    all technical indicators, statistical measures, and trading insights.
    The output is formatted for easy reading and provides actionable information
    for investment decision-making.
    
    Args:
        df (pandas.DataFrame): Stock data with 'Close' column and datetime index.
        sma_window (int, optional): Window size for SMA calculation. Defaults to 5.
    
    Returns:
        None: Prints formatted results to console.
        
    Calculations Include:
        - Simple Moving Average analysis
        - Price run pattern analysis (trending behavior)
        - Daily returns statistics (mean, volatility)
        - Maximum profit analysis (trading opportunities)
        - RSI momentum analysis (overbought/oversold conditions)
        - Bollinger Bands volatility analysis
        - Overall performance summary
        
    Example:
        >>> data = fetch_stock_data("AAPL", "1y")
        >>> display_analysis_results(data, sma_window=20)
        # Prints comprehensive analysis report to console
    """
    # Import required calculation functions
    from calculations import (calculate_sma, identify_runs, calculate_daily_returns, 
                            calculate_rsi, calculate_bollinger_bands)
    from advanced_calculations import calculate_max_profit
    
    # =============== CALCULATE ALL METRICS ===============
    sma = calculate_sma(df, sma_window)
    runs_data = identify_runs(df)
    returns = calculate_daily_returns(df)
    max_profit = calculate_max_profit(df['Close'].tolist())
    rsi = calculate_rsi(df, window=14)
    upper_band, middle_band, lower_band = calculate_bollinger_bands(df, window=20, num_std=2)
    
    # =============== DISPLAY FORMATTED RESULTS ===============
    print("=" * 60)
    print("ENHANCED STOCK ANALYSIS RESULTS")
    print("=" * 60)
    
    # Moving Average Analysis
    print(f"\n1. SIMPLE MOVING AVERAGE ({sma_window} days):")
    print(f"   Latest SMA value: ${sma.iloc[-1]:.2f}")
    current_price = df['Close'].iloc[-1]
    sma_position = "Above" if current_price > sma.iloc[-1] else "Below"
    sma_signal = "Bullish" if current_price > sma.iloc[-1] else "Bearish"
    print(f"   Current price position: {sma_position} SMA ({sma_signal} signal)")
    
    # Trend Run Analysis
    print(f"\n2. PRICE RUN ANALYSIS:")
    print(f"   Total upward days: {runs_data['total_up_days']}")
    print(f"   Total downward days: {runs_data['total_down_days']}")
    print(f"   Longest upward streak: {runs_data['longest_up_streak']} days")
    print(f"   Longest downward streak: {runs_data['longest_down_streak']} days")
    
    # Calculate trend bias
    total_directional_days = runs_data['total_up_days'] + runs_data['total_down_days']
    if total_directional_days > 0:
        upward_bias = (runs_data['total_up_days'] / total_directional_days) * 100
        print(f"   Overall trend bias: {upward_bias:.1f}% upward")
    
    # Volatility and Returns Analysis
    print(f"\n3. DAILY RETURNS ANALYSIS:")
    print(f"   Average daily return: {returns.mean():.4f} ({returns.mean()*100:.2f}%)")
    print(f"   Return volatility (std dev): {returns.std():.4f} ({returns.std()*100:.2f}%)")
    print(f"   Best single day: {returns.max():.4f} ({returns.max()*100:.2f}%)")
    print(f"   Worst single day: {returns.min():.4f} ({returns.min()*100:.2f}%)")
    
    # Profit Analysis
    print(f"\n4. MAXIMUM PROFIT ANALYSIS:")
    print(f"   Maximum achievable profit: ${max_profit:.2f}")
    print(f"   (Perfect timing with multiple transactions)")
    if len(df) > 0:
        profit_percentage = (max_profit / df['Close'].iloc[0]) * 100
        print(f"   Profit percentage: {profit_percentage:.2f}%")
    
    # RSI Momentum Analysis
    print(f"\n5. RELATIVE STRENGTH INDEX (RSI - 14 day):")
    current_rsi = rsi.iloc[-1]
    print(f"   Current RSI: {current_rsi:.2f}")
    
    # RSI interpretation with detailed explanations
    if current_rsi > 70:
        rsi_interpretation = "Overbought (>70) - Potential sell signal, price may decline"
    elif current_rsi < 30:
        rsi_interpretation = "Oversold (<30) - Potential buy signal, price may recover"
    else:
        rsi_interpretation = "Neutral (30-70) - No strong momentum signal"
    print(f"   Interpretation: {rsi_interpretation}")
    print(f"   RSI Range: {rsi.min():.2f} to {rsi.max():.2f}")
    
    # Bollinger Bands Volatility Analysis
    print(f"\n6. BOLLINGER BANDS ANALYSIS (20-day, 2σ):")
    
    # Band position analysis
    if current_price > upper_band.iloc[-1]:
        band_position = "Above Upper Band - Potentially Overbought"
        band_signal = "Consider selling or waiting for pullback"
    elif current_price < lower_band.iloc[-1]:
        band_position = "Below Lower Band - Potentially Oversold" 
        band_signal = "Consider buying or wait for confirmation"
    else:
        band_position = "Within Normal Trading Range"
        band_signal = "No strong price extreme signal"
    
    print(f"   Current position: {band_position}")
    print(f"   Trading signal: {band_signal}")
    
    # Volatility measurement
    band_width = (upper_band.iloc[-1] - lower_band.iloc[-1]) / middle_band.iloc[-1] * 100
    print(f"   Band width: {band_width:.2f}% (Higher = More volatile period)")
    print(f"   Upper: ${upper_band.iloc[-1]:.2f} | Middle: ${middle_band.iloc[-1]:.2f} | Lower: ${lower_band.iloc[-1]:.2f}")
    
    # Overall Data Summary
    print(f"\n7. DATA SUMMARY:")
    print(f"   Analysis period: {df.index[0].date()} to {df.index[-1].date()}")
    print(f"   Total trading days: {len(df)}")
    print(f"   Starting price: ${df['Close'].iloc[0]:.2f}")
    print(f"   Ending price: ${df['Close'].iloc[-1]:.2f}")
    print(f"   Highest price: ${df['High'].max():.2f}")
    print(f"   Lowest price: ${df['Low'].min():.2f}")
    
    # Performance calculation
    total_change = ((df['Close'].iloc[-1] / df['Close'].iloc[0]) - 1) * 100
    print(f"   Total period change: {total_change:.2f}%")
    
    # Annualized return estimation
    days_in_period = len(df)
    if days_in_period > 30:  # Only calculate if sufficient data
        annual_return = (((df['Close'].iloc[-1] / df['Close'].iloc[0]) ** (252/days_in_period)) - 1) * 100
        print(f"   Annualized return estimate: {annual_return:.2f}%")
    
    print("\n" + "=" * 60)

# Entry point for direct script execution
if __name__ == "__main__":
    """
    Entry point for direct script execution.
    
    When this module is run directly, it displays information about the
    available visualization functions and their enhanced capabilities.
    """
    print("Enhanced visualization module loaded successfully!")
    print("\nAvailable functions:")
    print("- plot_stock_data(): Create comprehensive multi-panel charts")
    print("  * Price with SMA and Bollinger Bands")
    print("  * RSI oscillator with overbought/oversold levels") 
    print("  * Trading volume visualization")
    print("  * Trend run highlighting")
    print("\n- display_analysis_results(): Comprehensive console analysis report")
    print("  * Technical indicators analysis")
    print("  * Trading signals and interpretations")
    print("  * Statistical performance metrics")
    print("  * Risk and volatility assessment")
    print("\nNow includes advanced technical analysis with RSI and Bollinger Bands!")