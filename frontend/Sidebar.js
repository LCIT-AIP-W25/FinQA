import React, { useState } from "react";
import { Avatar, Dialog, DialogContent, DialogTitle, IconButton } from "@mui/material"; // Remove DialogActions and Button
import { Close } from "@mui/icons-material"; // Import Close icon
import ChatHistory from "./ChatHistory";

const Sidebar = () => {
  const [isDialogOpen, setIsDialogOpen] = useState(false); // State to control modal
  const [selectedCompanies, setSelectedCompanies] = useState([]);

  const handleDialogOpen = () => {
    setIsDialogOpen(true);
  };

  const handleDialogClose = () => {
    setIsDialogOpen(false);
  };

  const handleCompanySelect = (company) => {
    setSelectedCompanies((prev) => {
      // If the company is already selected, remove it
      if (prev.includes(company)) {
        return prev.filter((item) => item !== company);
      } else if (prev.length < 4) {
        // Add the company only if the limit of 4 companies has not been reached
        return [...prev, company];
      }
      return prev; // If limit is reached, don't add the company
    });
  };

  return (
    <div className="sidebar">
      <div className="profile">
        <Avatar src="/profile-pic.jpg" />
        <h3>Komal Negah</h3>
      </div>

      <div className="favorites">
        <h4 onClick={handleDialogOpen}> Select Companies</h4>
        <ul>
          {selectedCompanies.length === 0 ? (
            <li>No companies selected</li>
          ) : (
            selectedCompanies.map((company, index) => <li key={index}>{company} ⭐</li>)
          )}
        </ul>
      </div>
<br></br>
      <div className="chat-history">
        <ChatHistory />
      </div>

      {/* Dialog to select favorite companies */}
      <Dialog open={isDialogOpen} onClose={handleDialogClose}>
        <DialogTitle>
          <div className="dialog-header">
            <h3>⭐ Choose your favorites</h3>
           
            <br />
            <IconButton
              edge="end"
              color="inherit"
              onClick={handleDialogClose}
              aria-label="close"
              sx={{ position: "absolute", right: 8, top: 8 }}
            >
              <Close />
            </IconButton>
          </div>
        </DialogTitle>
        <DialogContent>
          <div className="company-list">
            {["Apple", "Microsoft", "Tesla", "Amazon", "Google", "Meta"].map((company) => (
              <div className="company-item" key={company}>
                <input
                  type="checkbox"
                  checked={selectedCompanies.includes(company)}
                  onChange={() => handleCompanySelect(company)}
                  id={company.toLowerCase()}
                  disabled={selectedCompanies.length >= 4 && !selectedCompanies.includes(company)} // Disable if 4 companies are selected
                />
                <label htmlFor={company.toLowerCase()}>{company}</label>
              </div>
            ))}
          </div>
        </DialogContent>
      </Dialog>
    </div>
  );
};

export default Sidebar;
