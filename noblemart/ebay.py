import requests

def add_item_to_ebay(item_data, access_token):
    url = "https://api.ebay.com/sell/inventory/v1/inventory_item"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    payload = {
        "sku": item_data["sku"],
        "product": {
            "title": item_data["title"],
            "description": item_data["description"],
            "aspects": item_data["aspects"],  # e.g., {"Brand": ["BrandName"]}
            "imageUrls": item_data["imageUrls"],
            "mpn": item_data["mpn"]
        },
        "availability": {
            "shipToLocationAvailability": {
                "quantity": item_data["quantity"]
            }
        },
        "condition": "NEW",
        "price": {
            "value": item_data["price"],
            "currency": "USD"
        }
    }
    response = requests.post(url, headers=headers, json=payload)
    return response.json()