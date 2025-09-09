PyStock Analyzer

A comprehensive Python application for professional stock market technical analysis. PyStock Analyzer calculates key financial metrics, identifies market trends, and provides advanced visualization for informed investment decisions.

🚀 Features
📊 Core Analysis Functions
Real-time Data Fetching: Yahoo Finance API integration

Simple Moving Average (SMA): Trend identification

Price Run Analysis: Consecutive upward/downward streaks

Daily Returns Calculation: Volatility measurement

Maximum Profit Algorithm: Best Time to Buy and Sell Stock II solution

📈 Advanced Technical Indicators
Relative Strength Index (RSI): Overbought/oversold detection

Bollinger Bands: Volatility and reversal points

Multi-timeframe Analysis: 1mo to 2y period selection

🎯 Dual Interface Support
Command-Line Interface (CLI): For technical users

Graphical User Interface (GUI): User-friendly Tkinter application

Interactive Charts: Matplotlib with professional styling

✅ Validation & Quality
Comprehensive Test Suite: 5+ validation test cases

Real-time Data Testing: Live market data integration

Error Handling: Robust exception management

📁 Project Structure
PyStockAnalyzer/

├── .venv/                     # Virtual environment

├── data/                      # Stock data storage

├── src/                       # Source code

│   ├── __pycache__/           # Python cache

│   ├── advanced_calculations.py # Max profit & validation

│   ├── calculations.py        # Core financial algorithms

│   ├── data_loader.py         # Yahoo Finance API integration

│   ├── gui.py                # Graphical user interface

│   ├── main.py               # Application entry point

│   ├── validation.py         # Comprehensive test suite

│   └── visualizer.py         # Data visualization

├── .gitignore                # Git ignore rules

├── README.md                 # Project documentation

└── requirements.txt          # Python dependencies

📄 File Descriptions
src/data_loader.py
Purpose: Data acquisition from Yahoo Finance
Key Function: fetch_stock_data(ticker, period)
Features: API integration, error handling, data cleaning

src/calculations.py
Purpose: Core financial algorithms
Key Functions:

calculate_sma() - Simple Moving Average

identify_runs() - Price trend analysis

calculate_daily_returns() - Return calculations

calculate_rsi() - Relative Strength Index

calculate_bollinger_bands() - Volatility bands

src/advanced_calculations.py
Purpose: Advanced algorithms
Key Functions:

calculate_max_profit() - Optimal trading strategy

run_validation_tests() - Comprehensive testing

src/visualizer.py
Purpose: Data visualization
Features:

Multi-panel professional charts

RSI and Bollinger Band visualization

Trend highlighting

Formatted result display

src/gui.py
Purpose: Graphical user interface
Features:

Tkinter-based interface

Real-time progress updates

Interactive chart embedding

Threaded operations

src/main.py
Purpose: Application controller
Features:

Dual interface mode (CLI/GUI)

User input handling

Module coordination

Data export functionality

src/validation.py
Purpose: Comprehensive testing
Features:

Unit tests for all functions

Integration testing

Validation against manual calculations
