from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
from utils.logging_utils import log_change

def train_model(model, X, y):
    """
    Parameters:
    - X: numpy array input data (shape: [samples, timesteps, features])
    - y: numpy array target values (shape: [samples])
    
    output:
    - trained model LSTM
    """

    # Callbac
    # "early_stop" - When val_loss does not increase after 3 epochs, training stops.
    # "reduce_lr" - If val_loss does not improve after 2 epochs, it will reduce the learning rate by half.
    early_stop = EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True)
    reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=2)

    # training
    # include validation, use 80% of the data for training and 20% for validation. - "validation_split=0.2"
    history = model.fit(X, y, epochs=50, batch_size=32, validation_split=0.2,
                        callbacks=[early_stop, reduce_lr], verbose=1)
    log_change("Model trained")
    log_change(f"Training loss history: {history.history['loss']}")
    
    return model
