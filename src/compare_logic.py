"""
Stock comparison and ranking module for the PyStock Analyzer.

This module provides functionality to compare multiple stocks side-by-side,
perform comprehensive analysis across different securities, and rank them
based on various financial metrics and technical indicators. It's designed
to help investors make informed decisions when choosing between multiple
investment options.

Key Features:
- Multi-stock comparative analysis
- Comprehensive scoring system for ranking stocks
- Technical indicator comparison (SMA, RSI, volatility)
- Performance metrics calculation and comparison
- Chart data preparation for visualization
- Run period analysis for trend identification

Scoring Criteria:
- Total return performance (weighted positively)
- Volatility assessment (lower is better)
- Maximum profit potential (weighted positively)
- RSI momentum analysis (neutral preferred)
- Technical indicator signals
"""

import pandas as pd
from data_loader import fetch_stock_data
from calculations import calculate_sma, calculate_rsi, identify_run_periods
from advanced_calculations import calculate_max_profit


def do_compare_logic(tickers, period='6mo', sma_window=10):
    """
    Perform comprehensive comparative analysis across multiple stocks.
    
    This function fetches data for multiple stock tickers and performs
    standardized analysis to enable fair comparison. It calculates all
    major technical indicators, performance metrics, and prepares data
    for both tabular comparison and chart visualization.
    
    Args:
        tickers (list): List of stock ticker symbols to compare (e.g., ['AAPL', 'MSFT', 'GOOGL']).
        period (str, optional): Time period for analysis. Defaults to '6mo'.
                               Valid periods: '1mo', '3mo', '6mo', '1y', '2y', 'ytd', 'max'.
        sma_window (int, optional): Window size for Simple Moving Average calculation.
                                   Defaults to 10.
    
    Returns:
        tuple: A tuple containing:
            - all_results_list (list): List of dictionaries with analysis results for each stock
            - all_charts (dict): Dictionary with chart data for visualization, keyed by ticker
            
    Analysis Includes:
        - Current and historical price data
        - Simple Moving Average calculations
        - RSI (Relative Strength Index) with interpretation
        - Volatility measurements
        - Maximum profit potential calculations
        - Trend run period identification
        - Performance metrics and percentage changes
        
    Example:
        >>> tickers = ['AAPL', 'MSFT', 'GOOGL']
        >>> results, charts = do_compare_logic(tickers, period='6mo', sma_window=20)
        >>> for result in results:
        ...     print(f"{result['ticker']}: {result['total_change']:.2f}% change")
    """
    all_results_list = []
    all_charts = {}

    print(f"Analyzing {len(tickers)} stocks over {period} period...")

    for ticker in tickers:
        print(f"Processing {ticker}...")
        
        # =============== DATA FETCHING ===============
        stock_data = fetch_stock_data(ticker, period)

        if stock_data is None or stock_data.empty:
            print(f"⚠️  Skipping {ticker} due to empty or unavailable data.")
            continue
        
        # =============== TECHNICAL INDICATORS ===============
        # Simple Moving Average calculation
        sma = calculate_sma(stock_data, sma_window)
        
        # RSI (Relative Strength Index) calculation
        rsi = calculate_rsi(stock_data, window=14)
        rsi_current = rsi.iloc[-1] if not rsi.empty else None

        # RSI interpretation for investment signals
        rsi_status = "Neutral"
        if rsi_current is not None:
            if rsi_current < 30:
                rsi_status = "Oversold"  # Potential buy signal
            elif rsi_current > 70:
                rsi_status = "Overbought"  # Potential sell signal

        # =============== VOLATILITY ANALYSIS ===============
        # Calculate daily returns and volatility (risk measure)
        returns = stock_data['Close'].pct_change().dropna()
        volatility = returns.std() * 100 if not returns.empty else None  # Convert to percentage

        # =============== PROFIT ANALYSIS ===============
        # Calculate maximum profit potential using advanced algorithm
        prices = stock_data['Close'].tolist()
        max_profit = calculate_max_profit(prices) if prices else None

        # =============== PERFORMANCE METRICS ===============
        # Calculate overall performance during the analysis period
        start_price = stock_data['Close'].iloc[0]
        current_price = stock_data['Close'].iloc[-1]
        total_change = ((current_price / start_price) - 1) * 100

        # =============== COMPILE RESULTS ===============
        result_data = {
            'ticker': ticker,
            'current_price': round(current_price, 2),
            'start_price': round(start_price, 2),
            'total_change': round(total_change, 2),
            'sma_window': sma_window,
            'sma_current': round(sma.iloc[-1], 2) if not sma.empty else None,
            'rsi_current': round(rsi_current, 2) if rsi_current is not None else None,
            'rsi_status': rsi_status,
            'volatility': round(volatility, 2) if volatility is not None else None,
            'max_profit': round(max_profit, 2) if max_profit is not None else None,
        }
        
        all_results_list.append(result_data)

        # =============== TREND RUN ANALYSIS ===============
        # Get run periods for trend visualization
        run_periods = identify_run_periods(stock_data)
        
        # Format run periods for chart visualization (only significant runs)
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
        # Prepare data for visualization components
        all_charts[ticker] = {
            'dates': [d.strftime('%Y-%m-%d') for d in stock_data.index],
            'prices': stock_data['Close'].round(2).tolist(),
            'sma': sma.round(2).where(pd.notnull(sma), None).tolist(),
            'rsi': rsi.round(2).where(pd.notnull(rsi), None).tolist(),
            'volume': stock_data['Volume'].astype(int).tolist(),
            'runs': run_highlights
        }

    print(f"✅ Successfully analyzed {len(all_results_list)} out of {len(tickers)} stocks.")
    return all_results_list, all_charts

def score_stock(result):
    """
    Calculate a comprehensive investment score for a stock based on multiple criteria.
    
    This function implements a sophisticated scoring algorithm that evaluates
    stocks across multiple dimensions including performance, risk, technical
    indicators, and momentum. The scoring system is designed to identify
    stocks with the best risk-adjusted return potential.
    
    Args:
        result (dict): Dictionary containing stock analysis results with keys:
                      - 'total_change': Percentage price change over period
                      - 'volatility': Volatility measure (standard deviation of returns)
                      - 'max_profit': Maximum profit potential
                      - 'rsi_status': RSI interpretation ('Neutral', 'Oversold', 'Overbought')
                      - 'rsi_current': Current RSI value
    
    Returns:
        float: Comprehensive investment score. Higher scores indicate more
               attractive investment opportunities.
               
    Scoring Components:
        1. Total Change (3x weight): Rewards positive performance
        2. Volatility (2x weight, negative): Penalizes high risk
        3. Max Profit (2x weight): Rewards trading opportunities
        4. RSI Status Bonus: Neutral (+10), Oversold (+5), Overbought (-10)
        5. RSI Range Bonus: +5 for values in healthy 30-70 range
        
    Example:
        >>> stock_result = {
        ...     'total_change': 15.5,
        ...     'volatility': 2.1,
        ...     'max_profit': 125.50,
        ...     'rsi_status': 'Neutral',
        ...     'rsi_current': 55.3
        ... }
        >>> score = score_stock(stock_result)
        >>> print(f"Investment Score: {score:.2f}")
    """
    score = 0

    def safe_float(val):
        """Safely convert value to float, handling None and invalid values."""
        try:
            return float(val)
        except (TypeError, ValueError):
            return None

    # =============== COMPONENT 1: TOTAL RETURN PERFORMANCE ===============
    # Reward positive performance, heavily weighted (3x multiplier)
    total_change = safe_float(result.get("total_change"))
    if total_change is not None:
        score += total_change * 3
        # Bonus for exceptional performance
        if total_change > 20:
            score += 10  # Extra bonus for strong performers

    # =============== COMPONENT 2: VOLATILITY (RISK ASSESSMENT) ===============
    # Penalize high volatility as it represents higher risk (2x negative weight)
    volatility = safe_float(result.get("volatility"))
    if volatility is not None:
        score -= volatility * 2
        # Additional penalty for extremely volatile stocks
        if volatility > 5:
            score -= 5  # Extra penalty for very high risk

    # =============== COMPONENT 3: MAXIMUM PROFIT POTENTIAL ===============
    # Reward stocks with higher profit opportunities (2x weight)
    max_profit = safe_float(result.get("max_profit"))
    if max_profit is not None:
        score += max_profit * 2

    # =============== COMPONENT 4: RSI MOMENTUM STATUS ===============
    # Reward balanced momentum, penalize extremes
    rsi_status = result.get("rsi_status")
    if rsi_status == "Neutral":
        score += 10  # Preferred: balanced momentum
    elif rsi_status == "Oversold":
        score += 5   # Potential buying opportunity
    elif rsi_status == "Overbought":
        score -= 10  # Potential selling pressure

    # =============== COMPONENT 5: RSI VALUE RANGE ASSESSMENT ===============
    # Bonus for RSI values in healthy trading range (30-70)
    rsi_current = safe_float(result.get("rsi_current"))
    if rsi_current is not None and 30 <= rsi_current <= 70:
        score += 5  # Healthy momentum range bonus

    return score


def choose_best_stock(all_results):
    """
    Identify the best investment opportunity from a list of analyzed stocks.
    
    This function evaluates all analyzed stocks using the comprehensive
    scoring system and identifies the stock with the highest investment
    score. It also adds the calculated score to each stock's result data
    for transparency and comparison purposes.
    
    Args:
        all_results (list): List of dictionaries containing stock analysis results.
                           Each dictionary should contain the data required by score_stock().
    
    Returns:
        dict or None: Dictionary containing the analysis results for the highest-scoring
                     stock, including the calculated score. Returns None if no valid
                     results are provided.
                     
    Side Effects:
        - Adds 'score' key to each result dictionary in all_results
        - Modifies the input list by adding score information
        
    Example:
        >>> results = [
        ...     {'ticker': 'AAPL', 'total_change': 12.5, 'volatility': 1.8, ...},
        ...     {'ticker': 'MSFT', 'total_change': 8.3, 'volatility': 1.2, ...}
        ... ]
        >>> best = choose_best_stock(results)
        >>> print(f"Best stock: {best['ticker']} with score: {best['score']}")
        
    Note:
        This function modifies the input list by adding score information.
        The scoring considers multiple factors for a balanced assessment
        of investment attractiveness.
    """
    if not all_results:
        return None
        
    best_stock = None
    highest_score = float('-inf')

    print("Calculating investment scores for all stocks...")

    # Calculate scores for all stocks and track the best one
    for result in all_results:
        stock_score = score_stock(result)
        result["score"] = round(stock_score, 2)
        
        print(f"  {result['ticker']}: Score = {stock_score:.2f}")
        
        # Track the highest scoring stock
        if stock_score > highest_score:
            highest_score = stock_score
            best_stock = result

    if best_stock:
        print(f"\n🏆 Best Investment Opportunity: {best_stock['ticker']} (Score: {best_stock['score']})")
    
    return best_stock


# Entry point for direct script execution
if __name__ == "__main__":
    """
    Entry point for direct script execution.
    
    When this module is run directly, it demonstrates the comparison
    functionality with a sample set of popular technology stocks.
    """
    print("Stock Comparison Module - Testing with sample stocks...")
    
    # Test with popular technology stocks
    test_tickers = ['AAPL', 'MSFT', 'GOOGL']
    
    print(f"Comparing: {', '.join(test_tickers)}")
    results, charts = do_compare_logic(test_tickers, period='3mo', sma_window=10)
    
    if results:
        best = choose_best_stock(results)
        print(f"\nComparison completed successfully!")
        print(f"Analyzed {len(results)} stocks with comprehensive scoring.")
    else:
        print("No valid results obtained. Check internet connection and ticker symbols.")