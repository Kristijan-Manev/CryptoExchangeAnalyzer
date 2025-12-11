import random
from textblob import TextBlob

class OnChainSentimentAnalyzer:
    def __init__(self):
        pass

    def analyze(self, crypto_id):
        # Simulated on-chain data (you can later connect to APIs like Glassnode)
        onchain_metrics = {
            "active_addresses": random.randint(500_000, 1_000_000),
            "transactions": random.randint(200_000, 500_000),
            "exchange_inflows": random.uniform(50, 200),
            "exchange_outflows": random.uniform(50, 200),
            "whale_transactions": random.randint(10, 50),
            "hash_rate": random.uniform(100, 300),
            "tvl": random.uniform(10_000_000_000, 20_000_000_000),
            "nvt_ratio": round(random.uniform(60, 120), 2),
            "mvrv_ratio": round(random.uniform(1.0, 3.0), 2),
        }

        # Dummy social posts or headlines for sentiment analysis
        sample_posts = [
            "Bitcoin price is expected to surge this week as whales accumulate.",
            "Investors are losing confidence in the market.",
            "The new update to the Ethereum network boosts security.",
            "Fear is dominating the crypto market today.",
            "Institutional investors are showing strong interest again."
        ]

        # Analyze sentiment with TextBlob (can also use VADER or BERT)
        sentiments = [TextBlob(post).sentiment.polarity for post in sample_posts]
        avg_sentiment = sum(sentiments) / len(sentiments)

        # Sentiment interpretation
        sentiment_label = (
            "Positive" if avg_sentiment > 0.1 else
            "Negative" if avg_sentiment < -0.1 else
            "Neutral"
        )

        result = {
            "crypto_id": crypto_id,
            "onchain_metrics": onchain_metrics,
            "average_sentiment": round(avg_sentiment, 3),
            "sentiment_label": sentiment_label,
        }

        return result
