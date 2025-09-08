import pandas as pd
import numpy as np
from calculations import calculate_sma, identify_runs, calculate_daily_returns, calculate_rsi, calculate_bollinger_bands
from advanced_calculations import calculate_max_profit

def run_comprehensive_validation():
    """Run comprehensive validation of all core functionalities."""
    print("=" * 60)
    print("VALIDATION TESTS FOR PyStock Analyzer")
    print("=" * 60)
    
    # Create test data
    test_data = pd.DataFrame({
        'Close': [10, 12, 15, 13, 16, 18, 17, 19, 22, 20]
    })
    
    # Test 1: Simple Moving Average
    print("\n1. SIMPLE MOVING AVERAGE VALIDATION")
    sma_3 = calculate_sma(test_data, 3)
    print(f"SMA(3) values: {sma_3.tolist()}")
    
    # Manual calculation check with proper NaN/None handling
    manual_sma_3 = [None, None, 12.33, 13.33, 14.67, 15.67, 17.0, 18.0, 19.33, 20.33]
    
    # Convert both to comparable format
    sma_rounded = [round(x, 2) if not pd.isna(x) else None for x in sma_3]
    manual_rounded = [round(x, 2) if x is not None else None for x in manual_sma_3]
    
    print(f"Rounded SMA values: {sma_rounded}")
    print(f"Expected values: {manual_rounded}")
    print(f"Manual check: {sma_rounded == manual_rounded}")
    
    # Test 2: Price Runs
    print("\n2. PRICE RUNS VALIDATION")
    runs_data = identify_runs(test_data)
    print(f"Runs data: {runs_data}")
    
    # Test 3: Daily Returns
    print("\n3. DAILY RETURNS VALIDATION")
    returns = calculate_daily_returns(test_data)
    print(f"Daily returns: {returns.tolist()}")
    
    # Test 4: Max Profit
    print("\n4. MAX PROFIT VALIDATION")
    test_prices = [7, 1, 5, 3, 6, 4]  # From requirements example
    max_profit = calculate_max_profit(test_prices)
    print(f"Max profit for [7,1,5,3,6,4]: {max_profit}, Expected: 7")
    
    # Test 5: Integration with real data
    print("\n5. INTEGRATION TEST WITH REAL DATA")
    try:
        from data_loader import fetch_stock_data
        data = fetch_stock_data("AAPL", "1mo")
        if data is not None:
            sma = calculate_sma(data, 5)
            runs = identify_runs(data)
            returns = calculate_daily_returns(data)
            profit = calculate_max_profit(data['Close'].tolist())
            
            print("✓ All functions work with real AAPL data")
            print(f"  SMA shape: {sma.shape}")
            print(f"  Runs data: {runs}")
            print(f"  Returns stats: mean={returns.mean():.4f}, std={returns.std():.4f}")
            print(f"  Max profit: ${profit:.2f}")
        else:
            print("✗ Failed to fetch real data")
    except Exception as e:
        print(f"✗ Integration test failed: {e}")

    # NEW: Test Bollinger Bands with appropriate window
    print("\n6. BOLLINGER BANDS VALIDATION")
    # Use smaller window for test data
    upper_band, middle_band, lower_band = calculate_bollinger_bands(test_data, 10, 2)
    
    # Get non-NaN values
    valid_mask = ~upper_band.isna()
    upper_valid = upper_band[valid_mask]
    middle_valid = middle_band[valid_mask]
    lower_valid = lower_band[valid_mask]
    
    print(f"Upper Band values (non-NaN): {upper_valid.tolist()}")
    print(f"Middle Band values (non-NaN): {middle_valid.tolist()}")
    print(f"Lower Band values (non-NaN): {lower_valid.tolist()}")
    
    # Test that bands make logical sense (only where we have values)
    if len(upper_valid) > 0:
        valid_bands = all(upper_valid >= middle_valid) and all(middle_valid >= lower_valid)
        print(f"Bands logical check: {valid_bands}")
    else:
        print("Bands logical check: Not enough data for validation")
    
    # Test 7: Integration with real data
    print("\n7. INTEGRATION TEST WITH REAL DATA")
    try:
        from data_loader import fetch_stock_data
        data = fetch_stock_data("AAPL", "1mo")
        if data is not None:
            sma = calculate_sma(data, 5)
            runs = identify_runs(data)
            returns = calculate_daily_returns(data)
            profit = calculate_max_profit(data['Close'].tolist())
            rsi_real = calculate_rsi(data, 14)
            upper_band_real, middle_band_real, lower_band_real = calculate_bollinger_bands(data, 20, 2)
            
            print("✓ All functions work with real AAPL data")
            print(f"  SMA shape: {sma.shape}")
            print(f"  Runs data: {runs}")
            print(f"  Returns stats: mean={returns.mean():.4f}, std={returns.std():.4f}")
            print(f"  Max profit: ${profit:.2f}")
            print(f"  RSI range: {rsi_real.min():.2f} to {rsi_real.max():.2f}")
            print(f"  Bollinger Bands calculated: {len(upper_band_real[~upper_band_real.isna()]) > 0}")
        else:
            print("✗ Failed to fetch real data")
    except Exception as e:
        print(f"✗ Integration test failed: {e}")
    
    print("\n" + "=" * 60)
    print("ENHANCED VALIDATION COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    run_comprehensive_validation()