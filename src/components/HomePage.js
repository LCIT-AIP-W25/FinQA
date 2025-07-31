import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import axios from 'axios';
import '../styles/HomePage.css';

function HomePage() {
  const [news, setNews] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedSentiments, setSelectedSentiments] = useState([]);
  const [selectedDate, setSelectedDate] = useState('');
  const [selectedTickers, setSelectedTickers] = useState([]);

  const [tempSelectedSentiments, setTempSelectedSentiments] = useState([]);
  const [tempSelectedDate, setTempSelectedDate] = useState('');
  const [tempSelectedTickers, setTempSelectedTickers] = useState([]);
  const [uniqueTickers, setUniqueTickers] = useState([]);

  const [currentPage, setCurrentPage] = useState(1);
  const [itemsPerPage] = useState(18);
  const user = JSON.parse(localStorage.getItem("user"));
  const navigate = useNavigate();

  useEffect(() => {
    fetchNews();
    fetchTickers();
  }, []);

  const fetchNews = async () => {
    try {
      const response = await axios.get(`http://localhost:5050/api/finance_news?limit=50`);
      setNews(Array.isArray(response.data) ? response.data : []);
    } catch (err) {
      console.error("News fetch error:", err);
    } finally {
      setLoading(false);
    }
  };

  const fetchTickers = async () => {
    try {
      const response = await axios.get(`http://localhost:5050/api/finance_news/tickers`);
      if (Array.isArray(response.data)) {
        const sorted = response.data.map(t => t.trim().toUpperCase()).sort();
        setUniqueTickers(sorted);
      }
    } catch (err) {
      console.error("Tickers fetch error:", err);
    }
  };

  const handleSentimentChange = (e) => {
    const value = e.target.value;
    setTempSelectedSentiments(prev =>
      prev.includes(value) ? prev.filter(s => s !== value) : [...prev, value]
    );
  };

  const handleDateChange = (e) => setTempSelectedDate(e.target.value);

  const handleTickerChange = (e) => {
    const value = e.target.value;
    setTempSelectedTickers(prev =>
      prev.includes(value) ? prev.filter(t => t !== value) : [...prev, value]
    );
  };

  const filterByDate = (itemDate) => {
    if (!selectedDate) return true;
    const now = new Date();
    const published = new Date(itemDate);
    if (selectedDate === 'today') return published.toDateString() === now.toDateString();
    if (selectedDate === 'week') {
      const weekAgo = new Date(now);
      weekAgo.setDate(now.getDate() - 7);
      return published >= weekAgo && published <= now;
    }
    if (selectedDate === 'month') {
      const monthAgo = new Date(now);
      monthAgo.setMonth(now.getMonth() - 1);
      return published >= monthAgo && published <= now;
    }
    return true;
  };

  const filterByTicker = (ticker) => {
    if (!ticker) return false;
    if (selectedTickers.length === 0) return true;
    return selectedTickers.includes(ticker.trim().toUpperCase());
  };

  const handleSignOut = () => {
    localStorage.removeItem('user');
    localStorage.removeItem('token');
    navigate('/login');
  };

  const filteredNews = news
    .filter(item => item.title?.toLowerCase().includes(searchTerm.toLowerCase()))
    .filter(item => selectedSentiments.length === 0 || selectedSentiments.includes(item.sentiment_label))
    .filter(item => filterByDate(item.scraped_at))
    .filter(item => filterByTicker(item.ticker));

  useEffect(() => setCurrentPage(1), [searchTerm, selectedSentiments, selectedDate, selectedTickers]);

  const totalPages = Math.ceil(filteredNews.length / itemsPerPage);
  const startIndex = (currentPage - 1) * itemsPerPage;
  const endIndex = startIndex + itemsPerPage;
  const currentNews = filteredNews.slice(startIndex, endIndex);

  return (
    <div className="home-container">
      <header className="home-header">
        <div className="header-top">
          <div className="logo-title">
            <img src="/images/Logo.png" alt="FinAnswer Logo" className="home-logo" />
            <h1>Welcome, {user?.username} 👋</h1>
          </div>
          <div className="search-nav-wrapper">
            <input
              type="text"
              className="home-search-bar"
              placeholder="Search news..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
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
        </div>
      </header>

      <main className="main-content">
        <aside className="filters-sidebar">
          <h3>Filter News</h3>

          <div className="filter-section">
            <h4>By Sentiment</h4>
            {['Positive', 'Negative', 'Neutral'].map((sentiment) => (
              <label className="filter-option" key={sentiment}>
                <input
                  type="checkbox"
                  name="sentiment"
                  value={sentiment}
                  checked={tempSelectedSentiments.includes(sentiment)}
                  onChange={handleSentimentChange}
                />
                {sentiment}
              </label>
            ))}
          </div>

          <div className="filter-section">
            <h4>By Date</h4>
            <div className="filter-options">
              {['today', 'week', 'month', ''].map((option, idx) => (
                <label className="filter-option" key={idx}>
                  <input
                    type="radio"
                    name="date"
                    value={option}
                    checked={tempSelectedDate === option}
                    onChange={handleDateChange}
                  />
                  {option === '' ? 'All' : option.charAt(0).toUpperCase() + option.slice(1)}
                </label>
              ))}
            </div>
          </div>

          <div className="filter-section">
            <h4>By Ticker</h4>
            <div className="filter-options">
              {uniqueTickers.map((ticker) => (
                <label className="filter-option" key={ticker}>
                  <input
                    type="checkbox"
                    name="ticker"
                    value={ticker}
                    checked={tempSelectedTickers.includes(ticker)}
                    onChange={handleTickerChange}
                  />
                  {ticker}
                </label>
              ))}
            </div>
          </div>

          <button
            className="filter-button"
            type="button"
            onClick={() => {
              setSelectedSentiments(tempSelectedSentiments);
              setSelectedDate(tempSelectedDate);
              setSelectedTickers(tempSelectedTickers);
            }}
          >
            Apply Filter
          </button>
        </aside>

        <div className="news-section">
          <div className="news-header">
            <h2>Latest Financial News</h2>
            {filteredNews.length > 0 && (
              <div className="news-info">
                Showing {startIndex + 1} - {Math.min(endIndex, filteredNews.length)} of {filteredNews.length} articles
              </div>
            )}
          </div>

          {loading ? (
            <div className="loading">Loading...</div>
          ) : (
            <>
              <div className="news-tiles-container">
                {currentNews.map((item, idx) => (
                  <div key={idx} className="news-tile">
                    <h3 className="news-title">
                      <a href={item.url} target="_blank" rel="noreferrer">{item.title}</a>
                    </h3>
                    <p className="news-ticker">{item.ticker}</p>
                    <p className="news-date">🗓 {new Date(item.scraped_at).toLocaleDateString()}
                    </p>
                  </div>
                ))}
              </div>

              {totalPages > 1 && (
                <div className="pagination">
                  <button onClick={() => setCurrentPage(p => Math.max(p - 1, 1))} disabled={currentPage === 1}>← Prev</button>
                  {Array.from({ length: Math.min(totalPages, 5) }, (_, i) => {
                    const page = totalPages <= 5 ? i + 1 : currentPage <= 3 ? i + 1 : currentPage >= totalPages - 2 ? totalPages - 4 + i : currentPage - 2 + i;
                    return (
                      <button
                        key={page}
                        className={`pagination-number ${currentPage === page ? 'active' : ''}`}
                        onClick={() => setCurrentPage(page)}
                      >
                        {page}
                      </button>
                    );
                  })}
                  <button onClick={() => setCurrentPage(p => Math.min(p + 1, totalPages))} disabled={currentPage === totalPages}>Next →</button>
                </div>
              )}
            </>
          )}
        </div>

        <div className="right-container">
          <h3 className="section-title">Top Finance Reads</h3>
          {[{
            title: 'Know Your Client (KYC) Rule',
            description: 'Ensures advisors understand your risk tolerance.',
            url: 'https://www.securities-administrators.ca/',
          }, {
            title: 'TFSA Stock Trading Guidelines',
            description: 'TFSA allows stock trading, but day-trading risks tax penalties.',
            url: 'https://www.canada.ca/en/revenue-agency/services/tax/individuals/topics/tax-free-savings-account.html',
          }, {
            title: 'CRM2 – Transparency in Fees',
            description: 'Requires annual disclosure of fees and investment performance.',
            url: 'https://www.getsmarteraboutmoney.ca/invest/investment-products/stocks/',
          }, {
            title: 'Insider Trading Laws',
            description: 'Using non-public information to trade is illegal.',
            url: 'https://www.osc.ca/',
          }].map(({ title, description, url }, idx) => (
            <div key={idx} className="article-card">
              <h4>{title}</h4>
              <p>{description}</p>
              <a href={url} target="_blank" rel="noopener noreferrer" className="view-pdf">Learn More →</a>
            </div>
          ))}
        </div>
      </main>
    </div>
  );
}

export default HomePage;
