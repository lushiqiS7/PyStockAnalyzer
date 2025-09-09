import yfinance as yf
import pandas as pd

def fetch_stock_data(ticker, period="1y"):

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