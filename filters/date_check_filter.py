import logging


class DateCheckFilter:
    def __init__(self, csv_manager, date_check_strategy):
        self.csv_manager = csv_manager
        self.date_check_strategy = date_check_strategy
        self.logger = logging.getLogger(__name__)

    def process(self, cryptocurrencies):
        """Filter 2: Check last date of available data for each cryptocurrency"""
        self.logger.info("Starting date check filter")

        crypto_date_info = []

        for crypto in cryptocurrencies:
            crypto_id = crypto['id']

            # Check historical data for this crypto
            last_date = self.csv_manager.get_last_historical_date(crypto_id)

            # Use the strategy
            needs_update = self.date_check_strategy.needs_update(last_date)

            crypto_date_info.append({
                'crypto': crypto,
                'last_date': last_date,
                'needs_update': needs_update
            })

        # Log statistics
        needs_update_count = len([c for c in crypto_date_info if c['needs_update']])
        self.logger.info(f"Date check completed: {needs_update_count}/{len(crypto_date_info)} need updates")

        return crypto_date_info
