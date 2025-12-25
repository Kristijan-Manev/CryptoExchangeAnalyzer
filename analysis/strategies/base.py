class AnalysisStrategy:
    """Generic interface for any analysis strategy"""

    def analyze(self, crypto_id, **kwargs):
        raise NotImplementedError("Subclasses must implement analyze()")
