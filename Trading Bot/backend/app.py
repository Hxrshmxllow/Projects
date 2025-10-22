from flask import Flask, request, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

ALPHA_VANTAGE_API_KEY = "GCCK1VX261WUUKX3"

@app.route('/')
def hello_world():
    return 'Hello World'

@app.route("/search", methods=["GET"])
def search_stock():
    query = request.args.get("query")  
    if not query:
        return jsonify({"error": "Missing query parameter"}), 400
    url = f"https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={query}&apikey={ALPHA_VANTAGE_API_KEY}"
    response = requests.get(url)
    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch data"}), 500
    data = response.json()
    results = [
        {"symbol": item["1. symbol"], "name": item["2. name"]}
        for item in data.get("bestMatches", [])
    ]
    return jsonify(results)

@app.route("/stock-data", methods=["GET"])
def stock_data():
    symbol = request.args.get("symbol")
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={ALPHA_VANTAGE_API_KEY}"
    response = requests.get(url)
    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch stock data"}), 500
    data = response.json()
    print(data)
    time_series = data.get("Time Series (Daily)", {})
    stock_prices = []
    for date, values in list(time_series.items())[:30]:  
        stock_prices.append({
            "date": date,
            "price": float(values["4. close"])
        })
    return jsonify(stock_prices)

if __name__ == '__main__':
    app.run()