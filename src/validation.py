"""
Validation and testing module for the PyStock Analyzer.

This module provides comprehensive validation and testing functionality
to ensure all components of the stock analysis system work correctly.
It includes unit tests, integration tests, and interface compatibility
tests for both GUI and web applications.

Key Features:
- Core calculation function validation
- Technical indicator accuracy testing
- Real-world data integration testing
- GUI and web interface compatibility checks
- Enhanced functionality verification (run highlighting, etc.)
- Comprehensive error handling and reporting

Test Categories:
1. Unit Tests: Individual function validation
2. Integration Tests: Component interaction testing
3. Interface Tests: GUI and web app compatibility
4. Data Tests: Real market data validation
"""

import pandas as pd
import numpy as np
import sys
import os

# Import all calculation modules for testing
from calculations import (calculate_sma, identify_runs, calculate_daily_returns, 
                         calculate_rsi, calculate_bollinger_bands, identify_run_periods)
from advanced_calculations import calculate_max_profit


def test_gui_imports():
    """
    Test GUI module imports and enhanced functionality compatibility.
    
    This function verifies that the GUI module can properly import and use
    all enhanced analysis functions, particularly the run highlighting
    functionality. It creates sample data and tests the run period
    identification to ensure visualization features work correctly.
    
    Returns:
        bool: True if all GUI imports and functionality tests pass, False otherwise.
        
    Tests:
        - GUI module import capability
        - Run period identification functionality
        - Sample data processing
        - Error handling and reporting
    """
    try:
        # Test GUI module import
        from gui import StockAnalyzerGUI
        print("✅ GUI imports successful - run highlighting should work")
        
        # Test the identify_run_periods function with sample data
        print("   Testing run period identification...")
        
        # Create realistic sample stock data with mixed price movements
        dates = pd.date_range(start='2024-01-01', periods=10, freq='D')
        prices = [100, 102, 101, 103, 105, 104, 102, 100, 98, 99]  # Mix of up/down moves
        sample_data = pd.DataFrame({
            'Close': prices
        }, index=dates)
        
        # Test run period identification
        run_periods = identify_run_periods(sample_data)
        print(f"✅ Found {len(run_periods)} run periods in sample data")
        
        # Display detailed run analysis for verification
        for i, run in enumerate(run_periods):
            direction_name = "Upward" if run['direction'] == 1 else "Downward" if run['direction'] == -1 else "Flat"
            print(f"   Run {i+1}: {direction_name} from {run['start_date'].date()} to {run['end_date'].date()} ({run['length']} days)")
        
        return True
        
    except Exception as e:
        print(f"❌ GUI imports failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_web_imports():
    """
    Test web application module imports and compatibility.
    
    This function verifies that the web application can properly import
    and use all analysis functions. It adds the webapp directory to the
    Python path and attempts to import the Flask application module.
    
    Returns:
        bool: True if web app imports successfully, False otherwise.
        
    Note:
        This test ensures that the web interface can access all the same
        analysis capabilities as the GUI interface.
    """
    try:
        # Add webapp directory to Python path for import
        webapp_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'webapp')
        sys.path.append(webapp_path)
        
        # Import web application module
        import app as app_module # type: ignore
        
        print("✅ Web app imports successful - run highlighting should work")
        return True
        
    except Exception as e:
        print(f"❌ Web app imports failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_run_highlighting_functionality():
    """
    Test enhanced run highlighting functionality across interfaces.
    
    This function performs comprehensive testing of the run highlighting
    feature that visualizes consecutive price movement periods. It tests
    both GUI and web interface compatibility to ensure the enhancement
    works across all user interfaces.
    
    Returns:
        bool: True if all interface tests pass, False otherwise.
        
    Tests Include:
        - GUI interface compatibility
        - Web interface compatibility  
        - Function integration verification
        - User guidance for testing
    """
    print("=" * 60)
    print("TESTING ENHANCED RUN HIGHLIGHTING FUNCTIONALITY")
    print("=" * 60)
    
    # Test GUI interface compatibility
    print("Testing GUI Interface...")
    gui_ok = test_gui_imports()
    print()
    
    # Test web interface compatibility
    print("Testing Web Interface...")
    web_ok = test_web_imports()
    
    # Summary and user guidance
    print("=" * 60)
    if gui_ok and web_ok:
        print("✅ All enhanced interface tests passed! Run highlighting should work in both GUI and web interfaces.")
        print("\nTo test the enhanced functionality:")
        print("- GUI: Run 'python src/main.py' and select GUI mode")  
        print("- Web: Run 'python webapp/app.py' and visit http://localhost:5000")
        print("- Look for colored background highlighting on charts showing trend runs")
    else:
        print("❌ Some enhanced interface tests failed. Check the errors above.")
        print("The basic functionality should still work, but enhanced features may be limited.")
    
    return gui_ok and web_ok

def run_comprehensive_validation():
    """
    Run comprehensive validation of all core calculation functionalities.
    
    This function performs extensive testing of all mathematical and analytical
    functions in the stock analysis system. It validates calculations against
    known expected results and tests integration with real market data.
    
    Test Coverage:
        1. Simple Moving Average calculation accuracy
        2. Price run analysis and pattern detection
        3. Daily returns calculation verification
        4. Maximum profit algorithm validation
        5. RSI (Relative Strength Index) calculation
        6. Bollinger Bands indicator testing
        7. Real-world data integration testing
        
    Returns:
        None: Prints detailed test results to console.
    """
    print("=" * 60)
    print("COMPREHENSIVE VALIDATION TESTS FOR PyStock Analyzer")
    print("=" * 60)
    
    # =============== CREATE TEST DATA ===============
    # Use realistic price sequence for testing
    test_data = pd.DataFrame({
        'Close': [10, 12, 15, 13, 16, 18, 17, 19, 22, 20]
    })
    
    # =============== TEST 1: SIMPLE MOVING AVERAGE ===============
    print("\n1. SIMPLE MOVING AVERAGE VALIDATION")
    print("   Testing SMA calculation accuracy...")
    
    sma_3 = calculate_sma(test_data, 3)
    print(f"   SMA(3) calculated values: {sma_3.tolist()}")
    
    # Manual calculation verification with proper NaN/None handling
    # SMA(3) for [10,12,15,13,16,18,17,19,22,20] should be:
    # [NaN, NaN, 12.33, 13.33, 14.67, 15.67, 17.0, 18.0, 19.33, 20.33]
    expected_sma_3 = [None, None, 12.33, 13.33, 14.67, 15.67, 17.0, 18.0, 19.33, 20.33]
    
    # Convert both to comparable format (rounded for floating point comparison)
    sma_rounded = [round(x, 2) if not pd.isna(x) else None for x in sma_3]
    expected_rounded = [round(x, 2) if x is not None else None for x in expected_sma_3]
    
    print(f"   Rounded SMA values: {sma_rounded}")
    print(f"   Expected values:    {expected_rounded}")
    sma_test_passed = sma_rounded == expected_rounded
    print(f"   ✅ SMA Test: {'PASSED' if sma_test_passed else 'FAILED'}")
    
    # =============== TEST 2: PRICE RUNS ANALYSIS ===============
    print("\n2. PRICE RUNS ANALYSIS VALIDATION")
    print("   Testing consecutive price movement detection...")
    
    runs_data = identify_runs(test_data)
    print(f"   Run analysis results: {runs_data}")
    
    # Verify run statistics make sense
    total_days = len(test_data) - 1  # First day has no direction
    total_analyzed = runs_data['total_up_days'] + runs_data['total_down_days']
    print(f"   Total trading days analyzed: {total_analyzed}/{total_days}")
    print(f"   Longest upward streak: {runs_data['longest_up_streak']} days")
    print(f"   Longest downward streak: {runs_data['longest_down_streak']} days")
    print(f"   ✅ Run Analysis: COMPLETED")
    
    # =============== TEST 3: DAILY RETURNS ===============
    print("\n3. DAILY RETURNS VALIDATION")
    print("   Testing percentage change calculations...")
    
    returns = calculate_daily_returns(test_data)
    returns_list = returns.tolist()
    print(f"   Daily returns: {[round(x, 4) if not pd.isna(x) else None for x in returns_list]}")
    
    # Verify first value is NaN (no previous day for comparison)
    first_return_is_nan = pd.isna(returns.iloc[0])
    print(f"   First return is NaN (expected): {first_return_is_nan}")
    print(f"   ✅ Daily Returns Test: {'PASSED' if first_return_is_nan else 'FAILED'}")
    
    # =============== TEST 4: MAXIMUM PROFIT ALGORITHM ===============
    print("\n4. MAXIMUM PROFIT VALIDATION")
    print("   Testing optimal trading strategy calculation...")
    
    # Use the example from the requirements: [7,1,5,3,6,4] should yield profit of 7
    test_prices = [7, 1, 5, 3, 6, 4]
    max_profit = calculate_max_profit(test_prices)
    expected_profit = 7  # Buy at 1, sell at 5 (profit: 4); buy at 3, sell at 6 (profit: 3)
    
    print(f"   Test prices: {test_prices}")
    print(f"   Calculated max profit: ${max_profit}")
    print(f"   Expected max profit: ${expected_profit}")
    profit_test_passed = max_profit == expected_profit
    print(f"   ✅ Max Profit Test: {'PASSED' if profit_test_passed else 'FAILED'}")
    
    # =============== TEST 5: RSI CALCULATION ===============
    print("\n5. RELATIVE STRENGTH INDEX (RSI) VALIDATION")
    print("   Testing momentum oscillator calculation...")
    
    # Test with our sample data (use smaller window for limited data)
    rsi_test = calculate_rsi(test_data, window=6)
    rsi_values = rsi_test.tolist()
    print(f"   RSI values: {[round(x, 2) if not pd.isna(x) else None for x in rsi_values]}")
    
    # Verify RSI is bounded between 0 and 100
    valid_rsi = rsi_test.dropna()
    rsi_bounded = all((0 <= val <= 100) for val in valid_rsi)
    print(f"   RSI values bounded (0-100): {rsi_bounded}")
    print(f"   ✅ RSI Test: {'PASSED' if rsi_bounded else 'FAILED'}")
    
    # =============== TEST 6: BOLLINGER BANDS ===============
    print("\n6. BOLLINGER BANDS VALIDATION")
    print("   Testing volatility indicator calculation...")
    
    # Use all available data for Bollinger Bands (adjust window for small dataset)
    upper_band, middle_band, lower_band = calculate_bollinger_bands(test_data, window=10, num_std=2)
    
    # Extract non-NaN values for validation
    valid_mask = ~upper_band.isna()
    upper_valid = upper_band[valid_mask]
    middle_valid = middle_band[valid_mask]
    lower_valid = lower_band[valid_mask]
    
    print(f"   Upper Band (valid): {[round(x, 2) for x in upper_valid.tolist()]}")
    print(f"   Middle Band (valid): {[round(x, 2) for x in middle_valid.tolist()]}")
    print(f"   Lower Band (valid): {[round(x, 2) for x in lower_valid.tolist()]}")
    
    # Test logical relationship: Upper >= Middle >= Lower
    if len(upper_valid) > 0:
        bands_logical = all(upper_valid >= middle_valid) and all(middle_valid >= lower_valid)
        print(f"   Band ordering correct (Upper ≥ Middle ≥ Lower): {bands_logical}")
        print(f"   ✅ Bollinger Bands Test: {'PASSED' if bands_logical else 'FAILED'}")
    else:
        print(f"   ⚠️  Bollinger Bands Test: INSUFFICIENT DATA (need larger dataset)")
    
    # =============== TEST 7: REAL-WORLD DATA INTEGRATION ===============
    print("\n7. REAL-WORLD DATA INTEGRATION TEST")
    print("   Testing with live market data...")
    
    try:
        from data_loader import fetch_stock_data
        
        # Fetch recent Apple stock data
        real_data = fetch_stock_data("AAPL", "1mo")
        
        if real_data is not None and len(real_data) > 20:
            print("   ✅ Successfully fetched real market data")
            
            # Test all functions with real data
            sma_real = calculate_sma(real_data, 5)
            runs_real = identify_runs(real_data)
            returns_real = calculate_daily_returns(real_data)
            profit_real = calculate_max_profit(real_data['Close'].tolist())
            rsi_real = calculate_rsi(real_data, 14)
            upper_real, middle_real, lower_real = calculate_bollinger_bands(real_data, 20, 2)
            
            print(f"   ✅ All calculations completed successfully:")
            print(f"      - SMA data points: {sma_real.shape[0]}")
            print(f"      - Run analysis: {runs_real['total_up_days']} up, {runs_real['total_down_days']} down days")
            print(f"      - Returns stats: mean={returns_real.mean():.4f}, std={returns_real.std():.4f}")
            print(f"      - Max profit opportunity: ${profit_real:.2f}")
            print(f"      - RSI range: {rsi_real.min():.2f} to {rsi_real.max():.2f}")
            print(f"      - Bollinger Bands calculated: {len(upper_real.dropna())} valid points")
            print("   ✅ Real-World Integration Test: PASSED")
        else:
            print("   ⚠️  Real-World Integration Test: FAILED - Could not fetch sufficient data")
            
    except Exception as e:
        print(f"   ❌ Real-World Integration Test: FAILED - {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 60)
    print("COMPREHENSIVE VALIDATION COMPLETE")
    print("=" * 60)


def run_all_validations():
    """
    Execute all validation tests for the PyStock Analyzer system.
    
    This master function runs both the comprehensive calculation validation
    and the enhanced interface functionality tests. It provides a complete
    test suite to verify system integrity and feature compatibility.
    
    Test Suites:
        1. Comprehensive calculation validation
        2. Enhanced interface functionality testing
        3. Integration and compatibility verification
        
    Returns:
        None: Prints detailed test results and recommendations to console.
    """
    print("🔍 Starting complete validation test suite for PyStock Analyzer...")
    print()
    
    # Run core functionality validation
    run_comprehensive_validation()
    
    print("\n")
    
    # Run enhanced interface testing
    test_run_highlighting_functionality()
    
    print("\n🎉 All validation tests completed!")
    print("Check the results above for any issues that need attention.")


# Entry point for direct script execution
if __name__ == "__main__":
    """
    Entry point for direct script execution.
    
    When this module is run directly, it executes the complete validation
    test suite to verify all system components are working correctly.
    """
    run_all_validations()