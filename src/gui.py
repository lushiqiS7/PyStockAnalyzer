import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from data_loader import fetch_stock_data
from calculations import calculate_sma, identify_runs, calculate_daily_returns, calculate_rsi, calculate_bollinger_bands
from advanced_calculations import calculate_max_profit
from visualizer import plot_stock_data, display_analysis_results
import threading

class StockAnalyzerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("PyStock Analyzer - Enhanced")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f0f0')
        
        self.setup_gui()
        
    def setup_gui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Input section
        input_frame = ttk.LabelFrame(main_frame, text="Stock Data Input", padding="10")
        input_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # Ticker input
        ttk.Label(input_frame, text="Stock Ticker:").grid(row=0, column=0, sticky=tk.W, padx=5)
        self.ticker_var = tk.StringVar(value="AAPL")
        ttk.Entry(input_frame, textvariable=self.ticker_var, width=10).grid(row=0, column=1, padx=5)
        
        # Period selection
        ttk.Label(input_frame, text="Time Period:").grid(row=0, column=2, sticky=tk.W, padx=5)
        self.period_var = tk.StringVar(value="6mo")
        period_combo = ttk.Combobox(input_frame, textvariable=self.period_var, 
                                   values=["1mo", "3mo", "6mo", "1y", "2y"], width=8)
        period_combo.grid(row=0, column=3, padx=5)
        
        # SMA window
        ttk.Label(input_frame, text="SMA Window:").grid(row=0, column=4, sticky=tk.W, padx=5)
        self.sma_var = tk.StringVar(value="10")
        ttk.Entry(input_frame, textvariable=self.sma_var, width=5).grid(row=0, column=5, padx=5)
        
        # Analyze button
        self.analyze_btn = ttk.Button(input_frame, text="Analyze Stock", 
                                     command=self.analyze_stock)
        self.analyze_btn.grid(row=0, column=6, padx=10)
        
        # Results section
        results_frame = ttk.LabelFrame(main_frame, text="Analysis Results", padding="10")
        results_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        # Text area for results
        self.results_text = scrolledtext.ScrolledText(results_frame, height=15, width=80)
        self.results_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Chart section
        chart_frame = ttk.LabelFrame(main_frame, text="Price Chart with Technical Indicators", padding="10")
        chart_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        # Matplotlib figure
        self.fig, self.ax = plt.subplots(figsize=(12, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, chart_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready to analyze stocks...")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=5)
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=2)
        
    def analyze_stock(self):
        """Handle stock analysis in a separate thread to prevent GUI freezing"""
        self.analyze_btn.config(state='disabled')
        self.status_var.set("Fetching data...")
        
        # Run analysis in separate thread
        thread = threading.Thread(target=self._perform_analysis)
        thread.daemon = True
        thread.start()
        
    def _perform_analysis(self):
        """Perform the actual stock analysis"""
        try:
            ticker = self.ticker_var.get().upper()
            period = self.period_var.get()
            sma_window = int(self.sma_var.get())
            
            # Fetch data
            self.status_var.set(f"Fetching data for {ticker}...")
            stock_data = fetch_stock_data(ticker, period)
            
            if stock_data is None:
                messagebox.showerror("Error", f"Failed to fetch data for {ticker}")
                return
            
            # Perform calculations
            self.status_var.set("Performing analysis...")
            sma = calculate_sma(stock_data, sma_window)
            runs_data = identify_runs(stock_data)
            returns = calculate_daily_returns(stock_data)
            max_profit = calculate_max_profit(stock_data['Close'].tolist())
            
            # Calculate advanced indicators
            rsi = calculate_rsi(stock_data, 14)
            upper_band, middle_band, lower_band = calculate_bollinger_bands(stock_data, 20, 2)
            
            # Display results
            self._display_results(stock_data, sma, runs_data, returns, max_profit, sma_window, rsi, upper_band, middle_band, lower_band)
            
            # Update chart
            self._update_chart(stock_data, sma, sma_window, upper_band, lower_band)
            
            self.status_var.set(f"Analysis complete for {ticker}!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Analysis failed: {str(e)}")
        finally:
            self.analyze_btn.config(state='normal')
            
    def _display_results(self, data, sma, runs_data, returns, max_profit, sma_window, rsi, upper_band, middle_band, lower_band):
        """Display enhanced analysis results with RSI and Bollinger Bands"""
        result_text = f"{'='*60}\n"
        result_text += "ENHANCED STOCK ANALYSIS RESULTS\n"
        result_text += f"{'='*60}\n\n"
        
        result_text += f"1. SIMPLE MOVING AVERAGE ({sma_window} days):\n"
        result_text += f"   Latest SMA value: ${sma.iloc[-1]:.2f}\n\n"
        
        result_text += f"2. PRICE RUN ANALYSIS:\n"
        result_text += f"   Total upward days: {runs_data['total_up_days']}\n"
        result_text += f"   Total downward days: {runs_data['total_down_days']}\n"
        result_text += f"   Longest upward streak: {runs_data['longest_up_streak']} days\n"
        result_text += f"   Longest downward streak: {runs_data['longest_down_streak']} days\n\n"
        
        result_text += f"3. DAILY RETURNS:\n"
        result_text += f"   Average daily return: {returns.mean():.4f}\n"
        result_text += f"   Return volatility (std dev): {returns.std():.4f}\n\n"
        
        result_text += f"4. MAXIMUM PROFIT ANALYSIS:\n"
        result_text += f"   Maximum achievable profit: ${max_profit:.2f}\n"
        result_text += f"   (Multiple transactions allowed)\n\n"
        
        # RSI Analysis
        result_text += f"5. RELATIVE STRENGTH INDEX (RSI):\n"
        result_text += f"   Current RSI: {rsi.iloc[-1]:.2f}\n"
        rsi_status = "Overbought (>70)" if rsi.iloc[-1] > 70 else "Oversold (<30)" if rsi.iloc[-1] < 30 else "Neutral"
        result_text += f"   Interpretation: {rsi_status}\n"
        result_text += f"   RSI Range: {rsi.min():.2f} to {rsi.max():.2f}\n\n"
        
        # Bollinger Bands Analysis
        result_text += f"6. BOLLINGER BANDS ANALYSIS:\n"
        current_price = data['Close'].iloc[-1]
        band_status = "Above Upper Band (Overbought)" if current_price > upper_band.iloc[-1] else "Below Lower Band (Oversold)" if current_price < lower_band.iloc[-1] else "Within Bands (Neutral)"
        result_text += f"   Current Price: {band_status}\n"
        band_width = (upper_band.iloc[-1] - lower_band.iloc[-1]) / middle_band.iloc[-1] * 100
        result_text += f"   Band Width: {band_width:.2f}% (Higher = More Volatile)\n\n"
        
        # Data Summary
        result_text += f"7. DATA SUMMARY:\n"
        result_text += f"   Period: {data.index[0].date()} to {data.index[-1].date()}\n"
        result_text += f"   Total trading days: {len(data)}\n"
        result_text += f"   Starting price: ${data['Close'].iloc[0]:.2f}\n"
        result_text += f"   Ending price: ${data['Close'].iloc[-1]:.2f}\n"
        total_change = ((data['Close'].iloc[-1] / data['Close'].iloc[0]) - 1) * 100
        result_text += f"   Total change: {total_change:.2f}%\n"
        
        # Update GUI in main thread
        self.root.after(0, lambda: self._update_results_text(result_text))
        
    def _update_results_text(self, text):
        """Update the results text area (thread-safe)"""
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(1.0, text)
        
    def _update_chart(self, data, sma, sma_window, upper_band, lower_band):
        """Update the matplotlib chart with technical indicators"""
        self.ax.clear()
        
        # Plot closing price
        self.ax.plot(data.index, data['Close'], label='Closing Price', color='blue', alpha=0.7, linewidth=1.5)
        
        # Plot SMA
        self.ax.plot(data.index, sma, label=f'SMA ({sma_window} days)', color='red', linewidth=2)
        
        # Plot Bollinger Bands
        self.ax.plot(data.index, upper_band, label='Upper Bollinger Band', color='green', linestyle='--', alpha=0.7)
        self.ax.plot(data.index, lower_band, label='Lower Bollinger Band', color='red', linestyle='--', alpha=0.7)
        self.ax.fill_between(data.index, lower_band, upper_band, alpha=0.1, color='gray', label='Bollinger Band Area')
        
        # Format chart
        self.ax.set_title(f'{self.ticker_var.get()} Price with Technical Indicators', fontsize=14, fontweight='bold')
        self.ax.set_xlabel('Date', fontweight='bold')
        self.ax.set_ylabel('Price ($)', fontweight='bold')
        self.ax.legend()
        self.ax.grid(True, alpha=0.3)
        self.ax.tick_params(axis='x', rotation=45)
        
        # Update canvas
        self.fig.tight_layout()
        self.canvas.draw()

def main():
    """Main function to start the GUI application"""
    root = tk.Tk()
    app = StockAnalyzerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()