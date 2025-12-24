import pandas as pd
import os
import logging
from datetime import datetime
from config import SYMBOLS_DIR, HISTORICAL_DIR, METRICS_DIR, CSV_ENCODING, CSV_DELIMITER


class CSVManager:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._ensure_directories()

    def _ensure_directories(self):
        for dir_path in [SYMBOLS_DIR, HISTORICAL_DIR, METRICS_DIR]:
            os.makedirs(dir_path, exist_ok=True)

    def _save_csv(self, data, filename, key='date'):
        """Generic CSV save: append, deduplicate, sort."""
        if not data:
            return None

        df_new = pd.DataFrame(data)

        if os.path.exists(filename):
            try:
                df_existing = pd.read_csv(filename, encoding=CSV_ENCODING)
                df_combined = pd.concat([df_existing, df_new]).drop_duplicates(subset=[key], keep='last')
                df_combined = df_combined.sort_values(key)
                df_combined.to_csv(filename, index=False, encoding=CSV_ENCODING)
            except Exception as e:
                self.logger.error(f"Error appending CSV {filename}: {e}")
                df_new.to_csv(filename, index=False, encoding=CSV_ENCODING)
        else:
            df_new.to_csv(filename, index=False, encoding=CSV_ENCODING)

        self.logger.info(f"Saved {len(df_new)} records to {filename}")
        return filename

    # ---- Symbols ----
    def save_symbols(self, symbols):
        filename = os.path.join(SYMBOLS_DIR, f"crypto_symbols_{datetime.now():%Y%m%d_%H%M%S}.csv")
        return self._save_csv(symbols, filename)

    def get_last_symbols_file(self):
        try:
            files = [f for f in os.listdir(SYMBOLS_DIR) if f.endswith('.csv')]
            if not files:
                return None
            latest_file = max(files)
            return os.path.join(SYMBOLS_DIR, latest_file)
        except Exception as e:
            self.logger.error(f"Error getting latest symbols file: {e}")
            return None

    def load_symbols(self):
        file = self.get_last_symbols_file()
        if not file:
            return []
        try:
            df = pd.read_csv(file, encoding=CSV_ENCODING)
            return df.to_dict('records')
        except Exception as e:
            self.logger.error(f"Error loading symbols: {e}")
            return []

    # ---- Historical Data ----
    def save_historical_data(self, crypto_id, data):
        filename = os.path.join(HISTORICAL_DIR, f"{crypto_id}_historical.csv")
        return self._save_csv(data, filename, key='date')

    def get_last_historical_date(self, crypto_id):
        filename = os.path.join(HISTORICAL_DIR, f"{crypto_id}_historical.csv")
        if not os.path.exists(filename):
            return None
        try:
            df = pd.read_csv(filename, encoding=CSV_ENCODING)
            return df['date'].max() if not df.empty else None
        except Exception as e:
            self.logger.error(f"Error reading last historical date for {crypto_id}: {e}")
            return None

    def crypto_historical_exists(self, crypto_id):
        return os.path.exists(os.path.join(HISTORICAL_DIR, f"{crypto_id}_historical.csv"))

    # ---- Metrics ----
    def save_daily_metrics(self, crypto_id, data):
        filename = os.path.join(METRICS_DIR, f"{crypto_id}_metrics.csv")
        # Convert dict to list for consistency
        if isinstance(data, dict):
            data = [data]
        return self._save_csv(data, filename, key='date')
