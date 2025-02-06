import React from "react";
import { Link } from "react-router-dom";
import './Chatbox.css'; // Make sure this includes the styles

const Signup = () => {
  return (
    <div className="signup-container">
      <div className="signup-form">
        <h2>Sign Up</h2>
        <form>
          <input type="text" placeholder="Full Name" required />
          <input type="email" placeholder="Email" required />
          <input type="password" placeholder="Password" required />
          <button type="submit" class="sub">Sign Up</button>
        </form>
        <p>
          Already have an account? <Link to="/login">Login</Link>
        </p>
        
        {/* Social Login with Logos */}
        <div className="social-login">
          <p>sign up with:</p>
          <div className="social-buttons">
            <a href="https://accounts.google.com/signin" target="_blank" rel="noopener noreferrer">
              <button className="google-btn">
                <i className="fab fa-google"></i> {/* Google Logo */}
              </button>
            </a>
            <a href="https://www.linkedin.com/login" target="_blank" rel="noopener noreferrer">
              <button className="linkedin-btn">
                <i className="fab fa-linkedin"></i> {/* LinkedIn Logo */}
              </button>
            </a>
            <a href="https://www.facebook.com/login" target="_blank" rel="noopener noreferrer">
              <button className="facebook-btn">
                <i className="fab fa-facebook-f"></i> {/* Facebook Logo */}
              </button>
            </a>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Signup;
