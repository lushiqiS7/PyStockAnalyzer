"""
Advanced calculations module for stock analysis.

This module provides advanced financial calculation functions that extend
the basic calculations for more sophisticated stock analysis.
"""

import pandas as pd

from calculations import calculate_sma, calculate_daily_returns


def calculate_max_profit(prices):
    """
    Calculate the maximum profit that could be achieved from buying and selling stocks.
    
    This function implements a greedy approach where it assumes you can buy and sell
    multiple times to maximize profit. It calculates profit by summing all positive
    price changes (buying at each local minimum and selling at each local maximum).
    
    Args:
        prices (list or array-like): A sequence of stock prices in chronological order.
        
    Returns:
        float: The maximum profit that could be achieved. Returns 0 if no profit
               is possible (prices only decline or stay flat).
               
    Example:
        >>> prices = [7, 1, 5, 3, 6, 4]
        >>> calculate_max_profit(prices)
        7  # Buy at 1, sell at 5 (profit: 4), buy at 3, sell at 6 (profit: 3)
    """
    max_profit = 0
    
    # Iterate through prices starting from the second day
    for i in range(1, len(prices)):
        # If today's price is higher than yesterday's, add the difference to profit
        if prices[i] > prices[i-1]:
            max_profit += prices[i] - prices[i-1]
            
    return max_profit

def run_validation_tests():
    """
    Run comprehensive validation tests for the calculation functions.
    
    This function attempts to delegate to a dedicated validation module,
    but falls back to basic built-in tests if the validation module
    is not available. The tests verify the correctness of:
    - Simple Moving Average (SMA) calculations
    - Maximum profit calculations
    - Daily returns calculations
    
    The function prints test results to the console and is primarily
    used for development and debugging purposes.
    
    Returns:
        None: Results are printed to console.
        
    Note:
        This function is designed to work both with and without the
        dedicated validation.py module for better robustness.
    """
    try:
        # Try to use the dedicated validation module
        from validation import run_all_validations
        run_all_validations()
    except ImportError:
        # Fall back to basic validation tests if validation module is not available
        print("Running basic validation tests...")
        
        # Test 1: Simple Moving Average (SMA) calculation
        test_data = pd.DataFrame({'Close': [10, 12, 15, 13, 16, 18, 17]})
        sma_3 = calculate_sma(test_data, 3).tolist()
        expected_sma_3 = [None, None, 12.33, 13.33, 14.67, 15.67, 17.00]

        # Round values for comparison (floating point precision handling)
        sma_rounded = [round(x, 2) if x is not None else None for x in sma_3]
        expected_rounded = [round(x, 2) if x is not None else None for x in expected_sma_3]

        print(f"SMA Test: {sma_rounded[2:] == expected_rounded[2:]}")
        
        # Test 2: Maximum profit calculation
        test_prices = [7, 1, 5, 3, 6, 4]
        max_profit = calculate_max_profit(test_prices)
        # Expected: Buy at 1, sell at 5 (profit: 4); buy at 3, sell at 6 (profit: 3) = 7 total
        print(f"Max Profit Test: {max_profit == 7}")
        
        # Test 3: Daily returns calculation
        daily_returns = calculate_daily_returns(test_data).tolist()
        print(f"Daily Returns Test: {len(daily_returns) == len(test_data)}")
        
        print("Basic validation tests completed!")

# Test the functions immediately when script is run directly
if __name__ == "__main__":
    """
    Entry point for direct script execution.
    
    This block runs validation tests when the module is executed directly
    (e.g., python advanced_calculations.py) but not when imported as a module.
    """
    run_validation_tests()