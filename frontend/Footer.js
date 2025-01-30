// src/components/Footer.js
import React from 'react';

const Footer = () => {
  return (
    <footer className="footer">
      <p>&copy; 2025 WealthWiz. All rights reserved.</p>
      <nav>
        <a href="#privacy-policy">Privacy Policy</a> |{' '}
        <a href="#terms">Terms of Service</a>
      </nav>
    </footer>
  );
};

export default Footer;
