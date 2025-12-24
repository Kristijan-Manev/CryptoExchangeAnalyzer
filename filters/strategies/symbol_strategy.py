import requests
import logging
import time
from config import COINGECKO_API_URL, MAX_CRYPTOCURRENCIES
from filters.strategies.symbol_fetch_strategy import SymbolFetchStrategy


class SymbolStrategy(SymbolFetchStrategy):
    """Concrete strategy that fetches symbol data from the CoinGecko API."""

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def fetch_symbols(self):
        """Fetch top cryptocurrencies from CoinGecko with pagination."""
        all_symbols = []
        page = 1
        per_page = 250  # Max per CoinGecko API

        self.logger.info("Fetching cryptocurrency symbols from CoinGecko")

        while len(all_symbols) < MAX_CRYPTOCURRENCIES:
            url = f"{COINGECKO_API_URL}/coins/markets"
            params = {
                'vs_currency': 'usd',
                'order': 'market_cap_desc',
                'per_page': per_page,
                'page': page,
                'sparkline': False
            }

            try:
                response = requests.get(url, params=params, timeout=30)
                response.raise_for_status()
                page_symbols = response.json()

                if not page_symbols:
                    break

                all_symbols.extend(page_symbols)
                page += 1

                time.sleep(1)  # avoid hitting rate limits

            except Exception as e:
                self.logger.error(f"Error fetching symbols from CoinGecko (page {page}): {e}")
                break

        self.logger.info(f"Fetched {len(all_symbols)} total symbols from CoinGecko.")
        return all_symbols[:MAX_CRYPTOCURRENCIES * 2]  # get extra for filtering
