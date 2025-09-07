#!/usr/bin/env python3
"""  
Simple and reliable test runner for PyStock Analyzer
"""

import unittest
import sys
import os

def run_tests():
    """Run all tests with proper path setup"""
    print("Running PyStock Analyzer Unit Tests...")
    print("=" * 50)

    # Add the current directory to Python path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, current_dir)

    try:
        # Import test modules - adjust these to match your actual test files
        from test.test_calculations import TestCalculations, TestEdgeCases
        from test.test_advanced_calculations import TestMaxProfit
        
        # Create test loader and suite
        loader = unittest.TestLoader()
        test_suite = unittest.TestSuite()
        
        # Add test classes
        test_suite.addTests(loader.loadTestsFromTestCase(TestCalculations))
        test_suite.addTests(loader.loadTestsFromTestCase(TestEdgeCases))
        test_suite.addTests(loader.loadTestsFromTestCase(TestMaxProfit))
        
        # Run tests
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(test_suite)
        
        return result.wasSuccessful()
        
    except ImportError as e:
        print(f"Import error: {e}")
        print("Make sure your test files exist and are named correctly.")
        return False

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)