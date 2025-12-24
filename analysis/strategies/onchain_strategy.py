from analysis.strategies.base import AnalysisStrategy


class OnChainSentimentStrategy(AnalysisStrategy):
    def __init__(self, analyzer, logger):
        self.analyzer = analyzer
        self.logger = logger

    def analyze(self, crypto_id):
        try:
            result = self.analyzer.analyze(crypto_id)
            return result
        except Exception as e:
            self.logger.error(f"OnChain/Sentiment analysis error for {crypto_id}: {e}")
            return {'error': str(e)}