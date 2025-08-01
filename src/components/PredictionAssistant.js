import React, { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import axios from 'axios';
import '../styles/PredictionAssistant.css';

import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer
} from 'recharts';

function PredictionAssistant() {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [query, setQuery] = useState('');
  const [response, setResponse] = useState([]);
  const [loading, setLoading] = useState(false);
  const [companyList, setCompanyList] = useState([]);
  const [selectedCompany, setSelectedCompany] = useState('');

  const user = JSON.parse(localStorage.getItem("user"));
  const navigate = useNavigate();

  const COMPANY_API_URL = process.env.REACT_APP_API_BASE + '/companies';

  useEffect(() => {
    async function fetchCompanies() {
      try {
        const response = await axios.get(COMPANY_API_URL);
        if (Array.isArray(response.data)) {
          setCompanyList(response.data);
        } else {
          console.error("❌ Unexpected data format for companies:", response.data);
          setCompanyList([]);
        }
        console.log("✅ Companies loaded for Trading Assistant:", response.data);
      } catch (error) {
        console.error("❌ Error fetching trading assistant companies:", error);
        setCompanyList([]);
      }
    }
    fetchCompanies();
  }, [COMPANY_API_URL]);

  const toggleMenu = () => setIsMenuOpen(!isMenuOpen);

  const handleSignOut = () => {
    localStorage.clear();
    navigate('/login');
  };

  const handleQuery = async () => {
    if (!query || !selectedCompany) return;

    setLoading(true);
    setResponse([]);
    try {
      const tickerRes = await axios.get(`${process.env.REACT_APP_API_BASE}/find_ticker?q=${selectedCompany}`);
      const ticker = tickerRes.data?.ticker;
      if (!ticker) {
        setResponse([{ date: "", prediction: "N/A", risk_level: "Ticker not found" }]);
        return;
      }

      const days = parseInt(query);
      const today = new Date();
      const predictionResults = [];

      for (let i = 0; i < days; i++) {
        const date = new Date(today);
        date.setDate(today.getDate() + i);
        const isoDate = date.toISOString().split('T')[0];

        try {
          const predRes = await axios.get(`${process.env.REACT_APP_API_BASE}/prediction_by_date?ticker=${ticker}&date=${isoDate}`);
          const predictionObj = predRes.data?.predictions?.[0];
          if (predictionObj) {
            predictionResults.push({
              date: predictionObj.date,
              prediction: predictionObj.prediction,
              risk_level: predictionObj.risk_level
            });
          } else {
            predictionResults.push({ date: isoDate, prediction: 'N/A', risk_level: 'No prediction' });
          }
        } catch (err) {
          predictionResults.push({ date: isoDate, prediction: 'N/A', risk_level: 'Error fetching prediction' });
        }
      }

      setResponse(predictionResults);
    } catch (error) {
      console.error('❌ Error during prediction:', error);
      setResponse([{ date: "", prediction: "N/A", risk_level: "Unexpected error" }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="trading-assistant-container">
      <header className="prediction-header">
        <div className="header-top-prediction">
          <div className="logo-title-prediction">
            <img src="/images/Logo.png" alt="FinAnswer Logo" className="home-logo" />
            <h1>Prediction Bot</h1>
          </div>
            <div className="top-nav-wrapper">
              <div className="top-nav">
                <Link to="/home">Home</Link>
                <Link to="/chat">Learning Bot</Link>
                <Link to="/prediction-assistant">Prediction Bot</Link>
                <Link to="/trading-bot">Trading Bot</Link>
                

                <button onClick={handleSignOut} className="sign-out-btn">Sign Out</button>
              </div> 
          </div>
        </div>
      </header>
       <main className="trading-main">
        <div className="trading-container">
          <h2>Predict Price</h2>

          {/* Company Selector */}
          <div className="company-selector">
            <label htmlFor="companyDropdown" className="selector-label">Select Company:</label>
            <select
              id="companyDropdown"
              className="selector-dropdown"
              value={selectedCompany}
              onChange={(e) => setSelectedCompany(e.target.value)}
            >
              <option value="">-- Choose a company --</option>
              {companyList.map((company, idx) => (
                <option key={idx} value={company}>{company}</option>
              ))}
            </select>
          </div>

 {/* Day Selector and Button */}
<div className="query-section inline-sentence">
  <span className="sentence-text">Predict stock movement for the next</span>

  <select
    id="daysDropdown"
    className="days-inline-dropdown"
    value={query}
    onChange={(e) => setQuery(e.target.value)}
  >
    <option value="">--select--</option>
    {Array.from({ length: 8 }, (_, i) => {
      const days = i + 3;
      return (
        <option key={days} value={days}>
          {days} days
        </option>
      );
    })}
  </select>

  <span className="sentence-text">.</span>
</div>

<div className="query-button-wrapper">
  <button
    onClick={handleQuery}
    disabled={loading || !query || !selectedCompany}
    className="query-button"
  >
    {loading ? 'Processing...' : 'Get Prediction'}
  </button>
</div>

{/* Response Output */}
{response.length > 0 && (
  <div className="response-section">
    <h3>Predictions:</h3>

    {/* 📊 Chart */}
    <div style={{ width: '100%', height: 300 }}>
      <ResponsiveContainer>
        <LineChart
          data={response}
          margin={{ top: 20, right: 30, left: 20, bottom: 5 }}
        >
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="date" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Line
            type="monotone"
            dataKey="prediction"
            stroke="#8884d8"
            activeDot={{ r: 6 }}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>

    {/* 📋 List */}
    <ul className="response-list">
      {response.map((item, idx) => (
        <li key={idx}>
          {item.date}: <strong>{item.prediction}</strong> | Risk:{' '}
          <em>{item.risk_level}</em>
        </li>
      ))}
    </ul>
  </div>
)}

        </div> {/* Close trading-content */}
      </main>
    </div>  
  );
}

export default PredictionAssistant;