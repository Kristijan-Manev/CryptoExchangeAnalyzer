import requests
import time
import logging
from datetime import datetime
from config import RATE_LIMIT_DELAY

class DataFillFilter:
    def __init__(self, csv_manager):
        self.csv_manager = csv_manager
        self.logger = logging.getLogger(__name__)

    def process(self, crypto_date_info):
        """Filter 3: Fill missing data for each cryptocurrency"""
        self.logger.info("Starting data fill filter")

        processed_count = 0
        success_count = 0

        for crypto_info in crypto_date_info:
            if crypto_info['needs_update']:
                crypto = crypto_info['crypto']
                last_date = crypto_info['last_date']

                try:
                    self.logger.info(f"Processing {crypto['id']} - {crypto['name']}")

                    # Download historical data (CryptoCompare)
                    historical_data = self._download_historical_data(crypto['symbol'], last_date)

                    # Download current metrics (CryptoCompare)
                    current_metrics = self._download_current_metrics(crypto['symbol'])

                    # Save results
                    if historical_data:
                        self.csv_manager.save_historical_data(crypto['id'], historical_data)
                        self.logger.info(f"Saved {len(historical_data)} records for {crypto['id']}")

                    if current_metrics:
                        self.csv_manager.save_daily_metrics(crypto['id'], current_metrics)

                    success_count += 1

                except Exception as e:
                    self.logger.error(f"Error processing {crypto['id']}: {e}")

                processed_count += 1
                time.sleep(RATE_LIMIT_DELAY)

        self.logger.info(f"Data fill completed: {success_count} successful")
        return {'processed_count': processed_count, 'success_count': success_count}

    # ---- HISTORICAL DATA ----
    def _download_historical_data(self, symbol, last_date):
        """Download long-term historical data from CryptoCompare"""
        try:
            url = f"https://min-api.cryptocompare.com/data/v2/histoday"
            params = {
                "fsym": symbol.upper(),
                "tsym": "USD",
                "limit": 3500
            }

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

            return formatted

        except Exception as e:
            self.logger.error(f"Error fetching CryptoCompare data for {symbol}: {e}")
            return []

    # ---- CURRENT METRICS ----
    def _download_current_metrics(self, symbol):
        """Download current market data (CryptoCompare)"""
        try:
            url = f"https://min-api.cryptocompare.com/data/pricemultifull"
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
