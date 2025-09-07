import json
import os
from typing import Dict, Any

class ConfigManager:
    """
    Manages application configuration with file persistence
    """
    
    def __init__(self, config_file: str = "config.json"):
        self.config_file = config_file
        self.default_config = {
            "default_ticker": "AAPL",
            "default_period": "6mo",
            "default_sma_window": 10,
            "theme": "light",
            "auto_refresh": False,
            "refresh_interval": 300,
            "chart_style": "default",
            "last_used_tickers": ["AAPL", "TSLA", "MSFT"],
            "window_size": {"width": 1000, "height": 700}
        }
        self.config = self.load_config()
    
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from file or use defaults"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    loaded_config = json.load(f)
                    # Merge with defaults to ensure all keys exist
                    return {**self.default_config, **loaded_config}
            except (json.JSONDecodeError, IOError):
                return self.default_config.copy()
        return self.default_config.copy()
    
    def save_config(self) -> bool:
        """Save configuration to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=4)
            return True
        except IOError:
            return False
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        return self.config.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """Set configuration value"""
        self.config[key] = value
        self.save_config()
    
    def update_last_used_tickers(self, ticker: str) -> None:
        """Update last used tickers list"""
        if ticker in self.config["last_used_tickers"]:
            self.config["last_used_tickers"].remove(ticker)
        self.config["last_used_tickers"].insert(0, ticker)
        # Keep only last 5 tickers
        self.config["last_used_tickers"] = self.config["last_used_tickers"][:5]
        self.save_config()

# Create a global instance
app_config = ConfigManager()

# This allows: from config import app_config
# Instead of: from config import config