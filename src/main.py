from data_loader import fetch_stock_data
from visualizer import plot_stock_data, display_analysis_results
from advanced_calculations import run_validation_tests

def cli_interface():
    """Command-line interface"""
    print("Welcome to PyStock Analyzer!")
    print("=" * 40)
    
    # Run validation tests first
    print("Running validation tests...")
    run_validation_tests()
    print()
    
    # Get user input
    ticker = input("Enter stock ticker (e.g., AAPL, TSLA, MSFT): ").upper()
    period = input("Enter time period (1y, 2y, 6mo, etc.) [default: 1y]: ") or "1y"
    sma_window = int(input("Enter SMA window size [default: 5]: ") or "5")
    
    # Fetch data
    print(f"\nFetching data for {ticker}...")
    stock_data = fetch_stock_data(ticker, period)
    
    if stock_data is None:
        print("Failed to fetch data. Please check your ticker symbol and internet connection.")
        return
    
    # Display analysis results
    display_analysis_results(stock_data, sma_window)
    
    # Generate plot
    print("Generating visualization...")
    plot_stock_data(stock_data, sma_window)
    
    # Save data option
    save_csv = input("\nWould you like to save the data to CSV? (y/n): ").lower()
    if save_csv == 'y':
        filename = f"{ticker}_data.csv"
        stock_data.to_csv(filename)
        print(f"Data saved to {filename}")

def main():
    """Main function with mode selection"""
    print("PyStock Analyzer - Choose Interface Mode")
    print("1. Command Line Interface (CLI)")
    print("2. Graphical User Interface (GUI)")
    
    choice = input("Enter choice (1 or 2): ").strip()
    
    if choice == "1":
        cli_interface()
    elif choice == "2":
        try:
            from gui import main as gui_main
            gui_main()
        except ImportError as e:
            print(f"GUI not available: {e}")
            print("Falling back to CLI interface...")
            cli_interface()
    else:
        print("Invalid choice. Using CLI interface...")
        cli_interface()

if __name__ == "__main__":
    main()