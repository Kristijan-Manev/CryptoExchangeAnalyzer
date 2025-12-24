import logging
import time
from config import RATE_LIMIT_DELAY


class DataFillFilter:
    def __init__(self, csv_manager, fetch_strategy):
        """
        :param csv_manager: object responsible for saving data
        :param fetch_strategy: instance of a class implementing DataFetchStrategy
        """
        self.csv_manager = csv_manager
        self.fetch_strategy = fetch_strategy  # the Strategy pattern here
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

                    # Use the injected strategy instead of local methods
                    historical_data = self.fetch_strategy.download_historical_data(
                        crypto['symbol'], last_date
                    )

                    current_metrics = self.fetch_strategy.download_current_metrics(
                        crypto['symbol']
                    )

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
