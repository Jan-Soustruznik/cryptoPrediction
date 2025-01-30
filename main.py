from config import *
from data.data_fetcher import update_historical_data
from data.data_processing import prepare_data, compute_indicators
from model.model_utils import load_or_create_model, save_model
from model.model_training import train_model
from utils.logging_utils import log_change
from utils.decision_making import make_decision
from data.database import save_to_database
import tensorflow as tf
from tensorflow.keras.backend import clear_session
import time


if __name__ == "__main__":
    # Enable eager execution
    tf.config.run_functions_eagerly(True)

    # Clear existing session
    clear_session()
    
    symbol = "HBAR-USDT"
    interval = "1hour"
    
    # Update historical data
    df = update_historical_data(symbol, interval, DATA_PATH)

   # Compute RSI and MACD
    df = compute_indicators(df)

  # Prepare data for training
    X, y, scaler = prepare_data(df)

    # Load or create model
    model = load_or_create_model(X.shape[1:], MODEL_PATH)

   # Train the model
    model = train_model(model, X, y)

    # Uložení modelu
    save_model(model, MODEL_PATH)

    # # Make a prediction
    predicted_price = model.predict(X[-1].reshape(1, X.shape[1], X.shape[2]))
    predicted_price = scaler.inverse_transform([[predicted_price[0][0], 0, 0, 0]])[0][0]
    log_change(f"New prediction: {predicted_price:.4f}")

    # Make a decision
    decision = make_decision(df, predicted_price)
    log_change(f"Final decision based on analysis: {decision}")

    # Save prediction to database
    real_price = df['close'].iloc[-1]
    save_to_database(int(time.time()), real_price, predicted_price, decision)
