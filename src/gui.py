"""
Graphical User Interface module for the PyStock Analyzer.

This module provides a comprehensive GUI application built with tkinter that allows
users to analyze stock data interactively. The interface includes input controls,
data visualization with matplotlib, and detailed analysis results display.

Key Features:
- Interactive stock data fetching and analysis
- Real-time chart visualization with technical indicators
- Bollinger Bands and RSI analysis
- Run period highlighting for trend analysis
- Multi-threaded operations to prevent GUI freezing
- Export capabilities for analysis results

Dependencies:
- tkinter: GUI framework
- matplotlib: Charting and visualization
- pandas: Data manipulation
- Custom modules: data_loader, calculations, visualizer, advanced_calculations
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import threading
import pandas as pd
from tkinter import filedialog
import sys
import os

# Import custom analysis modules
from data_loader import fetch_stock_data
from calculations import (calculate_sma, identify_runs, calculate_daily_returns, 
                         calculate_rsi, calculate_bollinger_bands, identify_run_periods)
from advanced_calculations import calculate_max_profit
from visualizer import plot_stock_data, display_analysis_results


class StockAnalyzerGUI:
    """
    Main GUI application class for stock analysis.
    
    This class creates and manages the complete graphical user interface for the
    PyStock Analyzer application. It handles user input, data visualization,
    analysis results display, and provides an intuitive interface for stock
    market analysis.
    
    Attributes:
        root (tk.Tk): Main application window
        fig (matplotlib.Figure): Matplotlib figure for charts
        ax (matplotlib.Axes): Matplotlib axes for plotting
        canvas (FigureCanvasTkAgg): Matplotlib canvas widget
        toolbar (NavigationToolbar2Tk): Chart navigation toolbar
        hover_cid (int): Connection ID for hover events
        annot (matplotlib.Annotation): Chart annotation object
        last_stock_data (pandas.DataFrame): Last analyzed dataset for export
        
    GUI Components:
        - Input controls for ticker, period, and SMA window
        - Analysis results text area with scrolling
        - Interactive chart with technical indicators
        - Status bar for operation feedback
        - Navigation buttons and toolbar
    """
    
    def __init__(self, root):
        """
        Initialize the GUI application.
        
        Args:
            root (tk.Tk): The main tkinter root window.
        """
        self.root = root
        self.root.title("PyStock Analyzer - Enhanced")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f0f0')
        
        # Initialize chart interaction attributes
        self.hover_cid = None  # Connection ID for hover events
        self.annot = None      # Annotation object for chart tooltips
        self.last_stock_data = None  # Store last analyzed data for potential export
        
        # Set up the complete GUI layout
        self.setup_gui()
    def setup_gui(self):
        """
        Set up the complete GUI layout and components.
        
        This method creates and configures all GUI elements including:
        - Input controls for stock analysis parameters
        - Results display area with scrolling text
        - Interactive matplotlib chart with navigation toolbar
        - Status bar for user feedback
        - Proper grid layout and responsive resizing
        """
        # Create main container frame with padding
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # =============== INPUT SECTION ===============
        input_frame = ttk.LabelFrame(main_frame, text="Stock Data Input", padding="10")
        input_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)

        # Stock ticker input
        ttk.Label(input_frame, text="Stock Ticker:").grid(row=0, column=0, sticky=tk.W, padx=5)
        self.ticker_var = tk.StringVar(value="AAPL")
        ttk.Entry(input_frame, textvariable=self.ticker_var, width=10).grid(row=0, column=1, padx=5)

        # Time period selection
        ttk.Label(input_frame, text="Time Period:").grid(row=0, column=2, sticky=tk.W, padx=5)
        self.period_var = tk.StringVar(value="6mo")
        period_combo = ttk.Combobox(input_frame, textvariable=self.period_var, 
                                   values=["1mo", "3mo", "6mo", "1y", "2y"], width=8)
        period_combo.grid(row=0, column=3, padx=5)

        # SMA window configuration
        ttk.Label(input_frame, text="SMA Window:").grid(row=0, column=4, sticky=tk.W, padx=5)
        self.sma_var = tk.StringVar(value="10")
        ttk.Entry(input_frame, textvariable=self.sma_var, width=5).grid(row=0, column=5, padx=5)

        # Action buttons
        self.analyze_btn = ttk.Button(input_frame, text="Analyze Stock", 
                                     command=self.analyze_stock)
        self.analyze_btn.grid(row=0, column=6, padx=10)

        self.home_btn = ttk.Button(input_frame, text="Home", command=self.on_home)
        self.home_btn.grid(row=0, column=7, padx=10)
        
        # =============== RESULTS SECTION ===============
        results_frame = ttk.LabelFrame(main_frame, text="Analysis Results", padding="10")
        results_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        # Scrollable text area for detailed analysis results
        self.results_text = scrolledtext.ScrolledText(results_frame, height=15, width=80)
        self.results_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # =============== CHART SECTION ===============
        chart_frame = ttk.LabelFrame(main_frame, text="Price Chart with Technical Indicators", padding="10")
        chart_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        # Create matplotlib figure and canvas
        self.fig, self.ax = plt.subplots(figsize=(12, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, chart_frame)

        # Add navigation toolbar for chart interaction (zoom, pan, save, etc.)
        self.toolbar = NavigationToolbar2Tk(self.canvas, chart_frame)
        self.toolbar.update()

        # Pack canvas to fill available space
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # =============== STATUS SECTION ===============
        self.status_var = tk.StringVar(value="Ready to analyze stocks...")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=5)
        
        # =============== GRID CONFIGURATION ===============
        # Configure responsive resizing behavior
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)  # Results section expandable
        main_frame.rowconfigure(2, weight=2)  # Chart section gets more space
        
        # =============== EVENT BINDINGS ===============
        # Handle window close event properly
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def analyze_stock(self):
        """
        Handle stock analysis request from user interface.
        
        This method initiates the stock analysis process by disabling the analyze
        button to prevent multiple simultaneous requests, updating the status,
        and launching the analysis in a separate thread to prevent GUI freezing
        during data fetching and calculation operations.
        
        The actual analysis is performed in _perform_analysis() method running
        in a background thread to maintain UI responsiveness.
        """
        # Disable button to prevent multiple simultaneous analyses
        self.analyze_btn.config(state='disabled')
        self.status_var.set("Fetching data...")
        
        # Run analysis in separate thread to prevent GUI freezing
        analysis_thread = threading.Thread(target=self._perform_analysis)
        analysis_thread.daemon = True  # Thread will close when main program exits
        analysis_thread.start()
        
    def _perform_analysis(self):
        """
        Perform the complete stock analysis workflow.
        
        This method executes in a background thread and handles:
        1. Input validation and parameter extraction
        2. Stock data fetching from external API
        3. Calculation of technical indicators and analysis metrics
        4. Results display and chart visualization
        5. Error handling and user feedback
        
        The method coordinates all analysis components and ensures the GUI
        is updated safely from the background thread using root.after().
        
        Raises:
            Displays error messages via messagebox for any analysis failures.
        """
        try:
            # Extract and validate user input parameters
            ticker = self.ticker_var.get().strip().upper()
            period = self.period_var.get()
            sma_window = int(self.sma_var.get())
            
            # Validate input parameters
            if not ticker:
                messagebox.showerror("Error", "Please enter a valid ticker symbol")
                return
                
            if sma_window < 1:
                messagebox.showerror("Error", "SMA window must be a positive integer")
                return
            
            # =============== DATA FETCHING ===============
            self.status_var.set(f"Fetching data for {ticker}...")
            stock_data = fetch_stock_data(ticker, period)
            
            if stock_data is None or stock_data.empty:
                messagebox.showerror("Error", f"Failed to fetch data for {ticker}")
                return

            # Store data for potential export functionality
            self.last_stock_data = stock_data.copy()
            
            # =============== CALCULATIONS ===============
            self.status_var.set("Performing technical analysis...")
            
            # Basic calculations
            sma = calculate_sma(stock_data, sma_window)
            runs_data = identify_runs(stock_data)
            returns = calculate_daily_returns(stock_data)
            max_profit = calculate_max_profit(stock_data['Close'].tolist())
            
            # Advanced technical indicators
            rsi = calculate_rsi(stock_data, window=14)
            upper_band, middle_band, lower_band = calculate_bollinger_bands(stock_data, window=20, num_std=2)
            
            # =============== DISPLAY RESULTS ===============
            self._display_results(stock_data, sma, runs_data, returns, max_profit, 
                                sma_window, rsi, upper_band, middle_band, lower_band)
            
            # =============== UPDATE CHART ===============
            self._update_chart(stock_data, sma, sma_window, upper_band, lower_band)
            
            # Update status to show completion
            self.status_var.set(f"Analysis complete for {ticker}!")
            
        except ValueError as e:
            messagebox.showerror("Input Error", f"Invalid input: {str(e)}")
        except Exception as e:
            messagebox.showerror("Analysis Error", f"Analysis failed: {str(e)}")
        finally:
            # Always re-enable the analyze button
            self.analyze_btn.config(state='normal')
            
    def _display_results(self, data, sma, runs_data, returns, max_profit, sma_window, 
                        rsi, upper_band, middle_band, lower_band):
        """
        Format and display comprehensive analysis results.
        
        This method creates a detailed, formatted text report of all analysis
        results including basic statistics, technical indicators, and trading
        insights. The results are displayed in the scrollable text area.
        
        Args:
            data (pandas.DataFrame): Original stock data
            sma (pandas.Series): Simple Moving Average values
            runs_data (dict): Run analysis results from identify_runs()
            returns (pandas.Series): Daily returns data
            max_profit (float): Maximum achievable profit calculation
            sma_window (int): SMA calculation window size
            rsi (pandas.Series): Relative Strength Index values
            upper_band, middle_band, lower_band (pandas.Series): Bollinger Bands data
        """
        # Create comprehensive formatted analysis report
        result_text = f"{'='*60}\n"
        result_text += "ENHANCED STOCK ANALYSIS RESULTS\n"
        result_text += f"{'='*60}\n\n"
        
        # =============== MOVING AVERAGE ANALYSIS ===============
        result_text += f"1. SIMPLE MOVING AVERAGE ({sma_window} days):\n"
        result_text += f"   Latest SMA value: ${sma.iloc[-1]:.2f}\n"
        result_text += f"   Current price vs SMA: "
        if data['Close'].iloc[-1] > sma.iloc[-1]:
            result_text += "Above (Bullish signal)\n\n"
        else:
            result_text += "Below (Bearish signal)\n\n"
        
        # =============== TREND ANALYSIS ===============
        result_text += f"2. PRICE RUN ANALYSIS:\n"
        result_text += f"   Total upward days: {runs_data['total_up_days']}\n"
        result_text += f"   Total downward days: {runs_data['total_down_days']}\n"
        result_text += f"   Longest upward streak: {runs_data['longest_up_streak']} days\n"
        result_text += f"   Longest downward streak: {runs_data['longest_down_streak']} days\n"
        
        # Calculate trend bias
        total_directional_days = runs_data['total_up_days'] + runs_data['total_down_days']
        if total_directional_days > 0:
            up_bias = (runs_data['total_up_days'] / total_directional_days) * 100
            result_text += f"   Upward bias: {up_bias:.1f}%\n\n"
        else:
            result_text += "   No directional bias data available\n\n"
        
        # =============== VOLATILITY ANALYSIS ===============
        result_text += f"3. DAILY RETURNS ANALYSIS:\n"
        result_text += f"   Average daily return: {returns.mean():.4f} ({returns.mean()*100:.2f}%)\n"
        result_text += f"   Return volatility (std dev): {returns.std():.4f} ({returns.std()*100:.2f}%)\n"
        result_text += f"   Best single day: {returns.max():.4f} ({returns.max()*100:.2f}%)\n"
        result_text += f"   Worst single day: {returns.min():.4f} ({returns.min()*100:.2f}%)\n\n"
        
        # =============== PROFIT ANALYSIS ===============
        result_text += f"4. MAXIMUM PROFIT ANALYSIS:\n"
        result_text += f"   Maximum achievable profit: ${max_profit:.2f}\n"
        result_text += f"   (Perfect timing with multiple transactions)\n"
        if len(data) > 0:
            profit_percentage = (max_profit / data['Close'].iloc[0]) * 100
            result_text += f"   Profit percentage: {profit_percentage:.2f}%\n\n"
        
        # =============== RSI ANALYSIS ===============
        result_text += f"5. RELATIVE STRENGTH INDEX (RSI - 14 day):\n"
        current_rsi = rsi.iloc[-1]
        result_text += f"   Current RSI: {current_rsi:.2f}\n"
        
        # RSI interpretation
        if current_rsi > 70:
            rsi_status = "Overbought (>70) - Potential sell signal"
        elif current_rsi < 30:
            rsi_status = "Oversold (<30) - Potential buy signal"
        else:
            rsi_status = "Neutral (30-70) - No strong signal"
        result_text += f"   Interpretation: {rsi_status}\n"
        result_text += f"   RSI Range: {rsi.min():.2f} to {rsi.max():.2f}\n\n"
        
        # =============== BOLLINGER BANDS ANALYSIS ===============
        result_text += f"6. BOLLINGER BANDS ANALYSIS (20-day, 2σ):\n"
        current_price = data['Close'].iloc[-1]
        current_upper = upper_band.iloc[-1]
        current_lower = lower_band.iloc[-1]
        current_middle = middle_band.iloc[-1]
        
        # Band position analysis
        if current_price > current_upper:
            band_status = "Above Upper Band - Potentially Overbought"
        elif current_price < current_lower:
            band_status = "Below Lower Band - Potentially Oversold"
        else:
            band_status = "Within Bands - Normal trading range"
        result_text += f"   Current Position: {band_status}\n"
        
        # Volatility measurement
        band_width = (current_upper - current_lower) / current_middle * 100
        result_text += f"   Current Band Width: {band_width:.2f}%\n"
        result_text += f"   (Higher width = More volatile period)\n"
        result_text += f"   Upper Band: ${current_upper:.2f}\n"
        result_text += f"   Middle Band: ${current_middle:.2f}\n"
        result_text += f"   Lower Band: ${current_lower:.2f}\n\n"
        
        # =============== DATA SUMMARY ===============
        result_text += f"7. DATA SUMMARY:\n"
        result_text += f"   Analysis Period: {data.index[0].date()} to {data.index[-1].date()}\n"
        result_text += f"   Total trading days: {len(data)}\n"
        result_text += f"   Starting price: ${data['Close'].iloc[0]:.2f}\n"
        result_text += f"   Ending price: ${data['Close'].iloc[-1]:.2f}\n"
        result_text += f"   Highest price: ${data['High'].max():.2f}\n"
        result_text += f"   Lowest price: ${data['Low'].min():.2f}\n"
        
        # Overall performance calculation
        total_change = ((data['Close'].iloc[-1] / data['Close'].iloc[0]) - 1) * 100
        result_text += f"   Total period change: {total_change:.2f}%\n"
        
        # Annualized return estimation (rough)
        days_in_period = len(data)
        if days_in_period > 30:  # Only calculate if we have enough data
            annual_return = (((data['Close'].iloc[-1] / data['Close'].iloc[0]) ** (252/days_in_period)) - 1) * 100
            result_text += f"   Annualized return estimate: {annual_return:.2f}%\n"
        
        # Update GUI text area in thread-safe manner
        self.root.after(0, lambda: self._update_results_text(result_text))
        
    def _update_results_text(self, text):
        """
        Update the results text area in a thread-safe manner.
        
        This method safely updates the GUI text area from any thread by clearing
        the existing content and inserting the new analysis results.
        
        Args:
            text (str): Formatted analysis results text to display.
        """
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(1.0, text)
        
    def _update_chart(self, data, sma, sma_window, upper_band, lower_band):
        """
        Update the matplotlib chart with comprehensive technical analysis visualization.
        
        This method creates an interactive chart displaying stock price data with
        technical indicators, trend highlighting, and hover tooltips. It includes:
        - Stock closing price line
        - Simple Moving Average overlay
        - Bollinger Bands (upper and lower)
        - Run period highlighting (upward/downward trends)
        - Interactive hover annotations
        
        Args:
            data (pandas.DataFrame): Stock price data with datetime index
            sma (pandas.Series): Simple Moving Average values
            sma_window (int): SMA calculation window for labeling
            upper_band (pandas.Series): Upper Bollinger Band values
            lower_band (pandas.Series): Lower Bollinger Band values
        """
        # =============== CLEANUP PREVIOUS CHART ===============
        # Disconnect previous hover event if exists to prevent memory leaks
        if self.hover_cid is not None:
            self.fig.canvas.mpl_disconnect(self.hover_cid)
            self.hover_cid = None
        
        # Clear the axis and reset annotation object
        self.ax.clear()
        self.annot = None  # Reset annotation object

        # =============== TREND RUN HIGHLIGHTING ===============
        # Get run periods for background highlighting
        run_periods = identify_run_periods(data)
        
        # Track labeling to avoid duplicate legend entries
        upward_run_labeled = False
        downward_run_labeled = False
        
        # Add background highlighting for significant trend runs
        for run in run_periods:
            start_date = run['start_date']
            end_date = run['end_date']
            direction = run['direction']
            length = run['length']
            
            # Only highlight runs of 2 or more days to avoid visual clutter
            if length >= 2:
                if direction == 1:  # Upward run
                    label = 'Upward Run' if not upward_run_labeled else ""
                    self.ax.axvspan(start_date, end_date, alpha=0.2, color='green', label=label)
                    upward_run_labeled = True
                elif direction == -1:  # Downward run
                    label = 'Downward Run' if not downward_run_labeled else ""
                    self.ax.axvspan(start_date, end_date, alpha=0.2, color='red', label=label)
                    downward_run_labeled = True

        # =============== PRICE AND INDICATOR PLOTTING ===============
        # Plot main price line
        line_close, = self.ax.plot(data.index, data['Close'], 
                                  label='Closing Price', color='blue', alpha=0.7, linewidth=1.5)
        
        # Plot Simple Moving Average
        line_sma, = self.ax.plot(data.index, sma, 
                                label=f'SMA ({sma_window} days)', color='red', linewidth=2)
        
        # Plot Bollinger Bands
        line_upper, = self.ax.plot(data.index, upper_band, 
                                  label='Upper Bollinger Band', color='green', 
                                  linestyle='--', alpha=0.7)
        line_lower, = self.ax.plot(data.index, lower_band, 
                                  label='Lower Bollinger Band', color='red', 
                                  linestyle='--', alpha=0.7)
        
        # Fill area between Bollinger Bands
        self.ax.fill_between(data.index, lower_band, upper_band, 
                            alpha=0.1, color='gray', label='Bollinger Band Area')

        # =============== CHART FORMATTING ===============
        self.ax.set_title(f'{self.ticker_var.get()} Price with Technical Indicators and Run Highlighting', 
                         fontsize=14, fontweight='bold')
        self.ax.set_xlabel('Date', fontweight='bold')
        self.ax.set_ylabel('Price ($)', fontweight='bold')
        self.ax.legend(fontsize=8, loc="best", framealpha=0.8)
        self.ax.grid(True, alpha=0.3)
        self.ax.tick_params(axis='x', rotation=45)

        # =============== INTERACTIVE HOVER FUNCTIONALITY ===============
        # Create annotation object for hover tooltips
        self.annot = self.ax.annotate(
            "", xy=(0,0), xytext=(20,20), textcoords="offset points",
            bbox=dict(boxstyle="round", fc="w"), arrowprops=dict(arrowstyle="->")
        )
        self.annot.set_visible(False)

        def update_annot(line, ind):
            """Update annotation content based on hover position."""
            x, y = line.get_data()
            self.annot.xy = (x[ind["ind"][0]], y[ind["ind"][0]])
            text = f"{line.get_label()}\nDate: {x[ind['ind'][0]].date()}\nPrice: ${y[ind['ind'][0]]:.2f}"
            self.annot.set_text(text)
            self.annot.get_bbox_patch().set_alpha(0.8)

        def hover(event):
            """Handle mouse hover events for interactive tooltips."""
            if self.annot is None:  # Safety check
                return
            vis = self.annot.get_visible()
            if event.inaxes == self.ax:
                # Check all plotted lines for hover detection
                for line in [line_close, line_sma, line_upper, line_lower]:
                    cont, ind = line.contains(event)
                    if cont:
                        update_annot(line, ind)
                        self.annot.set_visible(True)
                        self.canvas.draw_idle()
                        return
            # Hide annotation if not hovering over any line
            if vis:
                self.annot.set_visible(False)
                self.canvas.draw_idle()

        # Connect hover event handler
        self.hover_cid = self.fig.canvas.mpl_connect("motion_notify_event", hover)

        # =============== FINALIZE CHART ===============
        self.fig.tight_layout()
        self.canvas.draw()

    def on_home(self):
        """
        Handle Home button click event.
        
        This method provides a way to exit the GUI and return to the main menu.
        It forcefully terminates the application and prompts the user to restart
        the main menu from the terminal.
        
        Note:
            Uses os._exit(0) for immediate termination, which is necessary
            when dealing with matplotlib and threading in tkinter applications.
        """
        print("\nGUI closed. Press Enter in the terminal to rerun the main menu.")
        import os
        os._exit(0)

    def on_closing(self):
        """
        Handle window close event (X button).
        
        This method is called when the user clicks the window close button.
        It ensures proper cleanup and provides feedback to the user about
        how to restart the application.
        
        Note:
            Uses os._exit(0) for immediate termination to prevent hanging
            threads and ensure complete application shutdown.
        """
        print("\nGUI closed. Press Enter in the terminal to rerun the main menu.")
        import os
        os._exit(0)


def main():
    """
    Main function to start the GUI application.
    
    This function creates the main tkinter window and initializes the
    StockAnalyzerGUI application. It serves as the entry point when
    this module is run directly.
    
    The function sets up the complete GUI and starts the tkinter
    event loop to handle user interactions.
    """
    root = tk.Tk()
    app = StockAnalyzerGUI(root)
    root.mainloop()


# Entry point for direct script execution
if __name__ == "__main__":
    """
    Entry point for direct script execution.
    
    When this module is run directly (e.g., python gui.py), it starts
    the GUI application by calling the main() function.
    """
    main()