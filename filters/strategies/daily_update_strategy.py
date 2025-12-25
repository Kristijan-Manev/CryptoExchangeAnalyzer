from datetime import datetime
import logging
from filters.strategies.date_check_strategy import DateCheckStrategy


class DailyUpdateStrategy(DateCheckStrategy):
    """Concrete strategy for checking if crypto data needs daily updates"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def needs_update(self, last_date: str) -> bool:
        if not last_date:
            return True

        try:
            last_date_dt = datetime.strptime(last_date, '%Y-%m-%d')
            current_date = datetime.now()
            difference = (current_date - last_date_dt).days
            return difference > 1
        except Exception as e:
            self.logger.error(f"Error parsing date '{last_date}': {e}")
            return True
