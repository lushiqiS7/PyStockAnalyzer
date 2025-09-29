"""
Data loading module for stock analysis.

This module provides functionality to fetch and load stock market data
from various sources, primarily using the Yahoo Finance API through
the yfinance library. It handles data retrieval, basic validation,
and error handling for robust data operations.
"""

import yfinance as yf
import pandas as pd


def fetch_stock_data(ticker, period="1y"):
    """
    Fetch historical stock data for a given ticker symbol.
    
    This function retrieves historical stock market data using the Yahoo Finance
    API through the yfinance library. It provides comprehensive historical data
    including open, high, low, close prices, volume, and other trading metrics.
    
    Args:
        ticker (str): Stock ticker symbol (e.g., 'AAPL', 'MSFT', 'GOOGL').
                     Case insensitive.
        period (str, optional): Time period for historical data. Defaults to "1y".
                               Valid periods include:
                               - "1d", "5d": Short-term intraday
                               - "1mo", "3mo", "6mo": Medium-term 
                               - "1y", "2y", "5y", "10y": Long-term
                               - "ytd": Year to date
                               - "max": Maximum available data
    
    Returns:
        pandas.DataFrame or None: DataFrame containing historical stock data with columns:
                                 - Open: Opening price
                                 - High: Highest price of the day
                                 - Low: Lowest price of the day  
                                 - Close: Closing price
                                 - Volume: Number of shares traded
                                 - Dividends: Dividend payments (if any)
                                 - Stock Splits: Stock split information (if any)
                                 Returns None if data fetching fails.
                                 
    Raises:
        Prints error message to console if data fetching fails, but does not
        raise exceptions to allow graceful error handling by calling code.
        
    Example:
        >>> data = fetch_stock_data("AAPL", "6mo")
        >>> if data is not None:
        ...     print(f"Retrieved {len(data)} days of data")
        ...     print(f"Price range: ${data['Low'].min():.2f} - ${data['High'].max():.2f}")
    """
    try:
        # Download the data using yfinance
        stock = yf.Ticker(ticker)
        df = stock.history(period=period)
        
        # Validate that we received data
        if df.empty:
            print(f"No data returned for ticker {ticker} with period {period}")
            return None
            
        # Print a success message and show the first few rows for verification
        print(f"Successfully fetched data for {ticker}")
        print(f"Data range: {df.index[0].date()} to {df.index[-1].date()}")
        print(f"Total records: {len(df)}")
        print("\nFirst few rows:")
        print(df.head())
        
        return df
        
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        print("Please check:")
        print("- Ticker symbol is correct")
        print("- Internet connection is available") 
        print("- Yahoo Finance service is accessible")
        return None


# Entry point for direct script execution
if __name__ == "__main__":
    """
    Entry point for direct script execution.
    
    When this module is run directly, it performs a test fetch of Apple (AAPL)
    stock data to verify that the data loading functionality is working correctly.
    """
    print("Testing data loading functionality...")
    
    # Test with a popular ticker (Apple)
    test_ticker = "AAPL"
    test_period = "1mo"  # Use shorter period for faster testing
    
    print(f"Fetching {test_period} of data for {test_ticker}...")
    data = fetch_stock_data(test_ticker, test_period)
    
    if data is not None:
        print(f"\n✓ Data fetching test passed!")
        print(f"✓ Successfully retrieved {len(data)} trading days")
        print(f"✓ Data columns: {list(data.columns)}")
    else:
        print("\n✗ Data fetching test failed.")
        print("✗ Please check your internet connection and try again.")