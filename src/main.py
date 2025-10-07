from data_loader import fetch_stock_data
from visualizer import plot_stock_data, display_analysis_results
from advanced_calculations import run_validation_tests
import sys


def cli_interface():
    """Command-line interface"""
    print("Welcome to PyStock Analyzer!")
    print("=" * 40)
    print("This tool helps you analyze stock data with various technical indicators.")
    
    # Run validation tests first
    print("Running validation tests...")
    run_validation_tests()
    print()
    try:
        # Get user input
        ticker = input("Enter stock ticker (e.g., AAPL, TSLA, MSFT): ").upper()
        period = input("Enter time period (1y, 2y, 6mo, etc.) [default: 1y]: ") or "1y"
        sma_window = int(input("Enter SMA window size [default: 5]: ") or "5")
        
        # Fetch data
        print(f"\nFetching data for {ticker}...")
        stock_data = fetch_stock_data(ticker, period)
        
        if stock_data is None:
            print("Failed to fetch data. Please check your ticker symbol and internet connection.")
            input("\nPress Enter to return to the main menu...")
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
    except Exception as e:
        print(f"Error: {e}")
    input("\nPress Enter to return to the main menu...")
    return

def gui_interface():
    """Graphical user interface"""
    import subprocess
    import sys
    import os
    try:
        gui_path = os.path.join(os.path.dirname(__file__), 'gui.py')
        # Use the same Python executable
        subprocess.run([sys.executable, gui_path])
        print("\nGUI window closed. Returning to main menu...")
    except Exception as e:
        print(f"An error occurred while launching the GUI: {e}")
    # No extra input prompt here; return directly to menu
    return
    

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
        #set use_reloader=True for development, False for production
        app.run(debug=True, use_reloader=True, host='0.0.0.0', port=5000)
        print("\nWeb server stopped. Returning to main menu...")
    except ImportError as e:
        print(f"Web interface not available: {e}")
        print("Make sure you have created the webapp directory and installed Flask")
        print("Run: pip install Flask")
        print("Falling back to GUI interface...")
        gui_interface()
    except KeyboardInterrupt:
        print("\nWeb server stopped. Returning to main menu...")
    input("\nPress Enter to return to the main menu...")
    return

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
            continue
        elif choice == "2":
            gui_interface()
            continue
        elif choice == "3":
            web_interface()
            continue
        elif choice == "4":
            print("\nRunning validation tests...")
            run_validation_tests()
            input("\nPress Enter to continue...")
            continue
        elif choice == "5":
            print("Thank you for using PyStock Analyzer!")
            print("Goodbye! 👋")
            break
        else:
            print("Invalid choice. Please enter a number between 1-5.")
            input("Press Enter to continue...")
            continue

if __name__ == "__main__":
    main()