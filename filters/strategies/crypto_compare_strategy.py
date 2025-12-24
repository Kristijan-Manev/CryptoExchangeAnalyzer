# crypto_compare_strategy.py
import requests
import logging
import time
from datetime import datetime
from config import RATE_LIMIT_DELAY
from filters.strategies.data_fetch_strategy import DataFetchStrategy


class CryptoCompareStrategy(DataFetchStrategy):
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def download_historical_data(self, symbol, last_date):
        """Download long-term historical data from CryptoCompare"""
        try:
            url = "https://min-api.cryptocompare.com/data/v2/histoday"
            params = {"fsym": symbol.upper(), "tsym": "USD", "limit": 2000}

            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()

            if data.get("Response") != "Success":
                self.logger.warning(f"No historical data for {symbol}")
                return []

            formatted = []
            for record in data["Data"]["Data"]:
                date = datetime.utcfromtimestamp(record["time"]).strftime("%Y-%m-%d")
                if last_date and date <= last_date:
                    continue
                formatted.append({
                    "date": date,
                    "open": record["open"],
                    "high": record["high"],
                    "low": record["low"],
                    "close": record["close"],
                    "volume": record["volumefrom"]
                })

            time.sleep(RATE_LIMIT_DELAY)
            return formatted

        except Exception as e:
            self.logger.error(f"Error fetching CryptoCompare data for {symbol}: {e}")
            return []

    def download_current_metrics(self, symbol):
        """Download current market data (CryptoCompare)"""
        try:
            url = "https://min-api.cryptocompare.com/data/pricemultifull"
            params = {"fsyms": symbol.upper(), "tsyms": "USD"}
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()

            data = response.json()
            coin_info = data["RAW"][symbol.upper()]["USD"]

            return {
                "date": datetime.now().strftime("%Y-%m-%d"),
                "price": coin_info.get("PRICE"),
                "volume_24h": coin_info.get("TOTALVOLUME24H"),
                "high_24h": coin_info.get("HIGH24HOUR"),
                "low_24h": coin_info.get("LOW24HOUR"),
                "market_cap": coin_info.get("MKTCAP")
            }

        except Exception as e:
            self.logger.error(f"Error fetching current metrics for {symbol}: {e}")
            return None
