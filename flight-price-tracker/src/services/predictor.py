class PricePredictor:
    def predict(self, history):
        if not history or len(history) < 3:
            return None, "Not enough data"

        last_prices = history[-3:]

        diff1 = last_prices[1] - last_prices[0]
        diff2 = last_prices[2] - last_prices[1]

        avg_change = (diff1 + diff2) / 2

        predicted_price = int(last_prices[-1] + avg_change)

        # Clamp prediction (avoid unrealistic values)
        predicted_price = max(int(last_prices[-1] * 0.85), predicted_price)
        predicted_price = min(int(last_prices[-1] * 1.25), predicted_price)

        # Trend detection
        if avg_change > 150:
            trend = "📈 Likely to Increase"
        elif avg_change < -150:
            trend = "📉 Likely to Drop"
        else:
            trend = "➖ Stable"

        return predicted_price, trend