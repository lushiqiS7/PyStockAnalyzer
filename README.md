# PyStock Analyzer

A comprehensive Python application for stock market trend analysis that calculates key financial metrics, identifies market trends, and visualizes results.

## Features

- **Data Fetching**: Retrieve historical stock data from Yahoo Finance
- **Technical Analysis**: 
  - Simple Moving Average (SMA) calculation
  - Price run identification (upward/downward streaks)
  - Daily returns calculation
  - Maximum profit calculation (Best Time to Buy and Sell Stock II algorithm)
- **Data Visualization**: Plot closing prices with SMA and highlighted trends
- **Validation Suite**: Comprehensive testing of all functionalities
- **User-Friendly Interface**: Command-line interface for easy interaction

## Project Structure
PyStockAnalyzer/

├── data/ # Folder for storing downloaded stock data

├── src/ # Source code directory

│ ├── data_loader.py # Data fetching from Yahoo Finance

│ ├── calculations.py # Core financial calculations (SMA, runs, returns)

│ ├── advanced_calculations.py # Max profit algorithm & validation tests

│ ├── visualizer.py # Data visualization and result display

│ └── main.py # Main application entry point

├── test/ # Test directory

├── .gitignore # Git ignore rules

├── requirements.txt # Python dependencies

└── README.md # Project documentation

## File Descriptions

### src/data_loader.py
Fetches historical stock data from Yahoo Finance API. Handles data retrieval, error handling, and returns cleaned pandas DataFrames.

**Key Functions:**
- `fetch_stock_data(ticker, period)`: Downloads stock data for a given ticker and time period

### src/calculations.py
Contains core financial calculation algorithms for stock analysis.

**Key Functions:**
- `calculate_sma(df, window)`: Computes Simple Moving Average
- `identify_runs(df)`: Identifies consecutive upward/downward price movements
- `calculate_daily_returns(df)`: Calculates daily percentage returns

### src/advanced_calculations.py
Implements advanced algorithms and validation tests.

**Key Functions:**
- `calculate_max_profit(prices)`: Solves "Best Time to Buy and Sell Stock II" problem
- `run_validation_tests()`: Runs comprehensive validation of all calculations

### src/visualizer.py
Handles data visualization and result presentation.

**Key Functions:**
- `plot_stock_data(df, sma_window)`: Plots price data with SMA and trend highlights
- `display_analysis_results(df, sma_window)`: Displays formatted analysis results

### src/main.py
Main application entry point that integrates all modules.

**Features:**
- Command-line interface for user interaction
  
- Coordinates data fetching, analysis, and visualization
  
- Provides option to save results to CSV

### src/validation_suite.py
Comprehensive testing suite for all project functionalities.

**Features:**
- Tests all core calculations with both synthetic and real data
- Validates algorithm correctness against manual calculations
- Provides detailed output for debugging

## Installation

1. Clone the repository:
git clone https://github.com/lushiqi57/PyStockAnalyzer.git
cd PyStockAnalyzer

2. Create a virtual environment:
python -m venv .venv

3. Activate the virtual environment:
# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate

4. Install dependencies:
pip install -r requirements.txt

Run the main application:

python src/main.py
Run the validation suite:

python src/validation_suite.py
Run individual modules:

python src/data_loader.py
python src/calculations.py

# etc.
Dependencies
pandas - Data manipulation and analysis
matplotlib - Data visualization
yfinance - Yahoo Finance API access
numpy - Numerical operations

Project Requirements Met
This project implements all requirements from the INF1002 Python Project specification:

✅ Simple Moving Average (SMA) calculation

✅ Upward and downward run identification

✅ Daily returns calculation

✅ Maximum profit calculation (Best Time to Buy and Sell Stock II)

✅ Visualization of price data with SMA and highlighted trends

✅ Validation with manual calculations (5+ test cases)

✅ Modular code design with clear separation of concerns

✅ Comprehensive documentation

✅ Team collaboration via GitHub

Contributors

LUSHIQI (2501829)

[Add your name and ID]

License

This project is created for educational purposes as part of the INF1002 Programming Fundamentals course.



