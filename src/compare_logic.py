import pandas as pd
from data_loader import fetch_stock_data
from calculations import calculate_sma, calculate_rsi, identify_run_periods
from advanced_calculations import calculate_max_profit

#Comparison for multiple stocks
def do_compare_logic(tickers, period='6mo', sma_window=10):
    all_results_list = []
    all_charts = {}

    for ticker in tickers:
        stock_data = fetch_stock_data(ticker, period)

        if stock_data is None or stock_data.empty:
            print(f"Skipping {ticker} due to empty data.")
            continue
        
        # --- SMA ---
        sma = calculate_sma(stock_data, sma_window)
        # --- RSI ---
        rsi = calculate_rsi(stock_data, 14)
        # --- RSI current ---
        rsi_current = rsi.iloc[-1] if not rsi.empty else None

        # --- RSI status ---
        rsi_status = "Neutral"
        if rsi_current is not None:
            if rsi_current < 30:
                rsi_status = "Oversold"
            elif rsi_current > 70:
                rsi_status = "Overbought"

        # --- Volatility ---
        returns = stock_data['Close'].pct_change().dropna()
        volatility = returns.std() * 100 if not returns.empty else None

        # --- Max Profit ---
        prices = stock_data['Close'].tolist()
        max_profit = calculate_max_profit(prices) if prices else None

        # Compile results
        all_results_list.append({
            'ticker': ticker,
            'current_price': round(stock_data['Close'].iloc[-1], 2),
            'start_price': round(stock_data['Close'].iloc[0], 2),
            'total_change': round(((stock_data['Close'].iloc[-1] / stock_data['Close'].iloc[0]) - 1) * 100, 2),
            'sma_window': sma_window,
            'sma_current': round(sma.iloc[-1], 2) if not sma.empty else None,
            'rsi_current': round(rsi.iloc[-1], 2) if not rsi.empty else None,
            'rsi_status': rsi_status,
            'volatility': round(volatility, 2) if volatility is not None else None,
            'max_profit': round(max_profit, 2) if max_profit is not None else None,
        })

        # Get run periods for highlighting
        run_periods = identify_run_periods(stock_data)
        
        # Format run periods for chart visualization
        run_highlights = []
        for run in run_periods:
            if run['length'] >= 2:  # Only highlight runs of 2+ days
                run_highlights.append({
                    'start': run['start_date'].strftime('%Y-%m-%d'),
                    'end': run['end_date'].strftime('%Y-%m-%d'),
                    'direction': 'up' if run['direction'] == 1 else 'down',
                    'length': run['length']
                })

        #Chart data
        all_charts[ticker] = {
            'dates': [d.strftime('%Y-%m-%d') for d in stock_data.index],
            'prices': stock_data['Close'].round(2).tolist(),
            'sma': sma.round(2).where(pd.notnull(sma), None).tolist(),
            'rsi': rsi.round(2).where(pd.notnull(rsi), None).tolist(),
            'volume': stock_data['Volume'].astype(int).tolist(),
            'runs': run_highlights
        }

    return all_results_list, all_charts

#Scoring system
def score_stock(result):
    score = 0

    def safe_float(val):
        try:
            return float(val)
        except (TypeError, ValueError):
            return None

    # 1. Total Change (positive = good)
    total_change = safe_float(result.get("total_change"))
    if total_change is not None:
        score += total_change * 3

    # 2. Volatility (lower is better)
    volatility = safe_float(result.get("volatility"))
    if volatility is not None:
        score -= volatility * 2

    # 3. Max Profit
    max_profit = safe_float(result.get("max_profit"))
    if max_profit is not None:
        score += max_profit * 2

    # 4. RSI status
    rsi_status = result.get("rsi_status")
    if rsi_status == "Neutral":
        score += 10
    elif rsi_status == "Oversold":
        score += 5
    elif rsi_status == "Overbought":
        score -= 10

    # 5. RSI value in valid range (30–70)
    rsi = safe_float(result.get("rsi_current"))
    if rsi is not None and 30 <= rsi <= 70:
        score += 5

    return score


def choose_best_stock(all_results):
    best = None
    highest_score = float('-inf')

    for result in all_results:
        result_score = score_stock(result)
        result["score"] = round(result_score, 2)
        if result_score > highest_score:
            highest_score = result_score
            best = result

    return best



