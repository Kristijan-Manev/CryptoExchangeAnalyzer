from analysis.strategies.base import AnalysisStrategy


class LSTMAnalysisStrategy(AnalysisStrategy):
    def __init__(self, predictor_class, data_provider, logger, lookback=30):
        self.predictor_class = predictor_class
        self.data_provider = data_provider
        self.logger = logger
        self.lookback = lookback

    def analyze(self, crypto_id):
        historical_data = self.data_provider._get_crypto_historical_data(crypto_id)
        if not historical_data or len(historical_data) < 100:
            self.logger.warning(f"Not enough data for LSTM analysis of {crypto_id}")
            return {'error': 'Not enough data to train LSTM'}

        predictor = self.predictor_class(lookback=self.lookback)
        results = predictor.train_and_predict(historical_data)

        return {
            'crypto_id': crypto_id,
            'metrics': {
                'RMSE': results['rmse'],
                'MAPE': results['mape'],
                'R2': results['r2']
            },
            'future_prices': results['future_predictions']
        }
