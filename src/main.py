from data_loader import fetch_stock_data
from visualizer import plot_stock_data, display_analysis_results
from advanced_calculations import run_validation_tests


def cli_interface():
    """Command-line interface"""
    print("Welcome to PyStock Analyzer!")
    print("=" * 40)
    print("This tool helps you analyze stock data with various technical indicators.")
    
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

def gui_interface():
    """Graphical user interface"""
    try:
        from gui import main as gui_main
        gui_main()
    except ImportError as e:
        print(f"GUI not available: {e}")
        print("Falling back to CLI interface...")
        cli_interface()

def web_interface():
    """Web interface"""
    try:
        import sys
        import os
        sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'webapp'))
        from app import app
        print("Starting web server...")
        print("Open: http://localhost:5000")
        print("Press Ctrl+C to stop the server")
        app.run(debug=True, host='0.0.0.0', port=5000)
    except ImportError as e:
        print(f"Web interface not available: {e}")
        print("Make sure you have created the webapp directory and installed Flask")
        print("Run: pip install Flask")
        print("Falling back to GUI interface...")
        gui_interface()
    except KeyboardInterrupt:
        print("\nWeb server stopped. Returning to main menu...")
        main()

def show_menu():
    """Display the main menu"""
    print("\n" + "=" * 50)
    print("            PYSTOCK ANALYZER")
    print("=" * 50)
    print("1. Command Line Interface (CLI)")
    print("2. Graphical User Interface (GUI)") 
    print("3. Web Interface")
    print("4. Run Validation Tests Only")
    print("5. Exit")
    print("=" * 50)

def main():
    """Main function with mode selection"""
    
    while True:
        show_menu()
        
        choice = input("Enter your choice (1-5): ").strip()
        
        if choice == "1":
            cli_interface()
        elif choice == "2":
            gui_interface()
        elif choice == "3":
            web_interface()
        elif choice == "4":
            print("\nRunning validation tests...")
            run_validation_tests()
            input("\nPress Enter to continue...")
        elif choice == "5":
            print("Thank you for using PyStock Analyzer!")
            print("Goodbye! 👋")
            break
        else:
            print("Invalid choice. Please enter a number between 1-5.")
            input("Press Enter to continue...")

if __name__ == "__main__":
    main()