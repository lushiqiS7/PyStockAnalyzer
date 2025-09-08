import pandas as pd
import numpy as np
from data_loader import fetch_stock_data
from calculations import calculate_daily_returns

class PortfolioAnalyzer:
    """Analyzes a portfolio of multiple stocks"""
    
    def __init__(self):
        self.stocks = {}
        self.weights = {}
    
    def add_stock(self, ticker, weight):
        """Add a stock to the portfolio with its weight"""
        self.stocks[ticker] = None  # Will store data when loaded
        self.weights[ticker] = weight
    
    def load_portfolio_data(self, period="1y"):
        """Load data for all stocks in the portfolio"""
        for ticker in self.stocks:
            data = fetch_stock_data(ticker, period)
            if data is not None:
                self.stocks[ticker] = data
            else:
                print(f"Warning: Could not load data for {ticker}")
    
    def calculate_portfolio_returns(self):
        """Calculate weighted portfolio returns"""
        portfolio_returns = None
        
        for ticker, data in self.stocks.items():
            if data is not None:
                returns = calculate_daily_returns(data)
                weight = self.weights[ticker]
                
                if portfolio_returns is None:
                    portfolio_returns = returns * weight
                else:
                    # Align indices and add weighted returns
                    aligned_returns = returns.reindex(portfolio_returns.index, fill_value=0)
                    portfolio_returns += aligned_returns * weight
        
        return portfolio_returns
    
    def analyze_portfolio(self):
        """Comprehensive portfolio analysis"""
        if not self.stocks:
            return {"error": "No stocks in portfolio"}
        
        self.load_portfolio_data()
        portfolio_returns = self.calculate_portfolio_returns()
        
        if portfolio_returns is None:
            return {"error": "Could not calculate portfolio returns"}
        
        # Calculate portfolio statistics
        total_return = (portfolio_returns + 1).prod() - 1
        annual_return = (1 + total_return) ** (252 / len(portfolio_returns)) - 1
        volatility = portfolio_returns.std() * np.sqrt(252)
        sharpe_ratio = annual_return / volatility if volatility > 0 else 0
        
        return {
            "total_return": total_return,
            "annual_return": annual_return,
            "volatility": volatility,
            "sharpe_ratio": sharpe_ratio,
            "max_drawdown": self.calculate_max_drawdown(portfolio_returns),
            "stock_contributions": self.calculate_contributions()
        }
    
    def calculate_max_drawdown(self, returns):
        """Calculate maximum drawdown"""
        cumulative_returns = (1 + returns).cumprod()
        peak = cumulative_returns.expanding().max()
        drawdown = (cumulative_returns - peak) / peak
        return drawdown.min()
    
    def calculate_contributions(self):
        """Calculate contribution of each stock to portfolio return"""
        contributions = {}
        total_return = 0
        
        for ticker, data in self.stocks.items():
            if data is not None:
                returns = calculate_daily_returns(data)
                stock_return = (returns + 1).prod() - 1
                weighted_return = stock_return * self.weights[ticker]
                contributions[ticker] = weighted_return
                total_return += weighted_return
        
        # Convert to percentages
        if total_return > 0:
            for ticker in contributions:
                contributions[ticker] = contributions[ticker] / total_return * 100
        
        return contributions

# Example usage
def analyze_sample_portfolio():
    """Example portfolio analysis"""
    portfolio = PortfolioAnalyzer()
    portfolio.add_stock("AAPL", 0.4)  # 40% Apple
    portfolio.add_stock("MSFT", 0.3)  # 30% Microsoft
    portfolio.add_stock("GOOGL", 0.3) # 30% Google
    
    results = portfolio.analyze_portfolio()
    return results