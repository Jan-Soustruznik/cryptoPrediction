from utils.logging_utils import log_change


# Decision-making function
def make_decision(df, predicted_price):
    # Fetch the last N close prices for trend analysis
    N = 5
    last_prices = df['close'].iloc[-N:]
    
    # Check if all previous N prices were decreasing or increasing
    if all(last_prices.diff().dropna() < 0) and predicted_price > last_prices.iloc[-1]:
        decision = "BUY"
        log_change(f"Decision: {decision}. Trend: Downward. Predicted price: {predicted_price:.4f} > Last price: {last_prices.iloc[-1]:.4f}")
    elif all(last_prices.diff().dropna() > 0) and predicted_price < last_prices.iloc[-1]:
        decision = "SELL"
        log_change(f"Decision: {decision}. Trend: Upward. Predicted price: {predicted_price:.4f} < Last price: {last_prices.iloc[-1]:.4f}")
    else:
        decision = "HOLD"
        log_change(f"Decision: {decision}. No strong trend or prediction matches last price: {last_prices.iloc[-1]:.4f}")
    return decision
