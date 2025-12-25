from abc import ABC, abstractmethod


class DataFetchStrategy(ABC):
    @abstractmethod
    def download_historical_data(self, symbol, last_date):
        pass

    @abstractmethod
    def download_current_metrics(self, symbol):
        pass
