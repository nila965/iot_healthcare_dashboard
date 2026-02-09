from joblib import load
import os

# -----------------------------
# LOAD TRAINED MODEL
# -----------------------------
MODEL_PATH = os.path.join("models", "health_model.pkl")
model = load(MODEL_PATH)

# -----------------------------
# PREDICTION FUNCTION
# -----------------------------
def predict_risk(heart_rate, temperature, humidity):
    """
    Predict health risk level
    Returns: Low / Medium / High
    """
    data = [[heart_rate, temperature, humidity]]
    result = model.predict(data)
    return result[0]
