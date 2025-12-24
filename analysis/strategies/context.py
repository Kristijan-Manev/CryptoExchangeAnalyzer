class AnalysisContext:
    def __init__(self, strategy):
        self.strategy = strategy

    def execute(self, crypto_id, **kwargs):
        return self.strategy.analyze(crypto_id, **kwargs)