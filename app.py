from flask import Flask, jsonify
from flask_cors import CORS

from thingspeak import fetch_thingspeak_data
from firebase_db import save_to_firebase
from predict import predict_risk

# -----------------------------
# CONFIG – Using your provided Channel IDs
# -----------------------------
# Channel 1: Health (Fields: 1:Temp, 2:Humi, 3:HeartRate, 4:Pulse, 5:RTC)
THINGSPEAK_CH1 = "3254741"
THINGSPEAK_KEY1 = "MWO5EB4I47OZCI4W"

# Channel 2: Motion (Field: 1: Gesture Code)
THINGSPEAK_CH2 = "3254742"
THINGSPEAK_KEY2 = "1W3VRELD11ICYPKH"

# -----------------------------
# FLASK SETUP
# -----------------------------
app = Flask(__name__)
CORS(app)

# -----------------------------
# ROUTES
# -----------------------------

@app.route("/health")
def health():
    """
    Fetches Health Channel (5 Fields)
    Mapping: 1:Temp, 2:Humi, 3:HeartRate, 4:Pulse, 5:RTC
    """
    data = fetch_thingspeak_data(THINGSPEAK_CH1, THINGSPEAK_KEY1, results=10)
    if data:
        # Save historical health logs to Firebase
        save_to_firebase(data, "health_data")
    return jsonify(data)

@app.route("/motion")
def motion():
    """
    Fetches Motion Channel (Gesture Monitoring)
    Mapping: Field 1 contains the numeric Gesture Code (0-10)
    """
    data = fetch_thingspeak_data(THINGSPEAK_CH2, THINGSPEAK_KEY2, results=10)
    if data:
        # Save historical gesture logs to Firebase
        save_to_firebase(data, "motion_data")
    return jsonify(data)

@app.route("/predict")
def predict():
    """
    Predicts health risk based on Channel 1 vitals.
    Correct Field Mapping based on your setup:
    - Field 3 = Heart Rate
    - Field 1 = Temperature
    - Field 2 = Humidity
    """
    data = fetch_thingspeak_data(THINGSPEAK_CH1, THINGSPEAK_KEY1, results=1)
    if not data:
        return jsonify({"error": "No data from ThingSpeak"}), 400

    latest = data[0]
    try:
        # Pull specific fields for AI input mapping
        hr = float(latest.get("field3", 0))    # HeartRate
        temp = float(latest.get("field1", 0))  # Temperature
        hum = float(latest.get("field2", 0))   # Humidity

        # Generate risk level using the trained AI model
        risk = predict_risk(hr, temp, hum)
        
        return jsonify({
            "risk_level": risk,
            "vitals": {"hr": hr, "temp": temp, "hum": hum},
            "timestamp": latest.get("field5") # RTC Timer value
        })
    except (ValueError, KeyError, TypeError) as e:
        return jsonify({"error": "Data processing error", "details": str(e)}), 500

# -----------------------------
if __name__ == "__main__":
    # Host 0.0.0.0 allows other devices on your local Wi-Fi to view the dashboard
    app.run(host="0.0.0.0", port=5000, debug=True)