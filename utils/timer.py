import time
import logging
from contextlib import contextmanager


# Strategy for logging
class LoggerStrategy:
    def log(self, message: str):
        raise NotImplementedError


class ConsoleLogger(LoggerStrategy):
    def log(self, message: str):
        print(message)


class FileLogger(LoggerStrategy):
    def __init__(self, filename="performance.log"):
        self.logger = logging.getLogger(__name__)
        handler = logging.FileHandler(filename)
        formatter = logging.Formatter('%(asctime)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    def log(self, message: str):
        self.logger.info(message)


# Singleton PerformanceTimer
class PerformanceTimer:
    _instance = None

    def __new__(cls, logger_strategy: LoggerStrategy = None):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.logger_strategy = logger_strategy or ConsoleLogger()
        return cls._instance

    @contextmanager
    def measure_time(self, operation_name="Operation"):
        start_time = time.time()
        self.logger_strategy.log(f"Starting {operation_name}...")

        try:
            yield
        finally:
            elapsed_time = time.time() - start_time
            self.logger_strategy.log(f"{operation_name} completed in {elapsed_time:.2f} seconds")


# Example usage:
if __name__ == "__main__":
    timer = PerformanceTimer(FileLogger())
    with timer.measure_time("Sample Task"):
        time.sleep(1.5)
