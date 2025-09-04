import yfinance as yf
import pandas as pd

def fetch_stock_data(ticker, period="1y"):
    """
    Fetches historical stock data from Yahoo Finance.
    
    Args:
        ticker (str): The stock ticker symbol (e.g., 'AAPL', 'TSLA').
        period (str): The time period to download. Valid periods: 
                      “1d”, “5d”, “1mo”, “3mo”, “6mo”, “1y”, “2y”, “5y”, “10y”, “ytd”, “max”
    
    Returns:
        pandas.DataFrame: A DataFrame with the stock data.
    """
    try:
        # Download the data
        stock = yf.Ticker(ticker)
        df = stock.history(period=period)
        
        # Print a success message and show the first few rows
        print(f"Successfully fetched data for {ticker}")
        print(df.head())
        return df
        
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return None

# Test the function immediately
if __name__ == "__main__":
    # Test with a popular ticker
    data = fetch_stock_data("AAPL")
    if data is not None:
        print("Data fetching test passed!")
    else:
        print("Data fetching test failed.")