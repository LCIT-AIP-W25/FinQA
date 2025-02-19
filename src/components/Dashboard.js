
import 'bootstrap/dist/css/bootstrap.min.css';
import Accordion from "react-bootstrap/Accordion";
import AccordionExpandIcon from './AccordionExpandIcon';
import React, { useEffect, useState } from "react";
import 'bootstrap/dist/js/bootstrap.bundle.min.js';
import { useNavigate } from 'react-router-dom';
import { Link } from 'react-router-dom';

function Dashboard() {
  const [anchorEl, setAnchorEl] = useState(null);
  const [showHistory, setShowHistory] = useState(false)
  const [showTopic, setShowTopic] = useState(false)
  const [message, setMessage] = useState(""); // State for storing user input

  const [windowWidth, setWindowWidth] = useState(window.innerWidth)
  const navigate = useNavigate(); // Hook to navigate

  const open = Boolean(anchorEl);

  useEffect(() => {
    const handleResize = () => {
      setWindowWidth(window.innerWidth)
    }
    window.addEventListener("resize", handleResize)
    return () => {
      window.removeEventListener("resize", handleResize)
    }
  }, [])

  const isMobile = windowWidth <= 992

  useEffect(() => {
    if (windowWidth > 767) {
      setShowHistory(true)
      setShowTopic(true)
    }
    if (windowWidth < 992) {
      setShowHistory(false)
      setShowTopic(false)
    }

  }, [windowWidth])

  const handleClick = (event) => {
    setAnchorEl(event.currentTarget);
  };


  const handleSignOut = () => {
    // Clear authentication state (example: remove token from localStorage)
    // localStorage.removeItem('authToken');

    // Redirect to login page
    navigate('/login');
  };
  const [isFocused, setIsFocused] = useState(false);

  const handleFocus = () => {
    setTimeout(() => {
      setIsFocused(true);
    }, 1000); // Adjust the delay time (in milliseconds) as needed
  };

  const handleBlur = () => {
    setIsFocused(false);
  };
  return (
    <>

      <section className="chat-bot">

        <div className="container-fluid">


          <div className='row head-chat'>
          <div className='d-flex justify-space-between'>
          <button  disabled={showTopic} className={`trans-btn ${!isMobile ? "d-set text-black" : ""}`} onClick={() => setShowHistory((curr) => !curr)}>
                <svg className='img-res' 
                viewBox="0 0 24 24" fill="black"
                color='black'
                xmlns="http://www.w3.org/2000/svg">
                  <g id="SVGRepo_bgCarrier" stroke-width="0"></g>
                  <g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <path d="M4 6H20M4 12H20M4 18H20" stroke="#fafafa" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path> </g></svg>
              </button>
                   </div>  
            <div className='col-6'>
              {/* <p className="chat-txt">AI-CHATBOT</p> */}
<Link to="/dashboard">

              <img className='we-img' src='/images/wes.png' alt=''></img>


              </Link>

            </div>
            <div className='col-6 d-flex justify-content-end align-items-center text-end'>
              <p className='text-white m-0 name-txt inline-block'>
                Komal Nigah
              </p>


              <div className="dropdown inline-block position-relative" style={{ cursor: "pointer" }}>
                <img className='inline-block img-profile' src='/images/user.png' id="dropdownMenuButton" aria-expanded="false" data-bs-toggle="dropdown" alt="User" />
                {/* <ul className="dropdown-menu position-absolute" aria-labelledby="dropdownMenuButton">
                  <li><a class="dropdown-item" href="#">My Profile</a></li>
                  <li> <a className="dropdown-item" href="#" onClick={handleSignOut}>
                    Sign Out
                  </a></li>
                </ul> */}

                <ul className="dropdown-menu position-absolute p-3" aria-labelledby="dropdownMenuButton" style={{ minWidth: "250px", textAlign: "center" }}>
                  <li>
                    <div className="d-flex flex-column align-items-center">
                      <div className="rounded-circle bg-secondary text-white d-flex justify-content-center align-items-center" style={{ width: "50px", height: "50px", fontSize: "24px" }}>
                        K
                      </div>
                      <p className="mt-2 mb-1 fw-bold">Hi, Komal!</p>
                    </div>
                  </li>
                  {/* <li>
                    <a className="dropdown-item text-primary fw-bold" href="#">Manage your Google Account</a>
                  </li> */}
                  <li><hr className="dropdown-divider" /></li>
                  <li>
                    <a className="dropdown-item" href="#">My Profile</a>
                  </li>
                  <li className='mt-3'>
                    <a className="dropdown-item text-danger" href="#" onClick={handleSignOut}>
                      Sign Out
                    </a>
                  </li>
                </ul>


              </div>




              <button disabled={showHistory} className={`trans-btn btn-trans- ${!isMobile ? "d-set" : ""}`} onClick={() => setShowTopic((curr) => !curr)}>
                <svg className='img-res' viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <path d="M4 6H20M4 12H20M4 18H20" stroke="#fafafa" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path> </g></svg>
              </button>

            </div>
          </div>




          <div className="row chat-row">


            <div className={`col-2 bg-chat ${!showHistory ? "d-set" : ""}`}>

              <AccordionExpandIcon />

            </div>
            <div
              className={`col-8 d-flex justify-content-center ${isFocused ? 'align-items-end pb-4' : 'align-items-center'}`}
              style={{ position: "relative", flexWrap: 'wrap' }}
            >
              <div className='message-body'>
                {message}
              </div>
              <div className='d-flex justify-content-center box-chat'>
                <img className='img-drop' src='/images/nsd.svg' alt="Icon" onClick={handleFocus} />
                <input
                  placeholder='Send a message'
                  className='inp-bot text-black'
                  onChange={(e) => setMessage(e.target.value)}

                />
              </div>
            </div>
            <div className={`col-2 bg-chat chat-b ${!showTopic ? "d-set" : ""}`}>

              <div className='d-flex align-items-center'>

                <div className='d-flex chat-back'>

                  <svg className='home-svg' viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <path d="M8 9H16" stroke="#ffffff" stroke-width="1.5" stroke-linecap="round"></path> <path d="M8 12.5H13.5" stroke="#ffffff" stroke-width="1.5" stroke-linecap="round"></path> <path d="M13.0867 21.3877L13.7321 21.7697L13.0867 21.3877ZM13.6288 20.4718L12.9833 20.0898L13.6288 20.4718ZM10.3712 20.4718L9.72579 20.8539H9.72579L10.3712 20.4718ZM10.9133 21.3877L11.5587 21.0057L10.9133 21.3877ZM1.25 10.5C1.25 10.9142 1.58579 11.25 2 11.25C2.41421 11.25 2.75 10.9142 2.75 10.5H1.25ZM3.07351 15.6264C2.915 15.2437 2.47627 15.062 2.09359 15.2205C1.71091 15.379 1.52918 15.8177 1.68769 16.2004L3.07351 15.6264ZM7.78958 18.9915L7.77666 19.7413L7.78958 18.9915ZM5.08658 18.6194L4.79957 19.3123H4.79957L5.08658 18.6194ZM21.6194 15.9134L22.3123 16.2004V16.2004L21.6194 15.9134ZM16.2104 18.9915L16.1975 18.2416L16.2104 18.9915ZM18.9134 18.6194L19.2004 19.3123H19.2004L18.9134 18.6194ZM19.6125 2.7368L19.2206 3.37628L19.6125 2.7368ZM21.2632 4.38751L21.9027 3.99563V3.99563L21.2632 4.38751ZM4.38751 2.7368L3.99563 2.09732V2.09732L4.38751 2.7368ZM2.7368 4.38751L2.09732 3.99563H2.09732L2.7368 4.38751ZM9.40279 19.2098L9.77986 18.5615L9.77986 18.5615L9.40279 19.2098ZM13.7321 21.7697L14.2742 20.8539L12.9833 20.0898L12.4412 21.0057L13.7321 21.7697ZM9.72579 20.8539L10.2679 21.7697L11.5587 21.0057L11.0166 20.0898L9.72579 20.8539ZM12.4412 21.0057C12.2485 21.3313 11.7515 21.3313 11.5587 21.0057L10.2679 21.7697C11.0415 23.0767 12.9585 23.0767 13.7321 21.7697L12.4412 21.0057ZM10.5 2.75H13.5V1.25H10.5V2.75ZM21.25 10.5V11.5H22.75V10.5H21.25ZM7.8025 18.2416C6.54706 18.2199 5.88923 18.1401 5.37359 17.9265L4.79957 19.3123C5.60454 19.6457 6.52138 19.7197 7.77666 19.7413L7.8025 18.2416ZM1.68769 16.2004C2.27128 17.6093 3.39066 18.7287 4.79957 19.3123L5.3736 17.9265C4.33223 17.4951 3.50486 16.6678 3.07351 15.6264L1.68769 16.2004ZM21.25 11.5C21.25 12.6751 21.2496 13.5189 21.2042 14.1847C21.1592 14.8438 21.0726 15.2736 20.9265 15.6264L22.3123 16.2004C22.5468 15.6344 22.6505 15.0223 22.7007 14.2868C22.7504 13.5581 22.75 12.6546 22.75 11.5H21.25ZM16.2233 19.7413C17.4786 19.7197 18.3955 19.6457 19.2004 19.3123L18.6264 17.9265C18.1108 18.1401 17.4529 18.2199 16.1975 18.2416L16.2233 19.7413ZM20.9265 15.6264C20.4951 16.6678 19.6678 17.4951 18.6264 17.9265L19.2004 19.3123C20.6093 18.7287 21.7287 17.6093 22.3123 16.2004L20.9265 15.6264ZM13.5 2.75C15.1512 2.75 16.337 2.75079 17.2619 2.83873C18.1757 2.92561 18.7571 3.09223 19.2206 3.37628L20.0044 2.09732C19.2655 1.64457 18.4274 1.44279 17.4039 1.34547C16.3915 1.24921 15.1222 1.25 13.5 1.25V2.75ZM22.75 10.5C22.75 8.87781 22.7508 7.6085 22.6545 6.59611C22.5572 5.57256 22.3554 4.73445 21.9027 3.99563L20.6237 4.77938C20.9078 5.24291 21.0744 5.82434 21.1613 6.73809C21.2492 7.663 21.25 8.84876 21.25 10.5H22.75ZM19.2206 3.37628C19.7925 3.72672 20.2733 4.20752 20.6237 4.77938L21.9027 3.99563C21.4286 3.22194 20.7781 2.57144 20.0044 2.09732L19.2206 3.37628ZM10.5 1.25C8.87781 1.25 7.6085 1.24921 6.59611 1.34547C5.57256 1.44279 4.73445 1.64457 3.99563 2.09732L4.77938 3.37628C5.24291 3.09223 5.82434 2.92561 6.73809 2.83873C7.663 2.75079 8.84876 2.75 10.5 2.75V1.25ZM2.75 10.5C2.75 8.84876 2.75079 7.663 2.83873 6.73809C2.92561 5.82434 3.09223 5.24291 3.37628 4.77938L2.09732 3.99563C1.64457 4.73445 1.44279 5.57256 1.34547 6.59611C1.24921 7.6085 1.25 8.87781 1.25 10.5H2.75ZM3.99563 2.09732C3.22194 2.57144 2.57144 3.22194 2.09732 3.99563L3.37628 4.77938C3.72672 4.20752 4.20752 3.72672 4.77938 3.37628L3.99563 2.09732ZM11.0166 20.0898C10.8136 19.7468 10.6354 19.4441 10.4621 19.2063C10.2795 18.9559 10.0702 18.7304 9.77986 18.5615L9.02572 19.8582C9.07313 19.8857 9.13772 19.936 9.24985 20.0898C9.37122 20.2564 9.50835 20.4865 9.72579 20.8539L11.0166 20.0898ZM7.77666 19.7413C8.21575 19.7489 8.49387 19.7545 8.70588 19.7779C8.90399 19.7999 8.98078 19.832 9.02572 19.8582L9.77986 18.5615C9.4871 18.3912 9.18246 18.3215 8.87097 18.287C8.57339 18.2541 8.21375 18.2487 7.8025 18.2416L7.77666 19.7413ZM14.2742 20.8539C14.4916 20.4865 14.6287 20.2564 14.7501 20.0898C14.8622 19.936 14.9268 19.8857 14.9742 19.8582L14.2201 18.5615C13.9298 18.7304 13.7204 18.9559 13.5379 19.2063C13.3646 19.4441 13.1864 19.7468 12.9833 20.0898L14.2742 20.8539ZM16.1975 18.2416C15.7862 18.2487 15.4266 18.2541 15.129 18.287C14.8175 18.3215 14.5129 18.3912 14.2201 18.5615L14.9742 19.8582C15.0192 19.832 15.096 19.7999 15.2941 19.7779C15.5061 19.7545 15.7842 19.7489 16.2233 19.7413L16.1975 18.2416Z" fill="#ffffff"></path> </g></svg>

                  <p className='text-white m-0 quik-txt'>Quick Topics</p>

                </div>
              </div>

              <div className='b-box'>

                <p className='t-text'>
                  Today
                </p>

                <button className='invest-basis'>
                  Investing Basics
                </button>

                <button className='invest-basis invest-in'>
                  Retirement Planing
                </button>

                <button className='invest-basis invest-in'>
                  Budgeting Tips
                </button>

                <button className='invest-basis invest-in'>
                  Tax Advice
                </button>
                <button className='invest-basis invest-in'>
                  Credit Scores
                </button>
                <button className='invest-basis invest-in'>
                  Debit management
                </button>



              </div>



            </div>

          </div>

        </div>

      </section>





    </>
  );
}

export default Dashboard;
