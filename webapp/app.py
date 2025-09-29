
"""
Flask Web Application for PyStock Analyzer.

This module provides a comprehensive web-based interface for stock market analysis
using Flask. It offers browser-based access to all PyStock Analyzer functionality
including single stock analysis, multi-stock comparison, and interactive charting.

Features:
- RESTful API endpoints for real-time data
- Interactive web forms for analysis parameters
- Responsive HTML templates with Bootstrap styling
- Multi-stock comparison capabilities
- Data export functionality (CSV)
- Real-time chart visualization with Chart.js
- Error handling and user feedback
- Mobile-responsive design

Routes:
- / : Main analysis interface
- /analyze : Single stock analysis
- /analyze_or_compare : Multi-stock analysis and comparison
- /api/stock_data : JSON API for real-time data
- /export : CSV data export
- /refresh : Data refresh and re-analysis

Dependencies:
- Flask: Web framework
- pandas: Data manipulation
- Custom PyStock Analyzer modules for calculations
"""

from flask import Flask, render_template, request, jsonify, Response
import sys
import os
from datetime import datetime
import pandas as pd

# Add src directory to Python path for module imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

# Import analysis modules with error handling
try:
    from data_loader import fetch_stock_data
    from calculations import (calculate_sma, identify_runs, calculate_daily_returns, 
                             calculate_rsi, calculate_bollinger_bands, identify_run_periods)
    from advanced_calculations import calculate_max_profit
    from compare_logic import do_compare_logic, choose_best_stock, score_stock
    ANALYSIS_AVAILABLE = True
    print("✅ All analysis modules loaded successfully.")
except ImportError as e:
    print(f"❌ Analysis modules not available: {e}")
    print("   Web interface will run in limited mode.")
    ANALYSIS_AVAILABLE = False

# Initialize Flask application
app = Flask(__name__)

@app.route('/')
def index():
    """
    Main application page with stock analysis interface.
    
    This route serves the primary user interface where users can input
    stock tickers, select analysis parameters, and choose between single
    stock analysis or multi-stock comparison modes.
    
    Returns:
        Rendered HTML template with analysis form and interface controls.
    """
    return render_template('index.html', analysis_available=ANALYSIS_AVAILABLE)


@app.route('/api/stock_data')
def api_stock_data():
    """
    RESTful API endpoint for real-time stock data retrieval.
    
    This endpoint provides JSON-formatted stock data including prices,
    technical indicators, and volume information. It's designed for
    AJAX calls and real-time chart updates.
    
    Query Parameters:
        ticker (str): Stock ticker symbol (default: 'AAPL')
        period (str): Time period for data (default: '6mo')
        sma_window (int): SMA calculation window (default: 10)
    
    Returns:
        JSON response containing:
        - dates: Array of date strings
        - prices: Array of closing prices
        - sma: Array of SMA values
        - rsi: Array of RSI values  
        - volume: Array of volume data
        - current_price: Latest closing price
        
    Example:
        GET /api/stock_data?ticker=AAPL&period=6mo&sma_window=20
    """
    if not ANALYSIS_AVAILABLE:
        return jsonify({'error': 'Analysis modules not available'}), 503
        
    # Extract query parameters with defaults
    ticker = request.args.get('ticker', 'AAPL').upper()
    period = request.args.get('period', '6mo')
    sma_window = int(request.args.get('sma_window', '10'))
    
    try:
        # Fetch stock data
        stock_data = fetch_stock_data(ticker, period)
        if stock_data is None or stock_data.empty:
            return jsonify({'error': 'No data available for the specified ticker'}), 400
        
        # Calculate technical indicators
        sma = calculate_sma(stock_data, sma_window)
        rsi = calculate_rsi(stock_data, 14)
        
        # Prepare chart-ready data structure
        chart_data = {
            'dates': [d.strftime('%Y-%m-%d') for d in stock_data.index],
            'prices': stock_data['Close'].round(2).tolist(),
            'sma': sma.round(2).where(pd.notnull(sma), None).tolist(),
            'rsi': rsi.round(2).where(pd.notnull(rsi), None).tolist(),
            'volume': stock_data['Volume'].astype(int).tolist(),
            'current_price': round(stock_data['Close'].iloc[-1], 2)
        }
        
        return jsonify(chart_data)
        
    except Exception as e:
        return jsonify({'error': f'Data processing error: {str(e)}'}), 500

@app.route('/analyze_or_compare', methods=['POST'])
def analyze_or_compare():
    """
    Unified route for both single stock analysis and multi-stock comparison.
    
    This route determines the analysis mode based on form data and routes
    to appropriate analysis functions. It supports both single stock
    analysis and comprehensive multi-stock comparison with ranking.
    
    Form Parameters:
        mode (str): 'single' or 'compare' analysis mode
        tickers (str): Comma-separated list of stock ticker symbols
        period (str): Time period for analysis
        sma_window (int): Simple Moving Average window size
        
    Returns:
        Rendered template with analysis results or comparison data.
        
    Modes:
        - compare: Multi-stock analysis with ranking and scoring
        - single: Individual stock analysis (fallback for any other mode)
    """
    if not ANALYSIS_AVAILABLE:
        return render_template('error.html', 
                             error="Analysis modules not available. Please check your installation.")
    
    try:
        # Extract form parameters
        mode = request.form.get('mode', 'single')
        tickers_raw = request.form.get('tickers', '').strip()
        
        if not tickers_raw:
            return render_template('error.html', error="No ticker symbols provided.")
        
        # Parse ticker list
        tickers = [t.strip().upper() for t in tickers_raw.split(',') if t.strip()]
        period = request.form.get('period', '6mo')
        sma_window = int(request.form.get('sma_window', '10'))

        # Route based on mode and ticker count
        if mode == 'compare' and len(tickers) > 1:
            # =============== MULTI-STOCK COMPARISON MODE ===============
            print(f"🔍 Performing comparison analysis for: {', '.join(tickers)}")
            
            # Execute comprehensive comparison analysis
            all_results, all_charts = do_compare_logic(tickers, period, sma_window)
            
            if not all_results:
                return render_template('error.html', 
                                     error="No valid data found for any of the provided tickers.")
            
            # Determine best investment recommendation
            best_stock = choose_best_stock(all_results)
            analysis_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            return render_template(
                'compare_results.html',
                all_results=all_results,
                all_charts=all_charts,
                analysis_date=analysis_date,
                recommendation_reason="Highest overall score based on return, risk, and technical indicators",
                best_score=best_stock["score"] if best_stock else None,
                recommended_ticker=best_stock["ticker"] if best_stock else None
            )
        else:
            # =============== SINGLE STOCK ANALYSIS MODE ===============
            # Fallback to single stock analysis or when only one ticker provided
            return analyze_stock()
    
    except Exception as e:
        return render_template('error.html', 
                             error=f"Analysis routing error: {str(e)}")


@app.route('/analyze', methods=['POST'])
def analyze_stock():
    """
    Comprehensive single stock analysis endpoint.
    
    This function performs detailed analysis of a single stock including
    all technical indicators, performance metrics, trend analysis, and
    risk assessment. Results are formatted for web display with
    interactive charts and detailed insights.
    
    Form Parameters:
        tickers (str): Single ticker symbol or first from comma-separated list
        period (str): Analysis time period
        sma_window (int): Simple Moving Average window
        
    Returns:
        Rendered results template with comprehensive analysis data and charts.
        
    Analysis Includes:
        - Price performance and percentage changes
        - Technical indicators (SMA, RSI, Bollinger Bands)
        - Trend run analysis with highlighting
        - Volatility and risk metrics
        - Maximum profit calculations
        - Interactive chart data preparation
    """
    if not ANALYSIS_AVAILABLE:
        return render_template('error.html', 
                             error="Analysis modules not available. Please check your installation.")
    
    try:
        # =============== INPUT PROCESSING ===============
        tickers_input = request.form.get('tickers', '').strip()
        if not tickers_input:
            return render_template('error.html', error="No ticker symbol provided.")
        
        # Extract first ticker for single analysis
        tickers = [t.strip().upper() for t in tickers_input.split(',') if t.strip()]
        ticker = tickers[0]  # Use first ticker for single analysis
        
        period = request.form.get('period', '6mo')
        sma_window = int(request.form.get('sma_window', '10'))

        print(f"📊 Analyzing {ticker} over {period} period with SMA({sma_window})")

        # =============== DATA FETCHING ===============
        stock_data = fetch_stock_data(ticker, period)
        if stock_data is None or stock_data.empty:
            return render_template('error.html', 
                                 error=f"No data available for ticker {ticker}. Please verify the symbol is correct.")
        
        # =============== TECHNICAL CALCULATIONS ===============
        # Core technical indicators
        sma = calculate_sma(stock_data, sma_window)
        runs_data = identify_runs(stock_data)
        returns = calculate_daily_returns(stock_data)
        max_profit = calculate_max_profit(stock_data['Close'].tolist())
        rsi = calculate_rsi(stock_data, 14)
        upper_band, middle_band, lower_band = calculate_bollinger_bands(stock_data, 20, 2)
        
        # =============== RESULTS COMPILATION ===============
        # Compile comprehensive analysis results
        results = {
            'ticker': ticker,
            'period': period,
            'sma_window': sma_window,
            'sma_current': round(sma.iloc[-1], 2) if not pd.isna(sma.iloc[-1]) else 'N/A',
            'up_days': runs_data['total_up_days'],
            'down_days': runs_data['total_down_days'],
            'longest_up_streak': runs_data['longest_up_streak'],
            'longest_down_streak': runs_data['longest_down_streak'],
            'avg_return': round(returns.mean(), 4),
            'volatility': round(returns.std(), 4),
            'max_profit': round(max_profit, 2),
            'rsi_current': round(rsi.iloc[-1], 2) if not pd.isna(rsi.iloc[-1]) else 'N/A',
            'rsi_min': round(rsi.min(), 2) if not pd.isna(rsi.min()) else 'N/A',
            'rsi_max': round(rsi.max(), 2) if not pd.isna(rsi.max()) else 'N/A',
            'current_price': round(stock_data['Close'].iloc[-1], 2),
            'start_price': round(stock_data['Close'].iloc[0], 2),
            'total_change': round(((stock_data['Close'].iloc[-1] / stock_data['Close'].iloc[0]) - 1) * 100, 2),
            'analysis_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'data_points': len(stock_data)
        }
        
        # =============== RSI INTERPRETATION ===============
        if results['rsi_current'] != 'N/A':
            if results['rsi_current'] > 70:
                results['rsi_status'] = 'Overbought'
            elif results['rsi_current'] < 30:
                results['rsi_status'] = 'Oversold'
            else:
                results['rsi_status'] = 'Neutral'
        else:
            results['rsi_status'] = 'N/A'
        
        # =============== TREND RUN ANALYSIS ===============
        # Get run periods for chart highlighting
        run_periods = identify_run_periods(stock_data)
        
        # Format run periods for visualization (only significant runs)
        run_highlights = []
        for run in run_periods:
            if run['length'] >= 2:  # Only highlight runs of 2+ days to reduce clutter
                run_highlights.append({
                    'start': run['start_date'].strftime('%Y-%m-%d'),
                    'end': run['end_date'].strftime('%Y-%m-%d'),
                    'direction': 'up' if run['direction'] == 1 else 'down',
                    'length': run['length']
                })
        
        # =============== CHART DATA PREPARATION ===============
        # Prepare comprehensive chart data for visualization
        chart_data = {
            'dates': [d.strftime('%Y-%m-%d') for d in stock_data.index],
            'prices': stock_data['Close'].round(2).tolist(),
            'sma': sma.round(2).where(pd.notnull(sma), None).tolist(),
            'rsi': rsi.round(2).where(pd.notnull(rsi), None).tolist(),
            'volume': stock_data['Volume'].astype(int).tolist(),
            'runs': run_highlights
        }

        # =============== TEMPLATE RENDERING ===============
        return render_template("results.html", results=results, chart_data=chart_data)

    except Exception as e:
        return render_template('error.html', 
                             error=f"Analysis error: {str(e)}")
    


@app.route('/export')
def export_results():
    """
    Export stock analysis data as downloadable CSV file.
    
    This endpoint generates a CSV file containing comprehensive stock data
    including historical prices, volumes, and calculated technical indicators.
    The file is returned as a downloadable attachment with appropriate headers.
    
    Query Parameters:
        ticker (str): Stock ticker symbol (default: 'AAPL')
        period (str): Analysis time period (default: '6mo')
        sma_window (int): Simple Moving Average window (default: '10')
        
    Returns:
        Response: CSV file download with content-disposition headers
        - Includes: Date, Open, High, Low, Close, Volume, SMA
        - Format: CSV with proper headers and date index
        - Filename: {ticker}_analysis.csv
        
    Error Responses:
        503: Analysis modules not available
        400: No data available for the specified ticker
        500: Processing error with details
    """
    if not ANALYSIS_AVAILABLE:
        return "Export not available", 503

    try:
        # =============== PARAMETER EXTRACTION ===============
        ticker = request.args.get('ticker', 'AAPL').upper()
        period = request.args.get('period', '6mo')
        sma_window = int(request.args.get('sma_window', '10'))

        print(f"📄 Exporting data for {ticker} ({period}) with SMA({sma_window})")

        # =============== DATA FETCHING ===============
        stock_data = fetch_stock_data(ticker, period)
        if stock_data is None or stock_data.empty:
            return "No data available for export", 400

        # =============== TECHNICAL INDICATOR ADDITION ===============
        # Add Simple Moving Average to export data
        stock_data['SMA'] = calculate_sma(stock_data, sma_window)

        # =============== CSV GENERATION ===============
        # Convert DataFrame to CSV format with date index
        csv_data = stock_data.to_csv(index=True)

        # =============== FILE RESPONSE ===============
        return Response(
            csv_data,
            mimetype='text/csv',
            headers={
                "Content-Disposition": f"attachment;filename={ticker}_analysis.csv"
            }
        )
    except Exception as e:
        return f"Export error: {str(e)}", 500

@app.errorhandler(404)
def not_found(error):
    """
    Handle 404 Not Found errors with user-friendly error page.
    
    This error handler catches all 404 errors throughout the application
    and returns a consistent error page instead of Flask's default 404 page.
    
    Args:
        error: The 404 error object from Flask
        
    Returns:
        tuple: (rendered error template, 404 status code)
    """
    return render_template('error.html', error="Page not found"), 404


@app.errorhandler(500)
def internal_error(error):
    """
    Handle 500 Internal Server errors with user-friendly error page.
    
    This error handler catches all unhandled server errors and returns
    a consistent error page with appropriate messaging for users.
    
    Args:
        error: The 500 error object from Flask
        
    Returns:
        tuple: (rendered error template, 500 status code)
    """
    return render_template('error.html', error="Internal server error"), 500

@app.route('/refresh', methods=['POST'])
def refresh_data():
    """
    Refresh stock data and re-analyze with updated information.
    
    This endpoint allows users to refresh their analysis with the latest
    stock data without manually re-entering all parameters. It preserves
    the current analysis settings and fetches fresh data from the API.
    
    Form Parameters:
        tickers (str): Ticker symbol(s) to refresh
        period (str): Time period for analysis
        sma_window (int): Simple Moving Average window size
        
    Returns:
        Rendered results template with refreshed analysis data
        
    Note:
        This function reuses the analyze_stock() logic to maintain
        consistency in analysis processing and output formatting.
    """
    if not ANALYSIS_AVAILABLE:
        return render_template('error.html', 
                             error="Analysis modules not available. Please check your installation.")
    
    try:
        # =============== PARAMETER EXTRACTION ===============
        tickers_input = request.form.get('tickers')
        period = request.form.get('period', '6mo')
        sma_window = int(request.form.get('sma_window', '10'))
        
        print(f"🔄 Refreshing analysis for {tickers_input} ({period})")
        
        # =============== FORM RECONSTRUCTION ===============
        # Reconstruct form data to reuse analyze_stock logic
        # This ensures consistent processing and error handling
        request.form = request.form.copy()
        request.form['tickers'] = tickers_input
        request.form['period'] = period
        request.form['sma_window'] = sma_window
        
        # =============== ANALYSIS DELEGATION ===============
        return analyze_stock()
        
    except Exception as e:
        return render_template('error.html', 
                             error=f"Refresh error: {str(e)}")

if __name__ == '__main__':
    """
    Flask application entry point for development server.
    
    This section runs when the script is executed directly (not imported).
    It starts the Flask development server with appropriate configuration
    for local development and testing.
    
    Server Configuration:
        - Debug Mode: Enabled for development (auto-reload on changes)
        - Host: 0.0.0.0 (accessible from network, not just localhost)
        - Port: 5000 (standard Flask development port)
        - URL: http://localhost:5000 or http://[your-ip]:5000
        
    Startup Checks:
        - Verifies analysis module availability
        - Displays appropriate warnings if modules missing
        - Provides clear startup instructions and URL
        
    Production Note:
        For production deployment, use a proper WSGI server like
        Gunicorn or uWSGI instead of the Flask development server.
    """
    print("🚀 Starting PyStock Analyzer Web Server...")
    print("=" * 50)
    
    # =============== MODULE AVAILABILITY CHECK ===============
    if not ANALYSIS_AVAILABLE:
        print("⚠️  WARNING: Analysis modules not available!")
        print("   Web interface will run in limited mode.")
        print("   Please check your installation and dependencies.")
    else:
        print("✅ All analysis modules loaded successfully")
    
    # =============== SERVER STARTUP INFORMATION ===============
    print("🌐 Server Configuration:")
    print("   URL: http://localhost:5000")
    print("   Network Access: http://[your-ip]:5000")
    print("   Debug Mode: Enabled")
    print("=" * 50)
    print("📋 Available Endpoints:")
    print("   /          - Main analysis interface")
    print("   /compare   - Multi-stock comparison")
    print("   /export    - CSV data export")
    print("   /api/...   - Real-time API endpoints")
    print("=" * 50)
    print("🛑 Press Ctrl+C to stop the server")
    print()
    
    # =============== FLASK SERVER STARTUP ===============
    app.run(debug=True, host='0.0.0.0', port=5000)