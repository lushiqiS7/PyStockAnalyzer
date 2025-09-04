import pandas as pd

from calculations import calculate_sma, calculate_daily_returns

def calculate_max_profit(prices):
    """
    Solves the "Best Time to Buy and Sell Stock II" problem.
    Calculates maximum profit from multiple buy-sell transactions.
    
    Args:
        prices (list or pandas.Series): Array of stock prices.
        
    Returns:
        float: Maximum profit achievable.
    """
    max_profit = 0
    for i in range(1, len(prices)):
        if prices[i] > prices[i-1]:
            max_profit += prices[i] - prices[i-1]
    return max_profit

def run_validation_tests():
    """
    Runs validation tests against manual calculations to ensure correctness.
    """
    print("Running validation tests...")
    
    # Test 1: Simple SMA calculation
    test_data = pd.DataFrame({'Close': [10, 12, 15, 13, 16, 18, 17]})
    sma_3 = calculate_sma(test_data, 3).tolist()
    expected_sma_3 = [None, None, 12.33, 13.33, 14.67, 15.67, 17.00]

    sma_rounded = [round(x, 2) if x is not None else None for x in sma_3]
    expected_rounded = [round(x, 2) if x is not None else None for x in expected_sma_3]

    print(f"SMA Test: {sma_rounded[2:] == expected_rounded[2:]}")
    # Test 2: Max Profit calculation
    test_prices = [7, 1, 5, 3, 6, 4]
    max_profit = calculate_max_profit(test_prices)
    print(f"Max Profit Test: {max_profit == 7}")  # Buy at 1, sell at 5; buy at 3, sell at 6
    
    # Test 3: Daily returns
    daily_returns = calculate_daily_returns(test_data).tolist()
    print(f"Daily Returns Test: {len(daily_returns) == len(test_data)}")
    
    print("Validation tests completed!")

# Test the functions immediately
if __name__ == "__main__":
    run_validation_tests()