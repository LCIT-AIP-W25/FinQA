import React from 'react';
import { useNavigate } from 'react-router-dom';
import '../styles/TradingBot.css';

function TradingBot() {
  const user = JSON.parse(localStorage.getItem("user"));
  const navigate = useNavigate();

  const handleSignOut = () => {
    localStorage.clear();
    navigate('/login');
  };

  return (
    <div className="trading-bot-container">
      <header className="trading-header">
        <div className="header-top">
          <div className="logo-title">
            <img src="/images/Logo.png" alt="FinAnswer Logo" className="trading-logo" />
            <h1>Trading Bot</h1>
          </div>
        </div>
      </header>

      <main className="trading-main">
        <div className="trading-content">
          <h2>Trading Bot Assistant</h2>
          <p>Welcome to the Trading Bot. This is where you can perform automated trading strategies.</p>
          <div className="features-section">
            <div className="feature-card">
              <h3>Automated Trading</h3>
              <p>Set up automated trading strategies based on technical indicators.</p>
            </div>
            <div className="feature-card">
              <h3>Market Analysis</h3>
              <p>Get real-time market analysis and predictions.</p>
            </div>
            <div className="feature-card">
              <h3>Risk Management</h3>
              <p>Manage your portfolio risk with our advanced tools.</p>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}

export default TradingBot;
