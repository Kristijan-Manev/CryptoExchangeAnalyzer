class AnalysisStrategy:
    """Generic interface for any analysis strategy"""
    def analyze(self, crypto_id):
        raise NotImplementedError("Subclasses must implement this method")