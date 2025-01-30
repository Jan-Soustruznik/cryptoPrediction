from tensorflow.keras.models import load_model as keras_load_model
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from utils.logging_utils import log_change, log_model_structure
import os

# Load or create model
def load_or_create_model(input_shape, model_path):
    if os.path.exists(model_path):
        old_model = keras_load_model(model_path)
        log_change(f"Model successfully loaded from {model_path}.")
        log_model_structure(old_model, "Loaded Model Structure")
        model = old_model
    else:
        log_change(f"No model found at {model_path}. Creating a new model...")
        model = Sequential([
            LSTM(50, return_sequences=True, input_shape=input_shape),
            LSTM(50, return_sequences=False),
            Dense(25),
            Dense(1)
        ])
        model.compile(optimizer='adam', loss='mean_squared_error')
        log_model_structure(model, "New Model Structure")
        log_change("New model created.")

    return model

def save_model(model, model_path):
    try:
        model.save(model_path)
        log_change(f"Model successfully saved to {model_path}.")
    except Exception as e:
        log_change(f"Failed to save the model: {e}")
