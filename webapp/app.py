from flask import Flask, render_template, request, jsonify, Response
import sys
import os
from datetime import datetime
import pandas as pd
from flask.helpers import redirect, url_for

# Add src directory to path to import your modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

try:
    from data_loader import fetch_stock_data
    from calculations import calculate_sma, identify_runs, calculate_daily_returns, calculate_rsi, calculate_bollinger_bands
    from advanced_calculations import calculate_max_profit
    from compare_logic import do_compare_logic, choose_best_stock, score_stock
    ANALYSIS_AVAILABLE = True
except ImportError as e:
    print(f"Analysis modules not available: {e}")
    ANALYSIS_AVAILABLE = False

app = Flask(__name__)

@app.route('/')
def index():
    """Main page with stock analysis form"""
    return render_template('index.html', analysis_available=ANALYSIS_AVAILABLE)

# Combined route to handle both single and compare modes
@app.route('/analyze_or_compare', methods=['POST'])
def analyze_or_compare():
    mode = request.form.get('mode', 'single')
    tickers_raw = request.form.get('tickers')
    if not tickers_raw:
        return "No tickers provided", 400
    tickers = [t.strip().upper() for t in tickers_raw.split(',') if t.strip()]
    period = request.form.get('period', '6mo')
    sma_window = int(request.form.get('sma_window', '10'))

    if mode == 'compare' and len(tickers) > 1:
        # do compare logic
        all_results, all_charts = do_compare_logic(tickers, period, sma_window)
        analysis_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        best_stock = choose_best_stock(all_results)
        recommended_ticker = best_stock["ticker"] if best_stock else None

        return render_template(
            'compare_results.html',
            all_results=all_results,
            all_charts=all_charts,
            analysis_date=analysis_date,
            recommendation_reason="best overall score across return, risk, and RSI indicators",
            best_score=best_stock["score"] if best_stock else None,
            recommended_ticker=recommended_ticker
        )
    else:
        # assume single or fallback
        return analyze_stock()
    
 # Single stock analysis   
@app.route('/analyze', methods=['POST'])
def analyze_stock():
    """Analyze stock and return results"""
    if not ANALYSIS_AVAILABLE:
        return render_template('error.html', error="Analysis modules not available. Please check your installation.")
    
    try:
        # Get and parse form input
        tickers_input = request.form.get('tickers')
        if not tickers_input:
            return "No tickers provided", 400  # Or show an error page
        tickers = [t.strip().upper() for t in tickers_input.split(',')]
        period = request.form.get('period', '6mo')
        sma_window = int(request.form.get('sma_window', '10'))

        all_results = []
        all_charts = {}

        for ticker in tickers:
            stock_data = fetch_stock_data(ticker, period)
            if stock_data is None or stock_data.empty:
                continue
        
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
            
        all_results.append(results)  
        
        # Chart data per ticker
        all_charts[ticker] = {
                'dates': [d.strftime('%Y-%m-%d') for d in stock_data.index],
                'prices': stock_data['Close'].round(2).tolist(),
                'sma': sma.round(2).where(pd.notnull(sma), None).tolist(),
                'rsi': rsi.round(2).where(pd.notnull(rsi), None).tolist(),
                'volume': stock_data['Volume'].astype(int).tolist()
            }

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
    


#export results as CSV
@app.route('/export')
def export_results():
    if not ANALYSIS_AVAILABLE:
        return "Export not available", 503

    try:
        # Get query params
        ticker = request.args.get('ticker', 'AAPL').upper()
        period = request.args.get('period', '6mo')
        sma_window = int(request.args.get('sma_window', '10'))

        # Fetch data
        stock_data = fetch_stock_data(ticker, period)
        if stock_data is None or stock_data.empty:
            return "No data available for export", 400

        # Optional: include SMA in export
        stock_data['SMA'] = calculate_sma(stock_data, sma_window)

        # Convert to CSV
        csv_data = stock_data.to_csv(index=True)

        # Return as downloadable file
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