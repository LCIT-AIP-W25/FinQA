import * as React from "react";
import Accordion from "@mui/material/Accordion";
import AccordionSummary from "@mui/material/AccordionSummary";
import AccordionDetails from "@mui/material/AccordionDetails";
import Typography from "@mui/material/Typography";
import { useState } from "react";
// import ArrowDownwardIcon from '@mui/icons-material/ArrowDownward';
// import ArrowDropDownIcon from '@mui/icons-material/ArrowDropDown';
import {
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  Button,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
} from "@mui/material"; // Import necessary components

export default function AccordionExpandIcon() {
  const [activeIndex, setActiveIndex] = useState(null); // State to track the active item
  // Handle item click
  const handleItemClick = (index) => {
    if (activeIndex === index) {
      setActiveIndex(null); // Toggle off if the same item is clicked
    } else {
      setActiveIndex(index);
    }
  };
  const [activeAcc, setActiveAcc] = useState(null); // State to track the active item
  // Handle item click
  const handleActiveAcc = (index) => {
    if (activeAcc === index) {
      setActiveAcc(null); // Toggle off if the same item is clicked
    } else {
      setActiveAcc(index);
    }
  };
  const [isComapnyClicked, setIsCompanyClicked] = useState(false);
  const [companyAdded, setCompanyAdded] = useState(false); // To control when to show the selected company

  const [isClicked, setIsClicked] = useState(false);
  const handleClick = () => {
    setIsClicked((prev) => !prev); // Toggle state on click
  };
  const handleCompanyClick = () => {
    setIsCompanyClicked((prev) => !prev); // Toggle state on click
  };
  const [openModal, setOpenModal] = useState(false);
  const [selectedCompany, setSelectedCompany] = useState("");

  // Open and close the modal
  const handleOpenModal = () => setOpenModal(true);
  const handleCloseModal = () => setOpenModal(false);

  const handleItemClicked = (index) => setActiveIndex(index);

  // Handle the company selection from dropdown
  const handleCompanyChange = (event) => {
    setSelectedCompany(event.target.value);
  };
  const handleAddCompany = () => {
    // Update Typography with the selected company
    if (selectedCompany) {
        setCompanyAdded(true); // Show the company after clicking "Add"

        handleItemClicked(3); // Optional: Change active index to highlight the Typography
    }
    handleCloseModal(); // Close the dialog
  };


  const companies = ["Company1", "Company2", "Company3", "Company4","Company5","Company6","Company7","Company8","Company9","Company10","Company11","Company12","Company13","Company14","Company15","Company16"];

  return (
    <div>
      <Accordion>
        <AccordionSummary
          onClick={handleCompanyClick}
          className={`cursor-pointer p-2 rounded-lg flex items-center transition-all duration-300 ${
            isComapnyClicked ? "bg-blue-500 text-white" : "bg-transparent"
          }`}
          style={{
            backgroundColor: isComapnyClicked ? "#2B2830" : "transparent", // Fallback for non-Tailwind setups
            color: isComapnyClicked ? "white" : "white",
          }}
          expandIcon={
            <svg
              viewBox="0 0 24 24"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
              width="24"
              height="24"
            >
              <path
                d="M6 9L12 15L18 9"
                stroke="white"
                strokeWidth="1.5"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
            </svg>
          }
          aria-controls="panel1-content"
          id="panel1-header"
        >
          <Typography
            component="span"
            style={{
              backgroundColor: isComapnyClicked ? "#2B2830" : "transparent", // Fallback for non-Tailwind setups
              color: isComapnyClicked ? "white" : "white",
            }}
          >
            <svg
              className="home-svg mr-2"
              viewBox="0 0 16 16"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                d="M1 6V15H6V11C6 9.89543 6.89543 9 8 9C9.10457 9 10 9.89543 10 11V15H15V6L8 0L1 6Z"
                fill="currentColor"
              ></path>
            </svg>
            Select Companies
          </Typography>
        </AccordionSummary>
        <Button
          onClick={handleOpenModal}
          style={{
            color: "white",
            fontWeight: "600", // Slightly bold text for emphasis
            padding: "8px 16px", // Consistent padding
            borderRadius: "4px", // Rounded corners for a modern look
            display: "flex",
            alignItems: "center",
            gap: "8px", // Space between icon and text
            transition: "all 0.3s ease", // Smooth transition for hover effect
          }}
          // onMouseOver={(e) => e.target.style.backgroundColor = '#303f9f'}  // Darker blue on hover
          // onMouseOut={(e) => e.target.style.backgroundColor = '#3f51b5'}  // Reset background color
        >
          Add New
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="18"
            height="18"
            fill="none"
            viewBox="0 0 24 24"
            style={{ verticalAlign: "middle" }}
          >
            <path
              fill="currentColor"
              d="M12 2C12.5523 2 13 2.44772 13 3V11H21C21.5523 11 22 11.4477 22 12C22 12.5523 21.5523 13 21 13H13V21C13 21.5523 12.5523 22 12 22C11.4477 22 11 21.5523 11 21V13H3C2.44772 13 2 12.5523 2 12C2 11.4477 2.44772 11 3 11H11V3C11 2.44772 11.4477 2 12 2Z"
            />
          </svg>
        </Button>
        <AccordionDetails>
          <Typography
            className={`type-txt txt-typ ${activeIndex === 0 ? "active" : ""}`}
            onClick={() => handleItemClick(0)}
          >
            - Company1
          </Typography>
          <Typography
            className={`mt-2 type-txt ${activeIndex === 1 ? "active" : ""}`}
            onClick={() => handleItemClick(1)}
          >
            - Company2
          </Typography>
          <Typography
            className={`mt-2 type-txt ${activeIndex === 2 ? "active" : ""}`}
            onClick={() => handleItemClick(2)}
          >
            - Company3
          </Typography>
          <Typography
            className={`mt-2 type-txt ${activeIndex === 3 ? "active" : ""}`}
            onClick={() => handleItemClick(3)}
          >
            - Company4
          </Typography>
          {companyAdded && selectedCompany && (
        <Typography
          className={`mt-2 type-txt ${activeIndex === selectedCompany ? "active" : ""}`}
          onClick={() => handleItemClicked(selectedCompany)}
        >
          - {selectedCompany}
        </Typography>
      )}
        </AccordionDetails>
      </Accordion>
      <Dialog open={openModal} onClose={handleCloseModal}>
        <DialogTitle style={{fontWeight:"700"}}>Company Selection</DialogTitle>
        <DialogContent>

          {/* Dropdown for companies */}
          <FormControl fullWidth>
            <InputLabel id="company-select-label">Company</InputLabel>
            <Select
              labelId="company-select-label"
              id="company-select"
              value={selectedCompany}
              label="Company"
              onChange={handleCompanyChange}
            >
              {companies.map((company, index) => (
                <MenuItem key={index} value={company}>
                  {company}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
        </DialogContent>
        <DialogActions>
        <Button onClick={handleAddCompany} color="primary">
            Add
          </Button>
          <Button onClick={handleCloseModal} color="primary">
            Close
          </Button>
        </DialogActions>
      </Dialog>
      <Accordion defaultExpanded>
        <AccordionSummary
          onClick={handleClick}
          className={`cursor-pointer p-2 rounded-lg flex items-center transition-all duration-300 ${
            !isClicked ? "bg-blue-500 text-white" : "bg-transparent"
          }`}
          style={{
            backgroundColor: !isClicked ? "#2B2830" : "transparent", // Fallback for non-Tailwind setups
            color: !isClicked ? "white" : "white",
          }}
          expandIcon={
            <svg
              viewBox="0 0 24 24"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
              width="24"
              height="24"
            >
              <path
                d="M6 9L12 15L18 9"
                stroke="white"
                strokeWidth="1.5"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
            </svg>
          }
          aria-controls="panel2-content"
          id="panel2-header"
        >
          <Typography component="span">
            <svg
              className="home-svg"
              viewBox="0 0 24 24"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <g id="SVGRepo_bgCarrier" stroke-width="0"></g>
              <g
                id="SVGRepo_tracerCarrier"
                stroke-linecap="round"
                stroke-linejoin="round"
              ></g>
              <g id="SVGRepo_iconCarrier">
                {" "}
                <path
                  d="M8 9H16"
                  stroke="#ffffff"
                  stroke-width="1.5"
                  stroke-linecap="round"
                ></path>{""}
                <path
                  d="M8 12.5H13.5"
                  stroke="#ffffff"
                  stroke-width="1.5"
                  stroke-linecap="round"
                ></path>{" "}
                <path
                  d="M13.0867 21.3877L13.7321 21.7697L13.0867 21.3877ZM13.6288 20.4718L12.9833 20.0898L13.6288 20.4718ZM10.3712 20.4718L9.72579 20.8539H9.72579L10.3712 20.4718ZM10.9133 21.3877L11.5587 21.0057L10.9133 21.3877ZM1.25 10.5C1.25 10.9142 1.58579 11.25 2 11.25C2.41421 11.25 2.75 10.9142 2.75 10.5H1.25ZM3.07351 15.6264C2.915 15.2437 2.47627 15.062 2.09359 15.2205C1.71091 15.379 1.52918 15.8177 1.68769 16.2004L3.07351 15.6264ZM7.78958 18.9915L7.77666 19.7413L7.78958 18.9915ZM5.08658 18.6194L4.79957 19.3123H4.79957L5.08658 18.6194ZM21.6194 15.9134L22.3123 16.2004V16.2004L21.6194 15.9134ZM16.2104 18.9915L16.1975 18.2416L16.2104 18.9915ZM18.9134 18.6194L19.2004 19.3123H19.2004L18.9134 18.6194ZM19.6125 2.7368L19.2206 3.37628L19.6125 2.7368ZM21.2632 4.38751L21.9027 3.99563V3.99563L21.2632 4.38751ZM4.38751 2.7368L3.99563 2.09732V2.09732L4.38751 2.7368ZM2.7368 4.38751L2.09732 3.99563H2.09732L2.7368 4.38751ZM9.40279 19.2098L9.77986 18.5615L9.77986 18.5615L9.40279 19.2098ZM13.7321 21.7697L14.2742 20.8539L12.9833 20.0898L12.4412 21.0057L13.7321 21.7697ZM9.72579 20.8539L10.2679 21.7697L11.5587 21.0057L11.0166 20.0898L9.72579 20.8539ZM12.4412 21.0057C12.2485 21.3313 11.7515 21.3313 11.5587 21.0057L10.2679 21.7697C11.0415 23.0767 12.9585 23.0767 13.7321 21.7697L12.4412 21.0057ZM10.5 2.75H13.5V1.25H10.5V2.75ZM21.25 10.5V11.5H22.75V10.5H21.25ZM7.8025 18.2416C6.54706 18.2199 5.88923 18.1401 5.37359 17.9265L4.79957 19.3123C5.60454 19.6457 6.52138 19.7197 7.77666 19.7413L7.8025 18.2416ZM1.68769 16.2004C2.27128 17.6093 3.39066 18.7287 4.79957 19.3123L5.3736 17.9265C4.33223 17.4951 3.50486 16.6678 3.07351 15.6264L1.68769 16.2004ZM21.25 11.5C21.25 12.6751 21.2496 13.5189 21.2042 14.1847C21.1592 14.8438 21.0726 15.2736 20.9265 15.6264L22.3123 16.2004C22.5468 15.6344 22.6505 15.0223 22.7007 14.2868C22.7504 13.5581 22.75 12.6546 22.75 11.5H21.25ZM16.2233 19.7413C17.4786 19.7197 18.3955 19.6457 19.2004 19.3123L18.6264 17.9265C18.1108 18.1401 17.4529 18.2199 16.1975 18.2416L16.2233 19.7413ZM20.9265 15.6264C20.4951 16.6678 19.6678 17.4951 18.6264 17.9265L19.2004 19.3123C20.6093 18.7287 21.7287 17.6093 22.3123 16.2004L20.9265 15.6264ZM13.5 2.75C15.1512 2.75 16.337 2.75079 17.2619 2.83873C18.1757 2.92561 18.7571 3.09223 19.2206 3.37628L20.0044 2.09732C19.2655 1.64457 18.4274 1.44279 17.4039 1.34547C16.3915 1.24921 15.1222 1.25 13.5 1.25V2.75ZM22.75 10.5C22.75 8.87781 22.7508 7.6085 22.6545 6.59611C22.5572 5.57256 22.3554 4.73445 21.9027 3.99563L20.6237 4.77938C20.9078 5.24291 21.0744 5.82434 21.1613 6.73809C21.2492 7.663 21.25 8.84876 21.25 10.5H22.75ZM19.2206 3.37628C19.7925 3.72672 20.2733 4.20752 20.6237 4.77938L21.9027 3.99563C21.4286 3.22194 20.7781 2.57144 20.0044 2.09732L19.2206 3.37628ZM10.5 1.25C8.87781 1.25 7.6085 1.24921 6.59611 1.34547C5.57256 1.44279 4.73445 1.64457 3.99563 2.09732L4.77938 3.37628C5.24291 3.09223 5.82434 2.92561 6.73809 2.83873C7.663 2.75079 8.84876 2.75 10.5 2.75V1.25ZM2.75 10.5C2.75 8.84876 2.75079 7.663 2.83873 6.73809C2.92561 5.82434 3.09223 5.24291 3.37628 4.77938L2.09732 3.99563C1.64457 4.73445 1.44279 5.57256 1.34547 6.59611C1.24921 7.6085 1.25 8.87781 1.25 10.5H2.75ZM3.99563 2.09732C3.22194 2.57144 2.57144 3.22194 2.09732 3.99563L3.37628 4.77938C3.72672 4.20752 4.20752 3.72672 4.77938 3.37628L3.99563 2.09732ZM11.0166 20.0898C10.8136 19.7468 10.6354 19.4441 10.4621 19.2063C10.2795 18.9559 10.0702 18.7304 9.77986 18.5615L9.02572 19.8582C9.07313 19.8857 9.13772 19.936 9.24985 20.0898C9.37122 20.2564 9.50835 20.4865 9.72579 20.8539L11.0166 20.0898ZM7.77666 19.7413C8.21575 19.7489 8.49387 19.7545 8.70588 19.7779C8.90399 19.7999 8.98078 19.832 9.02572 19.8582L9.77986 18.5615C9.4871 18.3912 9.18246 18.3215 8.87097 18.287C8.57339 18.2541 8.21375 18.2487 7.8025 18.2416L7.77666 19.7413ZM14.2742 20.8539C14.4916 20.4865 14.6287 20.2564 14.7501 20.0898C14.8622 19.936 14.9268 19.8857 14.9742 19.8582L14.2201 18.5615C13.9298 18.7304 13.7204 18.9559 13.5379 19.2063C13.3646 19.4441 13.1864 19.7468 12.9833 20.0898L14.2742 20.8539ZM16.1975 18.2416C15.7862 18.2487 15.4266 18.2541 15.129 18.287C14.8175 18.3215 14.5129 18.3912 14.2201 18.5615L14.9742 19.8582C15.0192 19.832 15.096 19.7999 15.2941 19.7779C15.5061 19.7545 15.7842 19.7489 16.2233 19.7413L16.1975 18.2416Z"
                  fill="#ffffff"
                ></path>{" "}
              </g>
            </svg>
            Chat History
          </Typography>
        </AccordionSummary>
        <AccordionDetails>
          <Typography
            className={`type-txt txt-typ ${activeAcc === 0 ? "active" : ""}`}
            onClick={() => handleActiveAcc(0)}
          >
            - History1
          </Typography>
          <Typography
            className={`type-txt mt-2 txt-typ ${
              activeAcc === 1 ? "active" : ""
            }`}
            onClick={() => handleActiveAcc(1)}
          >
            - History2
          </Typography>
          <Typography
            className={`type-txt mt-2 txt-typ ${
              activeAcc === 2 ? "active" : ""
            }`}
            onClick={() => handleActiveAcc(2)}
          >
            - History3
          </Typography>
          <Typography
            className={`type-txt mt-2 txt-typ ${
              activeAcc === 3 ? "active" : ""
            }`}
            onClick={() => handleActiveAcc(3)}
          >
            - History4
          </Typography>
        </AccordionDetails>
      </Accordion>
    </div>
  );
}
