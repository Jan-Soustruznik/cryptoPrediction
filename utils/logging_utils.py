from datetime import datetime


def log_change(message, log_path=f"tmp/log/model_update_log.txt"):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(log_path, "a") as log_file:
        log_file.write(f"{timestamp} - {message}\n")

# Log model structure
def log_model_structure(model, tag="Model Structure"):
    structure = []
    for layer in model.layers:
        structure.append(f"Layer: {layer.name}, Type: {layer.__class__.__name__}, Params: {layer.count_params()}")
    log_change(f"{tag}:\n" + "\n".join(structure))

# Log weight differences between two models
def log_weight_changes(old_model, new_model):
    for i, (old_weights, new_weights) in enumerate(zip(old_model.get_weights(), new_model.get_weights())):
        weight_diff = np.abs(old_weights - new_weights).mean()
        log_change(f"Layer {i+1}: Mean weight change: {weight_diff:.6f}")