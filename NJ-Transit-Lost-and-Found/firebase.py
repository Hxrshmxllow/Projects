import os
from werkzeug.utils import secure_filename
import firebase_admin
from firebase_admin import credentials, firestore, storage
from dotenv import load_dotenv

if not firebase_admin._apps:
    firebase_credentials_path = credentials.Certificate("lost-found-firebase.json")
    firebase_admin.initialize_app(firebase_credentials_path, {
        'storageBucket': 'lost-found-83655.appspot.com'
    })

db = firestore.client()  # Initialize Firestore
bucket = storage.bucket()  # Initialize Storage

VALID_CATEGORIES = [
    "Art/Photos", "Baby Items", "Bag", "Books/Writing Instruments", 
    "Cell Phone", "Clothing", "Electronics/Accessories", 
    "Household Goods/Appliances", "ID Cards", "Wallets", "Jewelry", 
    "Medical Field Related", "Misc", "None", "Perishable", 
    "Personal Accessories", "Shoes", "Sports/Recreation", "Tickets", "Toys", 
]

def upload_item(image_path, category , description , bus_route=None, bus_stop = None, train_line = None, train_station = None):
    """Upload image, location, and route to Firebase Storage and Firestore under a specific category."""
    if category not in VALID_CATEGORIES:
        print(f"Invalid category: {category}")
        return

    try:
        item_id = db.collection(category).document().id

        # Upload image to Firebase Storage
        blob = bucket.blob(f"{category}/{item_id}.jpg")
        with open(image_path, 'rb') as image_file:
            blob.upload_from_file(image_file)

        # Make the image publicly accessible
        blob.make_public()

        # Use the public URL
        image_url = blob.public_url
        # Store item metadata in Firestore
        item_data = {
            'item_id': item_id,
            'bus_route': bus_route,  # New variable to store "Bus Stop" or "Train Station"
            'bus_stop' : bus_stop,
            'train_line': train_line,
            'train_station' : train_station,                  # New variable to store bus number or train route
            'image_url': image_url,
            'category': category,
            'description' : description
        }
        db.collection(category).document(item_id).set(item_data)

        
        os.remove(image_path)
    except Exception as e:
        print(f"Error uploading item: {e}")


def search_items(location_type, route, category):
    """Search for matching items in Firestore within a specified category, location type, and route."""
    try:
        items_ref = db.collection(category)
        matches = items_ref.stream()

        matched_items = []
        for item in matches:
            print(item)
            item_data = item.to_dict()
            item_location_type = item_data.get('location_type', '')
            item_route = item_data.get('route', '')
            # Debugging output for each item
            print(f"Checking item in category '{category}': Location: {item_location_type}, Route: {item_route}")
            
            # Check for matching location and route
            if location_type.lower() == item_location_type.lower() and route.lower() == item_route.lower():
                print(f"Match found: {item_data}")
                matched_items.append(item_data)

        # Final debug output
        print(f"Total matched items in category '{category}': {matched_items}")
        return matched_items
    except Exception as e:
        print(f"Error searching items: {e}")
        return []
