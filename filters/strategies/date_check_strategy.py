from abc import ABC, abstractmethod


class DateCheckStrategy(ABC):
    @abstractmethod
    def needs_update(self, last_date: str) -> bool:
        """Return True if the data should be updated based on last_date"""
        pass
