from utils.logging_utils import log_change 

def train_model(model, X, y):
    """
    Funkce pro trénování modelu LSTM.
    
    Parametry:
    - X: numpy array vstupních dat (shape: [samples, timesteps, features])
    - y: numpy array cílových hodnot (shape: [samples])
    
    Návratová hodnota:
    - Vytrénovaný model LSTM
    """

    # Trénování modelu
    history = model.fit(X, y, epochs=10, batch_size=32, verbose=1)
    log_change("Model trained")
    log_change(f"Training loss history: {history.history['loss']}")
    
    return model
