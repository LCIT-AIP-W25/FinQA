import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import axios from 'axios';
import '../styles/HomePage.css';

function HomePage() {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [isAiChatExpanded, setIsAiChatExpanded] = useState(false);
  const [news, setNews] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedSentiments, setSelectedSentiments] = useState([]);
  const [selectedDate, setSelectedDate] = useState('');
  const [selectedTickers, setSelectedTickers] = useState([]);

  // Temporary states for filters before applying
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
    const apiUrl = `http://localhost:5050/api/finance_news?limit=50`; 
    const response = await axios.get(apiUrl);
    if (Array.isArray(response.data)) {
      setNews(response.data);
    } else {
      setNews([]);
    }
    setLoading(false);
  } catch (error) {
    console.error('Error fetching news:', error.message, error.response);
    setNews([]);
    setLoading(false);
  }
};

const fetchTickers = async () => {
  try {
    const response = await axios.get('http://localhost:5050/api/finance_news/tickers');
    if (Array.isArray(response.data)) {
      const sortedTickers = response.data.map(ticker => ticker.trim().toUpperCase()).sort();
      setUniqueTickers(sortedTickers);
    } else {
      setUniqueTickers([]);
    }
  } catch (error) {
    console.error('Error fetching tickers:', error.message, error.response);
    setUniqueTickers([]);
  }
};

  const toggleMenu = () => setIsMenuOpen(!isMenuOpen);
  const toggleAiChat = () => setIsAiChatExpanded(!isAiChatExpanded);
  const handleMainChat = () => navigate('/chat');
  const handleCompanyReports = () => navigate('/chat', { state: { openPanel: 'company' } });
  const handleChatHistory = () => navigate('/chat', { state: { openPanel: 'history' } });
  const handleMetrics = () => navigate('/chat', { state: { openPanel: 'metrics' } });
  const handleSignOut = () => {
    localStorage.clear();
    window.location.href = '/login';
  };

  const handleSentimentChange = (e) => {
    const value = e.target.value;
    setTempSelectedSentiments(prev =>
      prev.includes(value) ? prev.filter(sentiment => sentiment !== value) : [...prev, value]
    );
  };

  const handleDateChange = (e) => setTempSelectedDate(e.target.value);
  const handleTickerChange = (e) => {
    const value = e.target.value;
    setTempSelectedTickers(prev =>
      prev.includes(value) ? prev.filter(ticker => ticker !== value) : [...prev, value]
    );
  };

const filterByDate = (itemDate) => {
  if (!selectedDate) return true;
  const now = new Date();
  const publishedDate = new Date(itemDate); // ✅ use itemDate instead of item.scraped_at
  if (selectedDate === 'today') {
    return publishedDate.toDateString() === now.toDateString();
  } else if (selectedDate === 'week') {
    const oneWeekAgo = new Date(now);
    oneWeekAgo.setDate(now.getDate() - 7);
    return publishedDate >= oneWeekAgo && publishedDate <= now;
  } else if (selectedDate === 'month') {
    const oneMonthAgo = new Date(now);
    oneMonthAgo.setMonth(now.getMonth() - 1);
    return publishedDate >= oneMonthAgo && publishedDate <= now;
  }
  return true;
};

const filterByTicker = (ticker) => {
  if (selectedTickers.length === 0) return true;
  if (!ticker) return false;
  const upperTicker = ticker.trim().toUpperCase();
  return selectedTickers.includes(upperTicker);
};

const filteredNews = news
  .filter((item) => item.title?.toLowerCase().includes(searchTerm.toLowerCase()))
  .filter((item) => selectedSentiments.length === 0 || selectedSentiments.includes(item.sentiment_label))
  .filter((item) => filterByDate(item.scraped_at)) 
  .filter((item) => filterByTicker(item.ticker));

  // Reset to first page when filters change
  useEffect(() => {
    setCurrentPage(1);
  }, [searchTerm, selectedSentiments, selectedDate, selectedTickers]);

  // Pagination calculations
  const totalPages = Math.ceil(filteredNews.length / itemsPerPage);
  const startIndex = (currentPage - 1) * itemsPerPage;
  const endIndex = startIndex + itemsPerPage;
  const currentNews = filteredNews.slice(startIndex, endIndex);

  const handlePageChange = (pageNumber) => {
    setCurrentPage(pageNumber);
  };

  const handlePrevPage = () => {
    if (currentPage > 1) {
      setCurrentPage(currentPage - 1);
    }
  };

  const handleNextPage = () => {
    if (currentPage < totalPages) {
      setCurrentPage(currentPage + 1);
    }
  };

  return (
    <div className="home-container">
      <div className={`menu-overlay ${isMenuOpen ? 'open' : ''}`} onClick={() => setIsMenuOpen(false)}></div>

      <header className="home-header">
        <div className="header-top">
          <div className="logo-title">
            <img src="/images/Logo.png" alt="FinAnswer Logo" className="home-logo" />
            <h1>Welcome, {user?.username} 👋</h1>
          </div>
          <input
            type="text"
            className="home-search-bar"
            placeholder="Search news..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            style={{
              marginLeft: '20px',
              padding: '10px 16px',
              borderRadius: '8px',
              border: '1px solid #ccc',
              fontSize: '18px',
              width: '455px',
            }}
          />
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
  <li><Link to="/home">Home</Link></li>
  <li><Link to="/chat">Learning Bot</Link></li>
  <li><Link to="/trading-assistant">Trading Bot</Link></li>
</ul>

      </nav>

      <main className="main-content">
        <aside className="filters-sidebar">
          <h3>Filter News</h3>

          <div className="filter-section">
            <h4>By Sentiment</h4>
            <div className="filter-options">
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
          <button className="filter-button" type="button" onClick={() => {
            setSelectedSentiments(tempSelectedSentiments);
            setSelectedDate(tempSelectedDate);
            setSelectedTickers(tempSelectedTickers);
          }}>Filter</button>
        </aside>

        <div className="news-section">
          <div className="news-header">
            <h2>Latest Financial News</h2>
            {filteredNews.length > 0 && (
              <div className="news-info">
                Showing {startIndex + 1}-{Math.min(endIndex, filteredNews.length)} of {filteredNews.length} articles
              </div>
            )}
          </div>
          {loading ? (
            <div className="loading">Loading news...</div>
          ) : (
            <>
              <div className="news-tiles-container">
                {filteredNews.length === 0 ? (
                  <div className="no-news">No news available at the moment.</div>
                ) : (
                  currentNews.map((item, index) => (
                  <div key={startIndex + index} className="news-tile">
                  <h3 className="news-title">
                  <a href={item.url} target="_blank" rel="noopener noreferrer">
                     {item.title}
                    </a>
                    </h3>
                    <p className="news-ticker">{item.ticker}</p>
                    <p className="news-date">🗓 {new Date(item.scraped_at).toLocaleDateString()}</p>
                       </div>
                    ))
                )}
              </div>
              
              {/* Pagination Controls */}
              {totalPages > 1 && (
                <div className="pagination">
                  <button 
                    className="pagination-btn" 
                    onClick={handlePrevPage} 
                    disabled={currentPage === 1}
                  >
                    ← Previous
                  </button>
                  
                  <div className="pagination-numbers">
                    {Array.from({ length: Math.min(5, totalPages) }, (_, i) => {
                      let pageNumber;
                      if (totalPages <= 5) {
                        pageNumber = i + 1;
                      } else if (currentPage <= 3) {
                        pageNumber = i + 1;
                      } else if (currentPage >= totalPages - 2) {
                        pageNumber = totalPages - 4 + i;
                      } else {
                        pageNumber = currentPage - 2 + i;
                      }
                      
                      return (
                        <button
                          key={pageNumber}
                          className={`pagination-number ${currentPage === pageNumber ? 'active' : ''}`}
                          onClick={() => handlePageChange(pageNumber)}
                        >
                          {pageNumber}
                        </button>
                      );
                    })}
                  </div>
                  
                  <button 
                    className="pagination-btn" 
                    onClick={handleNextPage} 
                    disabled={currentPage === totalPages}
                  >
                    Next →
                  </button>
                </div>
              )}
            </>
          )}
        </div>

       <div className="right-container">
  <h3 className="section-title">Top Finance Reads</h3>

  <div className="article-card">
    <h4>Know Your Client (KYC) Rule</h4>
    <p>This rule ensures advisors understand your risk tolerance before giving investment advice.</p>
    <a href="https://www.securities-administrators.ca/" target="_blank" rel="noopener noreferrer" className="view-pdf">
      Learn More →
    </a>
  </div>

  <div className="article-card">
    <h4>TFSA Stock Trading Guidelines</h4>
    <p>Buying stocks in a TFSA is allowed, but day-trading can lead to taxes. Great for long-term investing.</p>
    <a href="https://www.canada.ca/en/revenue-agency/services/tax/individuals/topics/tax-free-savings-account.html" target="_blank" rel="noopener noreferrer" className="view-pdf">
      Learn More →
    </a>
  </div>

  <div className="article-card">
    <h4>CRM2 – Transparency in Fees</h4>
    <p>CRM2 rules require your broker to clearly show all fees and investment performance annually.</p>
    <a href="https://www.getsmarteraboutmoney.ca/invest/investment-products/stocks/" target="_blank" rel="noopener noreferrer" className="view-pdf">
      Learn More →
    </a>
  </div>

  <div className="article-card">
    <h4>Insider Trading Laws</h4>
    <p>Using private info to trade stocks is illegal and punishable by fines or jail in Canada.</p>
    <a href="https://www.osc.ca/" target="_blank" rel="noopener noreferrer" className="view-pdf">
      Learn More →
    </a>
  </div>
</div>

      </main>
    </div>
  );
}

export default HomePage;
