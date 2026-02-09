import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from joblib import dump
import os

# -----------------------------
# DATASET PATH (YOUR PC)
# -----------------------------
DATA_PATH = r"C:\Users\Ingage_Trainer_08\Desktop\IOT-Health-AI-Dashboard\dataset\health_dataset.csv"

# -----------------------------
# LOAD DATA
# -----------------------------
df = pd.read_csv(DATA_PATH)

# -----------------------------
# FEATURES & LABEL
# -----------------------------
X = df[['heart_rate', 'temp', 'humidity']]
y = df['risk_level']

# -----------------------------
# SPLIT DATA
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# -----------------------------
# TRAIN MODEL
# -----------------------------
model = RandomForestClassifier(n_estimators=200, random_state=42)
model.fit(X_train, y_train)

# -----------------------------
# TEST MODEL
# -----------------------------
y_pred = model.predict(X_test)
print("\nAccuracy:", accuracy_score(y_test, y_pred))
print("\nReport:\n", classification_report(y_test, y_pred))

# -----------------------------
# SAVE MODEL
# -----------------------------
MODEL_DIR = os.path.join(os.path.dirname(__file__), "models")
os.makedirs(MODEL_DIR, exist_ok=True)

dump(model, os.path.join(MODEL_DIR, "health_model.pkl"))

print("\nModel saved at backend/models/health_model.pkl")
