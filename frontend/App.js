import React from "react";
import { BrowserRouter as Router, Route, Routes, Navigate } from "react-router-dom"; // Import Navigate here
import Login from "./components/Login";
import Signup from "./components/Signup";
import Dashboard from "./pages/Dashboard";
import './components/Chatbox.css';

function App() {
  return (
    <Router>
      <div className="app">
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<Signup />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/" element={<Navigate to="/login" />} /> {/* Navigate is now imported */}
        </Routes>
      </div>
    </Router>
  );
}

export default App;
