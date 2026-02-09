import firebase_admin
from firebase_admin import credentials, firestore

# -----------------------------
# FIREBASE INITIALIZE
# -----------------------------
cred = credentials.Certificate("firebase_key.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# -----------------------------
# SAVE FUNCTION
# -----------------------------
def save_to_firebase(data, collection_name):
    """
    Save ThingSpeak data to Firestore
    """
    for item in data:
        db.collection(collection_name).add(item)
