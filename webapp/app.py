from flask import Flask, render_template, request, jsonify
import sys
import os
from datetime import datetime
import pandas as pd

# Add src directory to path to import your modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

try:
    from data_loader import fetch_stock_data
    from calculations import calculate_sma, identify_runs, calculate_daily_returns, calculate_rsi, calculate_bollinger_bands
    from advanced_calculations import calculate_max_profit
    ANALYSIS_AVAILABLE = True
except ImportError as e:
    print(f"Analysis modules not available: {e}")
    ANALYSIS_AVAILABLE = False

app = Flask(__name__)

@app.route('/')
def index():
    """Main page with stock analysis form"""
    return render_template('index.html', analysis_available=ANALYSIS_AVAILABLE)

@app.route('/analyze', methods=['POST'])
def analyze_stock():
    """Analyze stock and return results"""
    if not ANALYSIS_AVAILABLE:
        return render_template('error.html', error="Analysis modules not available. Please check your installation.")
    
    try:
        # Get form data
        ticker = request.form.get('ticker', 'AAPL').upper()
        period = request.form.get('period', '6mo')
        sma_window = int(request.form.get('sma_window', '10'))
        
        # Fetch data
        stock_data = fetch_stock_data(ticker, period)
        
        if stock_data is None or stock_data.empty:
            return render_template('error.html', error=f"Could not fetch data for {ticker}. Please check the ticker symbol.")
        
        # Perform calculations
        sma = calculate_sma(stock_data, sma_window)
        runs_data = identify_runs(stock_data)
        returns = calculate_daily_returns(stock_data)
        max_profit = calculate_max_profit(stock_data['Close'].tolist())
        rsi = calculate_rsi(stock_data, 14)
        upper_band, middle_band, lower_band = calculate_bollinger_bands(stock_data, 20, 2)
        
        # Prepare results
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
        
        # Add RSI status
        if results['rsi_current'] != 'N/A':
            if results['rsi_current'] > 70:
                results['rsi_status'] = 'Overbought'
            elif results['rsi_current'] < 30:
                results['rsi_status'] = 'Oversold'
            else:
                results['rsi_status'] = 'Neutral'
        else:
            results['rsi_status'] = 'N/A'
        
        #prepare data for charts
        chart_data = {
        'dates': [d.strftime('%Y-%m-%d') for d in stock_data.index],
        'prices': stock_data['Close'].round(2).tolist(),
        'sma': calculate_sma(stock_data, sma_window).round(2).where(pd.notnull(calculate_sma(stock_data, sma_window)), None).tolist(),
        'rsi': calculate_rsi(stock_data, 14).round(2).where(pd.notnull(calculate_rsi(stock_data, 14)), None).tolist(),
        'volume': stock_data['Volume'].astype(int).tolist()

    }
        # Pass both results and chart_data to template
        return render_template("results.html", results=results, chart_data=chart_data)


        

    except Exception as e:
        return render_template('error.html', error=f"Analysis error: {str(e)}")

@app.errorhandler(404)
def not_found(error):
    return render_template('error.html', error="Page not found"), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('error.html', error="Internal server error"), 500

if __name__ == '__main__':
    print("Starting PyStock Analyzer Web Server...")
    if not ANALYSIS_AVAILABLE:
        print("WARNING: Analysis modules not available. Web interface will run in limited mode.")
    print("Open: http://localhost:5000")
    print("Press Ctrl+C to stop the server")
    app.run(debug=True, host='0.0.0.0', port=5000)