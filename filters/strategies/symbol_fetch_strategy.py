from abc import ABC, abstractmethod


class SymbolFetchStrategy(ABC):
    """Interface for fetching cryptocurrency symbol data."""

    @abstractmethod
    def fetch_symbols(self):
        """Return a list of cryptocurrency symbol data from a data source."""
        pass
