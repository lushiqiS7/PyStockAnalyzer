PyStock Analyzer - Complete Project Summary

A comprehensive stock market analysis tool with multiple interfaces, providing professional technical analysis capabilities.

🚀 Project Overview
PyStock Analyzer is a full-featured Python application that performs advanced stock market technical analysis. It features three different user interfaces and implements all required functionalities from the INF1002 project specification.

📁 Complete Project Structure

PyStockAnalyzer/
├── .venv/                     # Python virtual environment
├── data/                      # Stock data storage directory
├── src/                       # Core analysis source code
│   ├── advanced_calculations.py # Advanced algorithms & validation
│   ├── calculations.py        # Core financial calculations
│   ├── data_loader.py         # Yahoo Finance API integration
│   ├── gui.py                # Tkinter graphical interface
│   ├── main.py               # Main application controller
│   ├── validation.py         # Comprehensive test suite
│   └── visualizer.py         # Data visualization module
├── webapp/                    # Flask web application
│   ├── static/
│   │   └── css/
│   │       └── style.css     # Web styles
│   ├── templates/            # HTML templates
│   │   ├── base.html         # Base template
│   │   ├── error.html        # Error page
│   │   ├── index.html        # Main form page
│   │   └── results.html      # Results display
│   └── app.py               # Flask application
├── .gitignore               # Git ignore rules
├── README.md               # Project documentation
└── requirements.txt        # Python dependencies
📊 Core Features Implemented
✅ Required Functionalities
Simple Moving Average (SMA) - Trend identification

Price Run Analysis - Consecutive upward/downward streaks

Daily Returns Calculation - Volatility measurement

Maximum Profit Algorithm - Best Time to Buy and Sell Stock II

Data Visualization - Charts with trends and indicators

Validation Testing - 5+ manual test cases

✅ Advanced Features
Relative Strength Index (RSI) - Overbought/oversold detection

Bollinger Bands - Volatility measurement

Multiple Timeframes - 1mo to 2y analysis periods

🎯 Three Interface Modes
1. Command Line Interface (CLI)
File: src/main.py (CLI functions)
Purpose: Traditional terminal-based interface for technical users
Features: Text-based interaction, validation tests, data export

2. Graphical User Interface (GUI)
File: src/gui.py
Purpose: Desktop application with Tkinter
Features: Point-and-click interface, embedded charts, real-time updates

3. Web Interface
File: webapp/app.py
Purpose: Modern web application with Flask
Features: Responsive design, browser accessibility, professional UI

📄 Detailed File Descriptions
Core Analysis Modules
src/data_loader.py
Purpose: Data acquisition and management
Key Function: fetch_stock_data(ticker, period)
Features: Yahoo Finance API integration, error handling, data cleaning

src/calculations.py
Purpose: Core financial algorithms
Key Functions:

calculate_sma() - Simple Moving Average

identify_runs() - Price trend analysis

calculate_daily_returns() - Return calculations

calculate_rsi() - Relative Strength Index

calculate_bollinger_bands() - Volatility bands

src/advanced_calculations.py
Purpose: Advanced algorithms and validation
Key Functions:

calculate_max_profit() - Optimal trading strategy

run_validation_tests() - Comprehensive testing suite

src/visualizer.py
Purpose: Data visualization and presentation
Features: Multi-panel charts, trend highlighting, formatted results

Interface Modules
src/main.py
Purpose: Application controller and CLI interface
Features: Mode selection, user input handling, module coordination

src/gui.py
Purpose: Graphical user interface
Features: Tkinter-based UI, real-time progress, threaded operations

webapp/app.py
Purpose: Flask web application
Features: RESTful API, template rendering, error handling

Web Application Files
webapp/templates/base.html
Purpose: Base template for all web pages
Features: Consistent layout, CSS/JS includes, navigation structure

webapp/templates/index.html
Purpose: Stock analysis form page
Features: User input form, popular stock examples, responsive design

webapp/templates/results.html
Purpose: Analysis results display
Features: Formatted results, color-coded indicators, action buttons

webapp/templates/error.html
Purpose: Error handling page
Features: User-friendly error messages, recovery options

webapp/static/css/style.css
Purpose: Web application styling
Features: Responsive design, professional colors, mobile compatibility

🛠 Installation & Setup
Prerequisites
Python 3.8+

pip package manager

Quick Setup
# Clone and setup
git clone https://github.com/lushiqi57/PyStockAnalyzer.git
cd PyStockAnalyzer

# Create virtual environment
python -m venv .venv

# Activate (Windows)
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
🎯 Usage Examples
Command Line Interface

python src/main.py
# Choose option 1
# Enter: AAPL, 1y, 10
Graphical Interface

python src/main.py
# Choose option 2
Web Interface

python src/main.py
# Choose option 3
# Open: http://localhost:5000
📊 Technical Architecture
Data Flow
Input → User selects stock and parameters

Data Fetching → Yahoo Finance API integration

Analysis → Multiple technical indicators calculated

Visualization → Charts and results generated

Output → Formatted display across all interfaces

Key Technologies
Pandas - Data manipulation and analysis

Matplotlib - Professional charting

yFinance - Real-time stock data

Tkinter - Desktop GUI framework

Flask - Web application framework

Jinja2 - HTML templating

👥 Team Members & Contributions
LUSHIQI (2501829) - GUI development, web interface(simple), visualization,Core algorithms, data processing, validation


✅ Academic Requirements Met
This project demonstrates mastery of:

Python programming fundamentals

Algorithm design and implementation

API integration and data processing

Multiple interface development (CLI, GUI, Web)

Software testing and validation

Team collaboration with Git

Financial analysis concepts

🚀 Future Enhancement Opportunities
Technical Improvements
Machine learning price predictions

Real-time data streaming

Portfolio analysis capabilities

Additional technical indicators (MACD, Stochastic)

Database integration

User Experience
Mobile application version

Advanced chart interactions

Automated report generation

Alert notifications

Social features

Deployment
Docker containerization

Cloud deployment (AWS, Azure)

CI/CD pipeline

Performance optimization

📝 License
This project is developed for educational purposes as part of the INF1002 Programming Fundamentals course at Singapore Institute of Technology.

🤝 Support
For technical support or questions:

Email: lushiqi2001@gmail.com