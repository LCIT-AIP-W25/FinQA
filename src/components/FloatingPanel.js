

// FloatingPanel.js
import React from "react";
import "../styles/FloatingPanel.css";

function FloatingPanel({ children, onClose, position = "left" }) {
  return (
    <div className={`floating-panel ${position}`}>
      <div className="floating-panel-header">
        <button onClick={onClose} className="close-btn">✘</button>
      </div>
      <div className="floating-panel-body">
        {children}
      </div>
    </div>
  );
}

export default FloatingPanel;
