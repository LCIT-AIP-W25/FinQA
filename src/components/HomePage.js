import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import axios from 'axios';
import '../styles/HomePage.css';

function HomePage() {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [news, setNews] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedSources, setSelectedSources] = useState([]);
  const [selectedDate, setSelectedDate] = useState('');
  const user = JSON.parse(localStorage.getItem("user"));
  const navigate = useNavigate();

  useEffect(() => {
    fetchNews();
  }, []);

  const fetchNews = async () => {
    try {
      const apiUrl = `${process.env.REACT_APP_AUTH_API_URL}/api/yahoo_news`;
      const response = await axios.get(apiUrl);
      if (Array.isArray(response.data)) {
        setNews(response.data);
      } else {
        console.error('Invalid news data format:', response.data);
        setNews([]);
      }
      setLoading(false);
    } catch (error) {
      console.error('Error fetching news:', error.message, error.response);
      setNews([]);
      setLoading(false);
    }
  };

  const toggleMenu = () => setIsMenuOpen(!isMenuOpen);
  const handleCompanyReports = () => navigate('/chat', { state: { openPanel: 'company' } });
  const handleChatHistory = () => navigate('/chat', { state: { openPanel: 'history' } });
  const handleMetrics = () => navigate('/chat', { state: { openPanel: 'metrics' } });
  const handleSignOut = () => {
    localStorage.clear();
    window.location.href = '/login';
  };

  const handleSourceChange = (e) => {
    const value = e.target.value;
    setSelectedSources(prev =>
      prev.includes(value) ? prev.filter(source => source !== value) : [...prev, value]
    );
  };

  const handleDateChange = (e) => setSelectedDate(e.target.value);

  const filterByDate = (itemDate) => {
    if (!selectedDate) return true;
    const now = new Date();
    const publishedDate = new Date(itemDate);
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

      {/* Hamburger icon (shown only when menu is closed) */}
      {!isMenuOpen && (
        <button className="menu-toggle" onClick={toggleMenu}>
          <span className="menu-icon"></span>
        </button>
      )}

      <nav className={`nav-menu ${isMenuOpen ? 'open' : ''}`}>
        {/* Close icon (X) shown only when menu is open */}
        {isMenuOpen && (
          <button className="menu-toggle" onClick={toggleMenu}>
            <span className="menu-icon open"></span>
          </button>
        )}

        <ul>
          <li><Link to="/home">Home</Link></li>
          <li><Link to="/chat">AI Chat</Link></li>
          <li><Link to="/pdf-chat">PDF Analysis</Link></li>

          <li className="menu-category">Chat Tools</li>
          <li><button className="menu-btn" onClick={handleCompanyReports}>Company Reports</button></li>
          <li><button className="menu-btn" onClick={handleChatHistory}>Chat History</button></li>
          <li><button className="menu-btn" onClick={handleMetrics}>Metrics</button></li>

          <li className="menu-category">Account</li>
          <li><button className="menu-btn sign-out" onClick={handleSignOut}>Sign Out</button></li>
        </ul>
      </nav>

      <main className="main-content">
        <aside className="filters-sidebar">
          <h3>Filter News</h3>

          <div className="filter-section">
            <h4>By Source</h4>
            <div className="filter-options">
              {['yahoo-finance', 'reuters', 'bloomberg'].map((source) => (
                <label className="filter-option" key={source}>
                  <input
                    type="checkbox"
                    name="source"
                    value={source}
                    checked={selectedSources.includes(source)}
                    onChange={handleSourceChange}
                  />
                  {source.replace('-', ' ').replace(/\b\w/g, c => c.toUpperCase())}
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
                    checked={selectedDate === option}
                    onChange={handleDateChange}
                  />
                  {option === '' ? 'All' : option.charAt(0).toUpperCase() + option.slice(1)}
                </label>
              ))}
            </div>
          </div>
        </aside>

        <div className="news-section">
          <h2>Latest Financial News</h2>
          {loading ? (
            <div className="loading">Loading news...</div>
          ) : news.length === 0 ? (
            <div className="no-news">No news available at the moment.</div>
          ) : (
            <div className="news-tiles-container">
              {news
                .filter((item) => item.title.toLowerCase().includes(searchTerm.toLowerCase()))
                .filter((item) => selectedSources.length === 0 || selectedSources.includes(item.source.toLowerCase()))
                .filter((item) => filterByDate(item.published_date))
                .map((item, index) => (
                  <div key={index} className="news-tile">
                    <h3 className="news-title">
                      <a href={item.link} target="_blank" rel="noopener noreferrer">
                        {item.title}
                      </a>
                    </h3>
                    <p className="news-source">🔹 {item.source}</p>
                    <p className="news-date">🗓 {new Date(item.published_date).toLocaleDateString()}</p>
                  </div>
                ))}
            </div>
          )}
        </div>
      </main>
    </div>
  );
}

export default HomePage;
