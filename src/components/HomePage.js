import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import axios from 'axios';
import '../styles/HomePage.css';

import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import axios from 'axios';
import '../styles/HomePage.css';

function HomePage() {
    const [isMenuOpen, setIsMenuOpen] = useState(false);
    const [news, setNews] = useState([]);
    const [loading, setLoading] = useState(true);
    const [searchTerm, setSearchTerm] = useState('');
    const user = JSON.parse(localStorage.getItem("user"));
    const navigate = useNavigate();

    useEffect(() => {
        fetchNews();
    }, []);

    const fetchNews = async () => {
        try {
            console.log('Fetching news...');
            const apiUrl = `${process.env.REACT_APP_AUTH_API_URL}/api/yahoo_news`;
            console.log('API URL:', apiUrl);
            const response = await axios.get(apiUrl);
            console.log('News data received:', response.data);

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
                    style={{ marginLeft: '20px', padding: '6px 12px', borderRadius: '6px', border: '1px solid #ccc', fontSize: '16px' }}
                />
                <button className="menu-toggle" onClick={toggleMenu} style={{ position: 'relative' }}>
                    <span className={`menu-icon ${isMenuOpen ? 'open' : ''}`} style={{ position: 'relative', right: '0', top: '0', transform: 'none', transition: 'none' }}></span>
                </button>
            </div>
        </header>

            <nav className={`nav-menu ${isMenuOpen ? 'open' : ''}`}>
                <ul>
                    {/* Removed the Main Navigation category label as requested */}
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
                        <label className="filter-option">
                            <input type="checkbox" name="source" value="yahoo-finance" />
                            Yahoo Finance
                        </label>
                        <label className="filter-option">
                            <input type="checkbox" name="source" value="reuters" />
                            Reuters
                        </label>
                        <label className="filter-option">
                            <input type="checkbox" name="source" value="bloomberg" />
                            Bloomberg
                        </label>
                    </div>
                </div>

                <div className="filter-section">
                    <h4>By Date</h4>
                    <div className="filter-options">
                        <label className="filter-option">
                            <input type="radio" name="date" value="today" />
                            Today
                        </label>
                        <label className="filter-option">
                            <input type="radio" name="date" value="week" />
                            This Week
                        </label>
                        <label className="filter-option">
                            <input type="radio" name="date" value="month" />
                            This Month
                        </label>
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
                        {news.map((item, index) => (
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
