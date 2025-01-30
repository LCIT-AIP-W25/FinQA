import React from 'react';

const Header = ({ darkMode, toggleTheme, logo }) => {
  return (
    <header className="header">
      <img src={logo} alt="Logo" className="logo" />
      <h1>Financial Chatbot</h1>
      <button className="theme-toggle" onClick={toggleTheme}>
        {darkMode ? '🌙 Dark Mode' : '☀️ Light Mode'}
      </button>
    </header>
  );
};

export default Header;
