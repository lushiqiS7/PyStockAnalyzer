"""
Main application entry point for the PyStock Analyzer.

This module provides the primary user interface for accessing all functionality
of the PyStock Analyzer system. It offers multiple interface options including
command-line, graphical, and web-based interfaces to accommodate different
user preferences and use cases.

Features:
- Interactive main menu system
- Command-line interface for quick analysis
- Graphical user interface for visual interaction
- Web interface for browser-based access
- Comprehensive validation testing
- Error handling and user guidance

Interface Options:
1. CLI: Terminal-based interface for quick stock analysis
2. GUI: Desktop application with charts and interactive features
3. Web: Browser-based interface accessible from any device
4. Validation: Comprehensive system testing and verification
"""

import sys
import os

# Import core analysis modules
from data_loader import fetch_stock_data
from visualizer import plot_stock_data, display_analysis_results
from advanced_calculations import run_validation_tests


def cli_interface():
    """
    Command-line interface for stock analysis.
    
    This function provides a text-based interface for users who prefer
    terminal interaction. It guides users through the analysis process,
    validates inputs, fetches data, performs calculations, and displays
    results. Includes options for data export and visualization.
    
    Features:
        - Interactive parameter input with defaults
        - Input validation and error handling
        - Comprehensive analysis results display
        - Data visualization generation
        - CSV export functionality
        - Graceful error recovery
    """
    print("Welcome to PyStock Analyzer CLI!")
    print("=" * 40)
    print("This tool helps you analyze stock data with various technical indicators.")
    print("Including: SMA, RSI, Bollinger Bands, run analysis, and more!")
    
    # Run validation tests first to ensure system integrity
    print("\nRunning system validation tests...")
    run_validation_tests()
    print()
    
    try:
        # =============== USER INPUT COLLECTION ===============
        # Get stock ticker with validation
        ticker = input("Enter stock ticker (e.g., AAPL, TSLA, MSFT): ").strip().upper()
        if not ticker:
            print("❌ Error: Ticker symbol cannot be empty.")
            input("\nPress Enter to return to the main menu...")
            return
            
        # Get time period with default
        period = input("Enter time period (1mo, 3mo, 6mo, 1y, 2y) [default: 1y]: ").strip() or "1y"
        
        # Get SMA window with validation
        try:
            sma_window = int(input("Enter SMA window size [default: 5]: ").strip() or "5")
            if sma_window < 1:
                print("❌ SMA window must be positive. Using default value of 5.")
                sma_window = 5
        except ValueError:
            print("❌ Invalid input. Using default SMA window of 5.")
            sma_window = 5
        
        # =============== DATA FETCHING ===============
        print(f"\n📊 Fetching data for {ticker} over {period} period...")
        stock_data = fetch_stock_data(ticker, period)
        
        if stock_data is None or stock_data.empty:
            print("❌ Failed to fetch data. Please check:")
            print("   - Ticker symbol is correct")
            print("   - Internet connection is available")
            print("   - Yahoo Finance service is accessible")
            input("\nPress Enter to return to the main menu...")
            return
        
        # =============== ANALYSIS AND DISPLAY ===============
        print("\n📈 Performing comprehensive analysis...")
        display_analysis_results(stock_data, sma_window)
        
        # =============== VISUALIZATION ===============
        print("\n📊 Generating interactive charts...")
        plot_stock_data(stock_data, sma_window)
        
        # =============== DATA EXPORT OPTION ===============
        save_csv = input("\n💾 Would you like to save the data to CSV? (y/n): ").lower().strip()
        if save_csv in ['y', 'yes']:
            filename = f"{ticker}_{period}_data.csv"
            stock_data.to_csv(filename)
            print(f"✅ Data saved to {filename}")
            
    except KeyboardInterrupt:
        print("\n\n⚠️  Operation cancelled by user.")
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        print("Please try again or contact support if the problem persists.")
    
    input("\nPress Enter to return to the main menu...")
    return

def gui_interface():
    """
    Launch the graphical user interface.
    
    This function starts the GUI application in a separate process to provide
    a rich visual interface for stock analysis. The GUI includes interactive
    charts, technical indicators, and comprehensive analysis displays.
    
    Features:
        - Interactive matplotlib charts with hover tooltips
        - Real-time analysis parameter adjustment
        - Technical indicator overlays
        - Run period highlighting
        - Export capabilities
        - Professional chart styling
        
    Note:
        The GUI runs in a separate process to prevent conflicts with the
        main menu system and ensure proper resource management.
    """
    import subprocess
    
    try:
        print("🚀 Launching Graphical User Interface...")
        print("   The GUI window will open shortly.")
        print("   Close the GUI window to return to this menu.")
        
        # Construct path to GUI module
        gui_path = os.path.join(os.path.dirname(__file__), 'gui.py')
        
        # Launch GUI using the same Python executable to ensure compatibility
        result = subprocess.run([sys.executable, gui_path], 
                              capture_output=False, text=True)
        
        print("\n🔙 GUI window closed. Returning to main menu...")
        
    except FileNotFoundError:
        print("❌ GUI module not found. Please ensure gui.py exists in the src directory.")
    except Exception as e:
        print(f"❌ An error occurred while launching the GUI: {e}")
        print("Please check the error details and try again.")
    
    # Return directly to menu without additional input prompt
    return
    

def web_interface():
    """
    Launch the web-based interface.
    
    This function starts a Flask web server that provides a browser-based
    interface for stock analysis. The web interface is accessible from any
    device with a web browser and provides the same analytical capabilities
    as the desktop interfaces.
    
    Features:
        - Browser-based accessibility
        - Responsive web design
        - Interactive charts and visualizations
        - Multi-device compatibility
        - Network accessibility
        - Modern web UI/UX
        
    Server Configuration:
        - Host: 0.0.0.0 (accessible from network)
        - Port: 5000
        - Debug mode: Enabled for development
        - Auto-reload: Disabled to prevent conflicts
        
    Note:
        The server will run until manually stopped with Ctrl+C.
        Access the interface at http://localhost:5000 or your machine's IP address.
    """
    try:
        print("🌐 Starting Web Interface...")
        print("   Initializing Flask web server...")
        
        # Add webapp directory to Python path for imports
        webapp_path = os.path.join(os.path.dirname(__file__), '..', 'webapp')
        sys.path.append(webapp_path)
        
        # Import and start the Flask application
        from app import app # type: ignore
        
        print("✅ Web server starting successfully!")
        print("📱 Access Options:")
        print("   - Local:   http://localhost:5000")
        print("   - Network: http://[your-ip]:5000")
        print("\n⚡ Server Controls:")
        print("   - Press Ctrl+C to stop the server")
        print("   - Close your browser tab to continue using it")
        print("\n🚀 Opening web interface...")
        
        # Start the Flask development server
        # use_reloader=False prevents conflicts with the main menu system
        app.run(debug=True, use_reloader=False, host='0.0.0.0', port=5000)
        
    except ImportError as e:
        print(f"❌ Web interface not available: {e}")
        print("\n🔧 Setup Requirements:")
        print("   1. Ensure webapp directory exists")
        print("   2. Install Flask: pip install Flask")
        print("   3. Check app.py exists in webapp directory")
        print("\n🔄 Falling back to GUI interface...")
        gui_interface()
    except KeyboardInterrupt:
        print("\n\n⚠️  Web server stopped by user (Ctrl+C).")
    except Exception as e:
        print(f"\n❌ Web server error: {e}")
        print("Please check the error details and try again.")
    
    print("🔙 Returning to main menu...")
    input("Press Enter to continue...")
    return

def show_menu():
    """
    Display the main application menu.
    
    This function presents a user-friendly menu interface that allows users
    to choose between different analysis interfaces and system functions.
    The menu provides clear descriptions and visual formatting for better
    user experience.
    """
    print("\n" + "=" * 50)
    print("            PYSTOCK ANALYZER")
    print("         Advanced Stock Analysis Tool")
    print("=" * 50)
    print("📊 Choose Your Interface:")
    print()
    print("1. 💻 Command Line Interface (CLI)")
    print("   └── Text-based analysis with detailed results")
    print()
    print("2. 🖥️  Graphical User Interface (GUI)") 
    print("   └── Interactive charts and visual analysis")
    print()
    print("3. 🌐 Web Interface")
    print("   └── Browser-based access from any device")
    print()
    print("4. 🔍 Run Validation Tests Only")
    print("   └── System integrity and function verification")
    print()
    print("5. 🚪 Exit")
    print("   └── Close the application")
    print("=" * 50)


def main():
    """
    Main application controller and menu system.
    
    This function implements the primary application loop, handling user
    menu selection and routing to appropriate interface functions. It
    provides a persistent menu system that allows users to switch between
    different interfaces without restarting the application.
    
    Menu Options:
        1. CLI: Command-line interface for terminal users
        2. GUI: Graphical interface with interactive charts
        3. Web: Browser-based interface for network access
        4. Validation: System testing and verification
        5. Exit: Clean application shutdown
        
    Features:
        - Persistent menu loop until user exits
        - Input validation and error handling
        - Clear user feedback and guidance
        - Graceful error recovery
        - Professional user experience
    """
    print("🎉 Welcome to PyStock Analyzer!")
    print("Your comprehensive tool for stock market analysis.")
    
    while True:
        try:
            show_menu()
            choice = input("Enter your choice (1-5): ").strip()
            
            if choice == "1":
                print("\n🔤 Launching Command Line Interface...")
                cli_interface()
                continue
                
            elif choice == "2":
                print("\n🖥️  Launching Graphical User Interface...")
                gui_interface()
                continue
                
            elif choice == "3":
                print("\n🌐 Launching Web Interface...")
                web_interface()
                continue
                
            elif choice == "4":
                print("\n🔍 Running comprehensive validation tests...")
                run_validation_tests()
                input("\n✅ Validation complete. Press Enter to continue...")
                continue
                
            elif choice == "5":
                print("\n👋 Thank you for using PyStock Analyzer!")
                print("🎯 Happy investing and may your trades be profitable!")
                print("Goodbye! �")
                break
                
            else:
                print("\n❌ Invalid choice. Please enter a number between 1-5.")
                input("Press Enter to try again...")
                continue
                
        except KeyboardInterrupt:
            print("\n\n⚠️  Application interrupted by user (Ctrl+C).")
            print("👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}")
            print("🔄 Returning to main menu...")
            input("Press Enter to continue...")
            continue


# Entry point for direct script execution
if __name__ == "__main__":
    """
    Entry point for direct script execution.
    
    When this module is run directly (e.g., python main.py), it starts
    the main application with the interactive menu system.
    """
    main()