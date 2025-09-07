import unittest
import sys
import os

# Add the parent directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

# Now import from src
from src.advanced_calculations import calculate_max_profit
from advanced_calculations import calculate_max_profit

class TestMaxProfit(unittest.TestCase):
    
    def test_max_profit_example_1(self):
        """Test with example from requirements"""
        prices = [7, 1, 5, 3, 6, 4]
        profit = calculate_max_profit(prices)
        self.assertEqual(profit, 7)
    
    def test_max_profit_example_2(self):
        """Test with increasing prices"""
        prices = [1, 2, 3, 4, 5]
        profit = calculate_max_profit(prices)
        self.assertEqual(profit, 4)
    
    def test_max_profit_example_3(self):
        """Test with decreasing prices"""
        prices = [7, 6, 4, 3, 1]
        profit = calculate_max_profit(prices)
        self.assertEqual(profit, 0)
    
    def test_max_profit_empty(self):
        """Test with empty list"""
        prices = []
        profit = calculate_max_profit(prices)
        self.assertEqual(profit, 0)
    
    def test_max_profit_single(self):
        """Test with single price"""
        prices = [100]
        profit = calculate_max_profit(prices)
        self.assertEqual(profit, 0)

if __name__ == '__main__':
    unittest.main()