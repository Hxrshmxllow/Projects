import './App.css';
import React, { useState, useEffect } from "react";
import { Line } from "react-chartjs-2";
import { Chart as ChartJS, LineElement, CategoryScale, LinearScale, PointElement } from "chart.js";
import axios from "axios"

ChartJS.register(LineElement, CategoryScale, LinearScale, PointElement);

function App() {
  const [query, setQuery] = useState(null);
  const [suggestions, setSuggestions] = useState([]);
  const [chartData, setChartData] = useState(null);

  const handleSearch = async (e) => {
    const searchTerm = e.target.value;
    setQuery(searchTerm);

    if (searchTerm.length > 1) {
      try {
        const response = await axios.get(`http://127.0.0.1:5000/search?query=${searchTerm}`);
        alert(`API Response: ${JSON.stringify(response.data, null, 2)}`); 
        setSuggestions(response.data);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    } else {
      setSuggestions([]);
    }
};

const fetchStockData = async (symbol) => {
  try {
    const response = await axios.get(`http://127.0.0.1:5000/stock-data?symbol=${symbol}`);
    const stockPrices = response.data.map(point => point.price);
    const stockDates = response.data.map(point => point.date);
    setChartData({
      labels: stockDates,
      datasets: [
        {
          label: `${symbol} Stock Price`,
          data: stockPrices,
          borderColor: "#02e0f0",
          backgroundColor: "#02e0f0",
          fill: true,
        },
      ],
    });
  } catch (error) {
  }
};

useEffect(() => {
  fetchStockData("TSLA");
}, []);

  return (
    <main>
      <div className="top_container">
        <div className="current_stock_container">
          {chartData && (
            <Line data={chartData} options={{ maintainAspectRatio: false }} className="chart-background" />
          )}
          <div className="search_container">
            <input 
              className='search_input'
              type="text" 
              value={query} 
              onChange={handleSearch} 
              placeholder="Search stock..."
            />
            {suggestions.length > 0 && (
              <div className="suggestions">
                <ul>
                  {suggestions.map((stock, index) => (
                    <li key={index} onClick={() => { 
                        setQuery(stock.symbol); 
                        fetchStockData(stock.symbol); 
                    }}>
                      {stock.symbol} - {stock.name}
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        </div>
        <div className="current_holdings_container">
        </div>
        <div className="bottom_container">
          <div className="balance_container">
            <p className='balance_text'>Balance:</p>
            <p className='balance_amount' >$1391.11</p>
          </div>
          <div className="buying_power_container">
          </div>
        </div>
      </div>
      <div className="transaction_container">
      </div>
    </main>
  );
}

export default App;
