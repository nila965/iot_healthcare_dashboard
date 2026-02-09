import requests
import logging

# Set up logging for professional error tracking
logging.basicConfig(level=logging.INFO)

def fetch_thingspeak_data(channel_id, api_key, results=10):
    """
    Fetches and cleans data from a ThingSpeak channel.
    Handles field mapping and null value prevention.
    """
    url = f"https://api.thingspeak.com/channels/{channel_id}/feeds.json"
    params = {
        "api_key": api_key,
        "results": results
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            feeds = response.json().get("feeds", [])
            
            # Professional data cleaning: Replace None/Null with "0" to prevent frontend crashes
            cleaned_data = []
            for entry in feeds:
                cleaned_entry = {
                    "created_at": entry.get("created_at"),
                    "entry_id": entry.get("entry_id")
                }
                
                # Dynamically clean fields 1 through 8
                for i in range(1, 9):
                    field_key = f"field{i}"
                    val = entry.get(field_key)
                    # If sensor data is missing, default to "0"
                    cleaned_entry[field_key] = val if val is not None else "0"
                
                cleaned_data.append(cleaned_entry)
                
            return cleaned_data
        else:
            logging.error(f"ThingSpeak Error: {response.status_code} for Channel {channel_id}")
            return []

    except requests.exceptions.RequestException as e:
        logging.error(f"Connection Error to ThingSpeak: {e}")
        return []