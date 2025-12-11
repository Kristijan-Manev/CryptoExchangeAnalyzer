import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_percentage_error
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.optimizers import Adam
import math

class LSTMPredictor:
    def __init__(self, lookback=30):
        self.lookback = lookback
        self.scaler = MinMaxScaler(feature_range=(0, 1))

    def _create_sequences(self, data):
        X, y = [], []
        for i in range(self.lookback, len(data)):
            X.append(data[i - self.lookback:i])  # multivariate sequence
            y.append(data[i, 3])  # predicting 'Close' price (4th column)
        return np.array(X), np.array(y)

    def train_and_predict(self, historical_data):
        """Train LSTM on OHLCV data and predict future closing prices"""
        df = pd.DataFrame(historical_data)

        # Ensure columns exist and convert to numeric
        for col in ['open', 'high', 'low', 'close', 'volume']:
            df[col] = pd.to_numeric(df[col], errors='coerce')

        df = df.dropna(subset=['open', 'high', 'low', 'close', 'volume'])

        # Use all OHLCV as features
        dataset = df[['open', 'high', 'low', 'close', 'volume']].values
        scaled = self.scaler.fit_transform(dataset)

        # Train/test split
        train_size = int(len(scaled) * 0.7)
        train, test = scaled[:train_size], scaled[train_size:]

        X_train, y_train = self._create_sequences(train)
        X_test, y_test = self._create_sequences(test)

        X_train = X_train.reshape((X_train.shape[0], X_train.shape[1], X_train.shape[2]))
        X_test = X_test.reshape((X_test.shape[0], X_test.shape[1], X_test.shape[2]))

        # Build LSTM model
        model = Sequential([
            LSTM(50, return_sequences=True, input_shape=(self.lookback, X_train.shape[2])),
            LSTM(50, return_sequences=False),
            Dense(25),
            Dense(1)
        ])
        model.compile(optimizer=Adam(0.001), loss='mean_squared_error')
        model.fit(X_train, y_train, epochs=20, batch_size=16, verbose=0)

        # Predict on test
        predictions = model.predict(X_test)
        # inverse scale only the 'Close' column
        close_scaler = MinMaxScaler(feature_range=(0, 1))
        close_scaler.min_, close_scaler.scale_ = self.scaler.min_[3], self.scaler.scale_[3]
        predictions = close_scaler.inverse_transform(predictions.reshape(-1, 1))
        real = close_scaler.inverse_transform(y_test.reshape(-1, 1))

        # Metrics
        rmse = math.sqrt(mean_squared_error(real, predictions))
        mape = mean_absolute_percentage_error(real, predictions)
        r2 = r2_score(real, predictions)

        # Future forecast (next 7 days)
        last_sequence = scaled[-self.lookback:]
        future_preds = []
        seq = last_sequence.copy()
        for _ in range(7):
            pred = model.predict(seq.reshape(1, self.lookback, X_train.shape[2]), verbose=0)
            future_preds.append(pred[0, 0])

            # Shift and append new features; for simplicity, keep other features as last row
            new_row = seq[-1].copy()
            new_row[3] = pred  # update 'Close'
            seq = np.vstack([seq[1:], new_row])

        future_prices = close_scaler.inverse_transform(np.array(future_preds).reshape(-1, 1)).flatten()

        return {
            "rmse": round(rmse, 3),
            "mape": round(mape, 3),
            "r2": round(r2, 3),
            "future_predictions": future_prices.tolist()
        }
