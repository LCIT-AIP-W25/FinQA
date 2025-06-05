import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import axios from 'axios';
import '../styles/HomePage.css';

function HomePage() {
    const [isMenuOpen, setIsMenuOpen] = useState(false);
    const [news, setNews] = useState([]);
    const [loading, setLoading] = useState(true);
    const user = JSON.parse(localStorage.getItem("user"));
    const navigate = useNavigate();

    useEffect(() => {
        fetchNews();
    }, []);

    const fetchNews = async () => {
        try {
            const response = await axios.get(`${process.env.REACT_APP_AUTH_API_URL}/api/yahoo_news`);
            setNews(response.data);
            setLoading(false);
        } catch (error) {
            console.error('Error fetching news:', error);
            setLoading(false);
        }
    };

    const toggleMenu = () => {
        setIsMenuOpen(!isMenuOpen);
    };

    const handleCompanyReports = () => {
        setIsMenuOpen(false);
        navigate('/chat', { state: { openPanel: 'company' } });
    };

    const handleChatHistory = () => {
        setIsMenuOpen(false);
        navigate('/chat', { state: { openPanel: 'history' } });
    };

    const handleMetrics = () => {
        setIsMenuOpen(false);
        navigate('/chat', { state: { openPanel: 'metrics' } });
    };

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
                        <img src="/images/wes.png" alt="WealthWiz Logo" className="home-logo" />
                        <h1>Welcome, {user?.username} 👋</h1>
                    </div>
                    <button className="menu-toggle" onClick={toggleMenu}>
                        <span className={`menu-icon ${isMenuOpen ? 'open' : ''}`}></span>
                    </button>
                </div>
            </header>

            <nav className={`nav-menu ${isMenuOpen ? 'open' : ''}`}>
                <ul>
                    <li className="menu-category">Main Navigation</li>
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

            <main className="home-features">
                <div className="news-section">
                    <h2>Latest Financial News</h2>
                    {loading ? (
                        <div className="loading">Loading news...</div>
                    ) : (
                        <div className="news-table-container">
                            <table className="news-table">
                                <thead>
                                    <tr>
                                        <th>Title</th>
                                        <th>Source</th>
                                        <th>Date</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {news.map((item, index) => (
                                        <tr key={index}>
                                            <td>
                                                <a href={item.link} target="_blank" rel="noopener noreferrer">
                                                    {item.title}
                                                </a>
                                            </td>
                                            <td>{item.source}</td>
                                            <td>{new Date(item.published_date).toLocaleDateString()}</td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    )}
                </div>
            </main>
        </div>
    );
}

export default HomePage;