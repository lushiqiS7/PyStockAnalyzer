import pandas as pd
from data_loader import fetch_stock_data
from calculations import calculate_sma, calculate_rsi


def do_compare_logic(tickers, period='6mo', sma_window=10):
    all_results_list = []
    all_charts = {}

    for ticker in tickers:
        stock_data = fetch_stock_data(ticker, period)

        if stock_data is None or stock_data.empty:
            print(f"Skipping {ticker} due to empty data.")
            continue

        sma = calculate_sma(stock_data, sma_window)
        rsi = calculate_rsi(stock_data, 14)

        all_results_list.append({
            'ticker': ticker,
            'current_price': round(stock_data['Close'].iloc[-1], 2),
            'start_price': round(stock_data['Close'].iloc[0], 2),
            'total_change': round(((stock_data['Close'].iloc[-1] / stock_data['Close'].iloc[0]) - 1) * 100, 2),
            'sma_window': sma_window,
            'sma_current': round(sma.iloc[-1], 2) if not sma.empty else None,
            'rsi_current': round(rsi.iloc[-1], 2) if not rsi.empty else None,
            'rsi_status': "Neutral",  # You can add logic here based on RSI value
            'volatility': "N/A",      # Add actual volatility calculation if needed
            'max_profit': "N/A",      # Add max profit calculation if needed
        })

        all_charts[ticker] = {
            'dates': [d.strftime('%Y-%m-%d') for d in stock_data.index],
            'prices': stock_data['Close'].round(2).tolist(),
            'sma': sma.round(2).where(pd.notnull(sma), None).tolist(),
            'rsi': rsi.round(2).where(pd.notnull(rsi), None).tolist(),
            'volume': stock_data['Volume'].astype(int).tolist(),
        }

    return all_results_list, all_charts
