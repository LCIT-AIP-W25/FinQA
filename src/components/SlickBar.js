// SlickBar.js
import React from "react";
// import { FaComments, FaChartBar } from "react-icons/fa";
import "../styles/SlickBar.css";

import { FaBuilding, FaComments, FaChartBar } from "react-icons/fa";

function SlickBar({ onToggleCompany, onToggleChat, onToggleMetrics }) {
  return (
    <div className="slick-bar">
      <button onClick={onToggleCompany} title="Select Company | Download Reports | PDF Mode">
        <FaBuilding />
      </button>
      <button onClick={onToggleChat} title="Chat History">
        <FaComments />
      </button>
      <button onClick={onToggleMetrics} title="Available Financial Metrics">
        <FaChartBar />
      </button>
    </div>
  );
}

export default SlickBar;


