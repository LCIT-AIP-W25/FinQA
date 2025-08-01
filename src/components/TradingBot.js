import React, { useState } from 'react';
import axios from 'axios';

import '../styles/TradingBot.css';

function TradingBot() {
  const [amount, setAmount] = useState('');
  const [riskLevel, setRiskLevel] = useState('medium');
  const [months, setMonths] = useState('');
  const [responseData, setResponseData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Input validation
    if (!amount || isNaN(amount) || parseFloat(amount) <= 0) {
      setError('Please enter a valid positive amount.');
      return;
    }
    if (!['low', 'medium', 'high'].includes(riskLevel)) {
      setError('Please select a valid risk level.');
      return;
    }
    if (!months || isNaN(months) || parseInt(months) <= 0) {
      setError('Please enter a valid positive number of months.');
      return;
    }

    setError(null);
    setLoading(true);
    setResponseData(null);

    try {
      const response = await axios.post(process.env.REACT_APP_API_BASE + '/portfolio-suggestion', {
        amount: parseFloat(amount),
        risk_level: riskLevel,
        months: parseInt(months)
      });

      setResponseData(response.data);
    } catch (err) {
      setError(`Failed to fetch portfolio suggestion: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="trading-bot-section" style={{ maxWidth: 600, margin: '0 auto', padding: 20 }}>
      <h1>Trading Bot Portfolio Suggestion</h1>
      <form onSubmit={handleSubmit} className="form-container" style={{ marginBottom: 20 }}>
        <div style={{ marginBottom: 10 }}>
          <label>
            Amount ($):
            <input
              type="number"
              step="0.01"
              value={amount}
              onChange={(e) => setAmount(e.target.value)}
              required
              style={{ marginLeft: 10, width: '100%' }}
            />
          </label>
        </div>
        <div style={{ marginBottom: 10 }}>
          <label>
            Risk Level:
            <select
              value={riskLevel}
              onChange={(e) => setRiskLevel(e.target.value)}
              required
              style={{ marginLeft: 10, width: '100%' }}
            >
              <option value="low">Low</option>
              <option value="medium">Medium</option>
              <option value="high">High</option>
            </select>
          </label>
        </div>
        <div style={{ marginBottom: 10 }}>
          <label>
            Months:
            <input
              type="number"
              value={months}
              onChange={(e) => setMonths(e.target.value)}
              required
              style={{ marginLeft: 10, width: '100%' }}
            />
          </label>
        </div>
        <div className="submit-button-container">
          <button type="submit" disabled={loading} style={{ padding: '8px 16px' }}>
            {loading ? 'Loading...' : 'Get Portfolio Suggestion'}
          </button>
        </div>
      </form>

      {error && <div style={{ color: 'red', marginBottom: 20 }}>{error}</div>}

      {responseData && (
        <div>
          <h2>Summary</h2>
          <ul>
            <li>Total Investment: {responseData.summary.total_investment}</li>
            <li>Risk Level: {responseData.summary.risk_level}</li>
            <li>Period: {responseData.summary.period}</li>
            <li>Expected Return: {responseData.summary.expected_return}</li>
            <li>Expected Profit: {responseData.summary.expected_profit}</li>
          </ul>

          <h2>Stocks</h2>
          <table border="1" cellPadding="5" cellSpacing="0" style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead>
              <tr>
                <th>Ticker</th>
                <th>Company</th>
                <th>Expected Return</th>
                <th>Expected Profit</th>
              </tr>
            </thead>
            <tbody>
              {responseData.stocks.map((stock, index) => (
                <tr key={index}>
                  <td>{stock.ticker}</td>
                  <td>{stock.company}</td>
                  <td>{stock.expected_return}</td>
                  <td>{stock.expected_profit}</td>
                </tr>
              ))}
            </tbody>
          </table>

          <h2>Strategy</h2>
          <p>{responseData.strategy}</p>
        </div>
      )}
    </div>
  );
}

export default TradingBot;