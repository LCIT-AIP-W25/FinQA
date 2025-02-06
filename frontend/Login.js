import React from "react";
import { useNavigate } from "react-router-dom";
import { Link } from "react-router-dom";
import { FcGoogle } from "react-icons/fc";
import { FaFacebook } from "react-icons/fa";

const Login = () => {
  const navigate = useNavigate();

  const handleLogin = (e) => {
    e.preventDefault();
    navigate("/dashboard");
  };

  return (
    <div className="login-container">
      <div className="login-left">
        <div className="balance-card">
          <h4>Current Balance</h4>
          <p className="balance-amount">$24,359</p>
        </div>
        <div className="transaction-card">
          <button className="new-transaction-btn">+ New Transaction</button>
          <p>or upload <span className="file-upload">.xls file</span></p>
        </div>
      </div>
      <div className="login-right">
        <h2>Welcome back!</h2>
        <p>Start managing your finance faster and better</p>
        <form onSubmit={handleLogin} className="login-form">
          <div className="input-group">
            <input type="email" placeholder="you@example.com" required />
          </div>
          <div className="input-group">
            <input type="password" placeholder="At least 8 characters" required />
          </div>
          <button type="submit" className="login-btn">Login</button>
          <div className="forgot-password">
            <Link to="/forgot-password">Forgot password?</Link>
          </div>
        </form>
        <div className="login-divider">or</div>
        <div className="social-login">
          <button className="google-btn">
            <FcGoogle className="icon" /> Google
          </button>
          <button className="facebook-btn">
            <FaFacebook className="icon" /> Facebook
          </button>
        </div>
        <p className="signup-text">
          Don’t have an account? <Link to="/signup">Sign Up</Link>
        </p>
      </div>
    </div>
  );
};

export default Login;
