from analysis.strategies.base import AnalysisStrategy


class TechnicalAnalysisStrategy(AnalysisStrategy):
    """Strategy for performing technical analysis on a cryptocurrency"""
    def __init__(self, analyzer, data_provider, logger):
        self.analyzer = analyzer            # Your TechnicalAnalyzer instance
        self.data_provider = data_provider  # CryptoExchangeProcessor for _get_crypto_historical_data and _get_indicators_summary
        self.logger = logger

    def analyze(self, crypto_id, time_frame='daily'):
        import pandas as pd

        # 1. Get historical data
        df_data = self.data_provider._get_crypto_historical_data(crypto_id)
        if not df_data or len(df_data) < 50:
            self.logger.warning(f"Insufficient data for technical analysis of {crypto_id}")
            return None

        df = pd.DataFrame(df_data)

        # 2. Ensure required columns exist
        required_cols = ['date', 'open', 'high', 'low', 'close']
        for col in required_cols:
            if col not in df.columns:
                self.logger.error(f"Missing required column {col} for {crypto_id}")
                return None

        # 3. Clean data
        df = df[(df[['open', 'high', 'low', 'close']] != 0).any(axis=1)]
        df = df.dropna(subset=['open', 'high', 'low', 'close'])

        # 4. Perform indicators calculation
        analysis_df = self.analyzer.calculate_indicators(df, time_frame)
        if analysis_df is None or analysis_df.empty:
            self.logger.error(f"Technical analysis failed for {crypto_id}")
            return None

        # 5. Convert to dict for template
        analysis_dict = analysis_df.to_dict('records')
        summary = self.analyzer.get_analysis_summary(analysis_df)
        indicators_summary = self.data_provider._get_indicators_summary(analysis_df)

        return {
            'crypto_id': crypto_id,
            'time_frame': time_frame,
            'data_points': len(analysis_dict),
            'analysis_data': analysis_dict[-100:],  # last 100 points
            'summary': summary,
            'indicators_summary': indicators_summary
        }
