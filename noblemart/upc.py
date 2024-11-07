import requests

def retrieveItemData(upc_code):
    response = requests.get(f"https://api.upcitemdb.com/prod/trial/lookup?upc={upc_code}")

    if response.status_code == 200:
        data = response.json()
        if data['code'] == "OK":
            item = data['items'][0]  
            name = item['title']
            brand = item['brand']
            description = item['description']
            category = item['category']
            img =  item['images'][0]
            return [name, brand, description, category, img]
        else:
            return None
    else:
        return None