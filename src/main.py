from data_loader import fetch_stock_data
from visualizer import plot_stock_data, display_analysis_results, generate_risk_report
from advanced_calculations import run_validation_tests
from portfolio_analyzer import analyze_sample_portfolio
from calculations import calculate_daily_returns

def cli_interface():
    """Command-line interface for single stock analysis"""
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
    
    # Generate and display risk report
    returns = calculate_daily_returns(stock_data)
    risk_report = generate_risk_report(stock_data, returns)
    print("\n" + risk_report)
    
    # Generate plot
    print("Generating visualization...")
    plot_stock_data(stock_data, sma_window)
    
    # Save data option
    save_csv = input("\nWould you like to save the data to CSV? (y/n): ").lower()
    if save_csv == 'y':
        filename = f"{ticker}_data.csv"
        stock_data.to_csv(filename)
        print(f"Data saved to {filename}")

def analyze_portfolio_cli():
    """CLI interface for portfolio analysis"""
    print("\n" + "=" * 50)
    print("PORTFOLIO ANALYSIS")
    print("=" * 50)
    
    print("\nAnalyzing sample portfolio: 40% AAPL, 30% MSFT, 30% GOOGL")
    print("Loading data...")
    
    results = analyze_sample_portfolio()
    
    if "error" in results:
        print(f"Error: {results['error']}")
        return
    
    print("\nPORTFOLIO PERFORMANCE RESULTS:")
    print("-" * 40)
    print(f"Total Return: {results['total_return']*100:>8.2f}%")
    print(f"Annual Return: {results['annual_return']*100:>7.2f}%")
    print(f"Volatility: {results['volatility']*100:>10.2f}%")
    print(f"Sharpe Ratio: {results['sharpe_ratio']:>9.2f}")
    print(f"Max Drawdown: {results['max_drawdown']*100:>7.2f}%")
    
    print("\nSTOCK CONTRIBUTIONS:")
    print("-" * 40)
    for ticker, contrib in results['stock_contributions'].items():
        print(f"  {ticker}: {contrib:>6.1f}%")
    
    print("\n" + "=" * 50)
    print("Portfolio analysis completed!")
    print("=" * 50)

def start_gui():
    """Start the graphical user interface"""
    try:
        from gui import main as gui_main
        gui_main()
    except ImportError as e:
        print(f"GUI not available: {e}")
        print("Falling back to CLI interface...")
        cli_interface()
    except Exception as e:
        print(f"Error starting GUI: {e}")
        print("Falling back to CLI interface...")
        cli_interface()

def show_help():
    """Display help information"""
    print("\nPyStock Analyzer - Help")
    print("=" * 30)
    print("1. Single Stock Analysis - Analyze individual stocks with technical indicators")
    print("2. GUI Mode - Graphical interface with advanced features and portfolio analysis")
    print("3. Portfolio Analysis - Analyze a diversified portfolio of multiple stocks")
    print("4. Includes: SMA, RSI, Bollinger Bands, Risk Metrics, and more!")
    print("\nRequired data: Internet connection for stock data download")

def main():
    """Main function with mode selection"""
    print("╔══════════════════════════════════════╗")
    print("║          PYSTOCK ANALYZER            ║")
    print("║      Professional Edition v5.0       ║")
    print("╚══════════════════════════════════════╝")
    
    print("\nChoose Analysis Mode:")
    print("1. Single Stock Analysis (CLI)")
    print("2. Graphical User Interface (GUI)")
    print("3. Portfolio Analysis (CLI)")
    print("4. Help")
    print("5. Exit")
    
    while True:
        try:
            choice = input("\nEnter choice (1-5): ").strip()
            
            if choice == "1":
                cli_interface()
            elif choice == "2":
                start_gui()
            elif choice == "3":
                analyze_portfolio_cli()
            elif choice == "4":
                show_help()
            elif choice == "5":
                print("Thank you for using PyStock Analyzer!")
                break
            else:
                print("Invalid choice. Please enter 1-5.")
                
            # Ask if user wants to continue
            if choice != "5":
                continue_choice = input("\nWould you like to perform another analysis? (y/n): ").lower()
                if continue_choice != 'y':
                    print("Thank you for using PyStock Analyzer!")
                    break
                    
        except KeyboardInterrupt:
            print("\n\nOperation cancelled by user.")
            break
        except Exception as e:
            print(f"\nAn error occurred: {e}")
            print("Please try again or check your inputs.")

if __name__ == "__main__":
    main()