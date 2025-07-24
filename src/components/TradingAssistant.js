import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import '../styles/TradingAssistant.css';

function TradingAssistant() {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [query, setQuery] = useState('');
  const [response, setResponse] = useState('');
  const [loading, setLoading] = useState(false);
  const [companyList, setCompanyList] = useState([]);
  const [selectedCompany, setSelectedCompany] = useState('');

  const user = JSON.parse(localStorage.getItem("user"));
  const navigate = useNavigate();

useEffect(() => {
  async function fetchCompanies() {
    try {
      const response = await axios.get('https://finrl-xsc4.onrender.com/companies');
      setCompanyList(response.data);  // ✅ Use the response directly
      console.log("✅ Companies loaded for Trading Assistant:", response.data);
    } catch (error) {
      console.error("❌ Error fetching trading assistant companies:", error);
    }
  }
  fetchCompanies();
}, []);

  const toggleMenu = () => setIsMenuOpen(!isMenuOpen);

  const handleSignOut = () => {
    localStorage.clear();
    window.location.href = '/login';
  };

  const handleQuery = async () => {
    if (!query.trim()) return;

    setLoading(true);
    try {
      const response = await axios.post('https://finrl-xsc4.onrender.com/companies', {
        query: query,
        user_id: user?.user_id,

        company: selectedCompany // 🟩 Pass selected company to backend
      });

      setResponse(response.data.response);
    } catch (error) {
      console.error('Error querying trading assistant:', error);
      setResponse('Sorry, I encountered an error processing your request. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="trading-assistant-container">
      <div className={`menu-overlay ${isMenuOpen ? 'open' : ''}`} onClick={() => setIsMenuOpen(false)}></div>

      <header className="trading-header">
        <div className="header-top">
          <div className="logo-title">
            <img src="/images/Logo.png" alt="FinAnswer Logo" className="trading-logo" />
            <h1>Trading Assistant</h1>
          </div>
        </div>
      </header>

      {!isMenuOpen && (
        <button className="menu-toggle" onClick={toggleMenu}>
          <span className="menu-icon"></span>
        </button>
      )}

      <nav className={`nav-menu ${isMenuOpen ? 'open' : ''}`}>
        {isMenuOpen && (
          <button className="menu-toggle" onClick={toggleMenu}>
            <span className={`menu-icon ${isMenuOpen ? 'open' : ''}`}></span>
          </button>
        )}
        <ul>
          <li><a href="/home">Home</a></li>
          <li><a href="/chat">Chat</a></li>
          <li><a href="/pdf-chat">PDF Analysis</a></li>
          <li><a href="/trading-assistant">Trading Assistant</a></li>
          <li className="menu-category">Account</li>
          <li><button className="menu-btn sign-out" onClick={handleSignOut}>Sign Out</button></li>
        </ul>
      </nav>

      <main className="trading-main">
        <div className="trading-content">
          <h2>Ask Your Trading Question</h2>

          {/* ✅ Company Selector */}
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

  <button 
    onClick={handleQuery} 
    disabled={loading || !query}
    className="query-button"
  >
    {loading ? 'Processing...' : 'Get Prediction'}
  </button>
</div>


          {/* ✅ Response Output */}
          {response && (
            <div className="response-section">
              <h3>Response:</h3>
              <div className="response-content">
                {response}
              </div>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}

export default TradingAssistant;
