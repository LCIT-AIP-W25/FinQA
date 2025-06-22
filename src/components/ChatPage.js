import { useLocation } from 'react-router-dom';
import { useLoader } from "./LoaderContext";
import React, { useEffect, useRef, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import axios from "axios";
import "../styles/ChatPage.css"; 
import ChatHistorySidebar from "./ChatHistorySidebar";
import MetricsSidebar from "./MetricsSidebar";
import SlickBar from "./SlickBar";           
import FloatingPanel from "./FloatingPanel"; 
import CompanyReportPanel from "./CompanyReportPanel";


function ChatPage() {
    const location = useLocation();
    const [message, setMessage] = useState("");
    const [currentChat, setCurrentChat] = useState([]);
    const [chatHistory, setChatHistory] = useState([]);
    const [sessionId, setSessionId] = useState("");
    const [user, setUser] = useState(null);
    const [dropdownOpen, setDropdownOpen] = useState(false);
    const [selectedCompany, setSelectedCompany] = useState('');
    const [searchTerm, setSearchTerm] = useState('');
    const [companyList, setCompanyList] = useState([]);
    const [showChatSidebar, setShowChatSidebar] = useState(false);
    const [showMetricsSidebar, setShowMetricsSidebar] = useState(false);
    const [showCompanyPanel, setShowCompanyPanel] = useState(() => window.innerWidth >= 768);

    const chatEndRef = useRef(null);
    const navigate = useNavigate();

    const CHATBOT_API_URL = process.env.REACT_APP_CHATBOT_API_URL || "http://127.0.0.1:5000";
    // const CHATBOT_API_URL = "http://127.0.0.1:5000"

    const { setLoading } = useLoader();

    useEffect(() => {
        if (location.state?.openPanel) {
            switch (location.state.openPanel) {
                case 'company':
                    setShowCompanyPanel(true);
                    break;
                case 'history':
                    setShowChatSidebar(true);
                    break;
                case 'metrics':
                    setShowMetricsSidebar(true);
                    break;
                default:
                    break;
            }
        }
    }, [location]);

    useEffect(() => {
        const setViewportHeight = () => {
          const vh = window.innerHeight * 0.01;
          document.documentElement.style.setProperty('--vh', `${vh}px`);
        };
      
        setViewportHeight();
        window.addEventListener('resize', setViewportHeight);
        return () => window.removeEventListener('resize', setViewportHeight);
      }, []);

    useEffect(() => {
        window.scrollTo(0, 0);
      }, []);
      
    useEffect(() => {
        const handleResize = () => {
          if (window.innerWidth < 768) {
            setShowCompanyPanel(false);
          }
        };
      
        window.addEventListener("resize", handleResize);
        return () => window.removeEventListener("resize", handleResize);
      }, []);

    useEffect(() => {
        //  Add a global request interceptor
        const requestInterceptor = axios.interceptors.request.use((config) => {
            // Skip loader for PDF upload & processing
            if (!config.url.includes("/upload_pdf") && !config.url.includes("/pdf_status")) {
                setLoading(true);
            }
            return config;
        });
    
        //  Add a global response interceptor
        const responseInterceptor = axios.interceptors.response.use(
            (response) => {
                // Skip disabling loader for PDF requests (they never triggered it)
                if (!response.config.url.includes("/upload_pdf") && !response.config.url.includes("/pdf_status")) {
                    setLoading(false);
                }
                return response;
            },
            (error) => {
                if (!error.config.url.includes("/upload_pdf") && !error.config.url.includes("/pdf_status")) {
                    setLoading(false);
                }
                return Promise.reject(error);
            }
        );
    
        //  Cleanup interceptors on unmount
        return () => {
            axios.interceptors.request.eject(requestInterceptor);
            axios.interceptors.response.eject(responseInterceptor);
        };
    }, [setLoading]);
    
    //  Auto-scroll to the latest message
    const scrollToBottom = () => {
        if (chatEndRef.current) {
            chatEndRef.current.parentNode.scrollTop = chatEndRef.current.parentNode.scrollHeight;
        }
    };

    //  Fetch company names from API on component mount
    useEffect(() => {
            async function fetchCompanies() {
                try {
                    const response = await axios.get(`${CHATBOT_API_URL}/api/companies`);
                    console.log("Fetched companies:", response.data);
                    setCompanyList(response.data);  //  Store fetched company names
                } catch (error) {
                    console.error("Error fetching company names:", error);
                }
            }
            fetchCompanies();
        }, []);

    //  Initialize session ID or generate a new one
    useEffect(() => {
        //  Fetch user data from localStorage
        const storedUser = JSON.parse(localStorage.getItem("user"));
        if (storedUser && storedUser.username) {
            setUser(storedUser); // Set user if found
        } else {
            navigate("/login"); // Redirect to login if not found
        }
    
        //  Initialize session ID
        const storedSessionId = localStorage.getItem("sessionId");
        const userId = localStorage.getItem("userId");
    
        if (!storedSessionId) {
            // Start a new session if there's no active session
            startNewChat();
        } else {
            // Load the existing session on reload
            loadChatSession(storedSessionId);
        }
    
        //  Fetch all chat sessions from the server
        fetchAllChatSessions();
    }, []);
      

    useEffect(() => {
        scrollToBottom();
    }, [currentChat]);


    //  Fetch all chat sessions for displaying history
    const fetchAllChatSessions = async () => {
        try {
            const userId = localStorage.getItem("userId");
            const response = await axios.get(`${CHATBOT_API_URL}/get_all_sessions/${userId}`);
            
            // Filter out empty chats (sessions with no messages)
            const validSessions = await Promise.all(
                response.data.map(async (chat) => {
                    const chatMessages = await axios.get(`${CHATBOT_API_URL}/get_chats/${chat.session_id}`);
                    return chatMessages.data.length > 0 ? chat : null;  // Only keep sessions with messages
                })
            );
    
            // Remove null values (unsent/empty sessions)
            setChatHistory(validSessions.filter(session => session !== null));
        } catch (error) {
            console.error("Error fetching user-specific chat sessions:", error);
        }
    }; 

    const sendMessage = async () => { //newly added today
        if (!message.trim()) return;
    
        // Append user message to chat
        const userMessage = { sender: "user", message: message };
        setCurrentChat((prevChat) => [...prevChat, userMessage]);
    
        await saveChatToBackend(userMessage);
    
        //  Check if company is selected
        if (!selectedCompany) {
            const errorMessage = { sender: "bot", message: "Please select a company before sending a message." };
            setCurrentChat((prevChat) => [...prevChat, errorMessage]);
            await saveChatToBackend(errorMessage);
            setMessage(""); // Clear input field
            return;
        }
    
        try {
            //  Make API call to the chatbot
            const response = await axios.post(`${CHATBOT_API_URL}/query_chatbot`, {
                question: message,
                session_id: sessionId,
                user_id: user.user_id,
                selected_company: selectedCompany
            });
    
            //  Handle chatbot response
            const botMessage = response.data.response
                ? { sender: "bot", message: response.data.response }
                : { sender: "bot", message: "I'm not sure how to respond to that." };
    
            setCurrentChat((prevChat) => [...prevChat, botMessage]);
            await saveChatToBackend(botMessage);
        } catch (error) {
            console.error("Error sending message:", error); // Log technical error
    
            //  User-friendly error message
            const errorMessage = { sender: "bot", message: "Oops! Something went wrong. Please try again later." };
            setCurrentChat((prevChat) => [...prevChat, errorMessage]);
            await saveChatToBackend(errorMessage);
        }
    
        setMessage(""); // Clear input field
    };

    //  Save message to backend (SQLite)
    const saveChatToBackend = async (chatMessage) => {
        try {
            const userId = localStorage.getItem("userId");
            await axios.post(`${CHATBOT_API_URL}/save_chat`, {
                sender: chatMessage.sender,
                message: chatMessage.message,
                session_id: sessionId,
                user_id: userId
            });

            // Update chat history after saving message
            await fetchAllChatSessions();
        } catch (error) {
            console.error("Error saving chat:", error);
        }
    };    

    //  Start a new chat (Generate a new session)
    const startNewChat = async () => {
        try {
            const userId = localStorage.getItem("userId");
            const response = await axios.post(`${CHATBOT_API_URL}/new_session`, { user_id: userId });
    
            const newSessionId = response.data.session_id;
            localStorage.setItem("sessionId", newSessionId);
            setSessionId(newSessionId);
            setCurrentChat([]);  // Clear chat messages
    
            // Force fetch updated chat history after creating a new session
            fetchAllChatSessions();  
        } catch (error) {
            console.error("Error starting a new chat session:", error);
        }
    };

    const loadChatSession = async (selectedSessionId) => {
        try {
            const response = await axios.get(`${CHATBOT_API_URL}/get_chat/${selectedSessionId}`);
            setSessionId(selectedSessionId);
            setCurrentChat(response.data.messages);  // Load the fetched messages
        } catch (error) {
            console.error("Error loading chat session:", error);
        }
    };
    
    //  Delete a chat session
    const deleteChatSession = async (sessionIdToDelete) => {
        const confirmDelete = window.confirm("Are you sure you want to delete this chat?");
        if (!confirmDelete) return;
    
        try {
            await axios.delete(`${CHATBOT_API_URL}/delete_chat/${sessionIdToDelete}`);
    
            // Remove from chat history immediately
            setChatHistory((prevHistory) =>
                prevHistory.filter(chat => chat.session_id !== sessionIdToDelete)
            );
    
            // If the active session was deleted, start a new chat
            if (sessionId === sessionIdToDelete) {
                startNewChat();
            }
    
            alert("Chat deleted successfully!");
        } catch (error) {
            console.error("Error deleting chat session:", error);
        }
    };       

    const handleSignOut = () => {
        localStorage.removeItem("user");              // full user info
        localStorage.removeItem("userId");            // used by chatbot
        localStorage.removeItem("sessionId");         // current chat session
        localStorage.removeItem("pdfChat_userId");    // used by PDF Q&A
        localStorage.removeItem("pdfChat_filename");  // uploaded PDF
        navigate("/login");                           // redirect to login
    };    
    
        // Store custom titles dynamically in localStorage
    const getOrGenerateTitle = (sessionId, chatMessages) => {
        const storedTitles = JSON.parse(localStorage.getItem("chatTitles")) || {};
    
        if (storedTitles[sessionId]) {
        return storedTitles[sessionId]; // Return the existing title
        }
    
        // Generate a new title dynamically based on chat content
        let newTitle = "New Chat";
        if (chatMessages && chatMessages.length > 0) {
        const firstMessage = chatMessages[0].message;
        newTitle = firstMessage.slice(0, 20); // First 20 characters of the first message
        } else {
        // Use timestamp if no messages
        newTitle = `Chat - `;
        }
    
        // Save the new title
        storedTitles[sessionId] = newTitle;
        localStorage.setItem("chatTitles", JSON.stringify(storedTitles));
    
        return newTitle;
    };

    const [uploadMessage, setUploadMessage] = useState("");
    const [filename, setFilename] = useState("");
    const [uploadStatus, setUploadStatus] = useState(null); // "success" | "error" | "loading"
    const [hoverMessage, setHoverMessage] = useState(""); // Store full message for hover

    const handleFileUpload = async (event) => {
        const file = event.target.files[0];
        if (!file) return;
    
        setUploadStatus("loading");
        setUploadMessage("⏳ Uploading...");
        setHoverMessage("Uploading PDF...");
        
        const userId = localStorage.getItem("userId");
        const formData = new FormData();
        formData.append("file", file);
        formData.append("user_id", userId);
    
        try {
            const response = await axios.post(`${CHATBOT_API_URL}/upload_pdf`, formData, {
                headers: { "Content-Type": "multipart/form-data" },
            });
    
            if (response.data.error) {
                setUploadStatus("error");
                setUploadMessage("❌");
                setHoverMessage(`Error: ${response.data.error}`);
                return;
            }
    
            setUploadStatus("success");
            setUploadMessage("⏳");
            setFilename(response.data.filename);
            setHoverMessage('PDF Processing...');
    
            //  Wait for processing to complete
            
            localStorage.setItem("pdfChat_userId", userId);
            localStorage.setItem("pdfChat_filename", response.data.filename);
            checkProcessingStatus(response.data.filename);

        } catch (error) {
            console.error("Upload failed:", error);
            setUploadStatus("error");
            setUploadMessage("❌");
            setHoverMessage("Upload failed. Please try again.");
        }
    };

    //  Check processing status until it's done
    const checkProcessingStatus = async (filename) => {
        const interval = setInterval(async () => {
            try {
                const userId = localStorage.getItem("userId");
                const statusResponse = await axios.get(`${CHATBOT_API_URL}/pdf_status/${userId}/${filename}`);

                if (statusResponse.data.status === "done") {
                    clearInterval(interval);
                    setUploadMessage("✅ Processing completed! Redirecting...");
                    setTimeout(() => navigate("/pdf-chat"), 2000);
                } else if (statusResponse.data.status === "failed") {
                    clearInterval(interval);
                    setUploadMessage("❌ Processing failed. Please try again.");
                }
            } catch (error) {
                console.error("Error checking status:", error);
            }
        }, 3000); //  Check every 3 seconds
    };

// Show Metrics Window------------------------------------------------

    const [companyMetrics, setCompanyMetrics] = useState([]);
    const [metricsSearchTerm, setMetricsSearchTerm] = useState('');
    const [selectedMetric, setSelectedMetric] = useState(''); // New state for selected metric

    const filteredMetrics = companyMetrics.filter(metric => 
    metric.toLowerCase().includes(metricsSearchTerm.toLowerCase())
    );

    // Handle metric selection
    const handleMetricClick = (metric) => {
    setSelectedMetric(metric);
    setMessage(prev => {
        if (!prev) return `${metric}`;
        if (prev.trim().endsWith('?')) return `${prev} ${metric}`;
        return `${prev} ${metric}`;
    });
    
    // Auto-focus the input field
    setTimeout(() => {
        const input = document.querySelector('.chat-app-input');
        if (input) input.focus();
    }, 100);
    };

    // Fetch company metrics when a company is selected
    useEffect(() => {
    async function fetchMetrics() {
        if (!selectedCompany) return;

        try {
        const response = await axios.get(`${CHATBOT_API_URL}/api/company_metrics/${selectedCompany}`);

        if (Array.isArray(response.data)) {
            response.data = response.data[0];
        }

        if (response.data && response.data.metrics && Array.isArray(response.data.metrics)) {
            setCompanyMetrics(response.data.metrics);
        } else {
            setCompanyMetrics([]);
        }
        } catch (error) {
        console.error("Error fetching company metrics:", error);
        setCompanyMetrics([]);
        }
    }

    fetchMetrics();
    }, [selectedCompany]);

    return (
        <section className="chat-app-container">
            <div className="chat-app-wrapper">
                {/* Header Section with User Info */}
                <div className="chat-app-header">
                    <div className="chat-app-logo">
                        <Link to="/home">
                            <img className="chat-app-logo-img" src="/images/wes.png" alt="Logo" />
                        </Link>
                        {/* Header Text */}
                        <h2 className="chat-app-header-title">FinAnswer</h2>
                    </div>


                    
                    <div className="chat-app-user-section">
                        <div className="chat-app-profile">
                            {user ? (
                                <>
                                    <span className="chat-app-username">{user.username}</span>
                                    <div className="chat-app-profile-dropdown" onClick={() => setDropdownOpen(!dropdownOpen)}>
                                        <div className="chat-app-profile-icon">
                                            {user.username.charAt(0).toUpperCase()}
                                        </div>
                                        {dropdownOpen && (
                                            <div className="chat-app-dropdown-menu">
                                                <div className="chat-app-profile-info">
                                                    <div className="chat-app-avatar">
                                                        {user.username.charAt(0).toUpperCase()}
                                                    </div>
                                                    <p className="chat-app-profile-name">Hi, {user.username}!</p>
                                                </div>
                                                <hr />
                                                {/* <button className="chat-app-dropdown-item">My Profile</button> */}
                                                <button className="chat-app-dropdown-item chat-app-sign-out" onClick={handleSignOut}>Sign Out</button>
                                            </div>
                                        )}
                                    </div>
                                </>
                            ) : (
                                <span>Loading...</span>  // Placeholder until user data loads
                            )}
                        </div>
                    </div>
                </div>
                <SlickBar
                    onToggleCompany={() => {
                        setShowCompanyPanel(prev => !prev);
                        setShowChatSidebar(false);
                        setShowMetricsSidebar(false);
                    }}
                    onToggleChat={() => {
                        setShowChatSidebar(prev => !prev);
                        setShowCompanyPanel(false);
                        setShowMetricsSidebar(false);
                    }}
                    onToggleMetrics={() => {
                        setShowMetricsSidebar(prev => !prev);
                        setShowCompanyPanel(false);
                        setShowChatSidebar(false);
                    }}
                    />

                <div className="chat-app-content">

                {showCompanyPanel && (
                        <FloatingPanel onClose={() => setShowCompanyPanel(false)}>
                            <CompanyReportPanel
                            searchTerm={searchTerm}
                            setSearchTerm={setSearchTerm}
                            companyList={companyList}
                            selectedCompany={selectedCompany}
                            setSelectedCompany={setSelectedCompany}
                            handleFileUpload={handleFileUpload}
                            uploadStatus={uploadStatus}
                            uploadMessage={uploadMessage}
                            hoverMessage={hoverMessage}
                            setUploadMessage={setUploadMessage}
                            setShowCompanyPanel={setShowCompanyPanel} 
                            />
                        </FloatingPanel>
                        )}


                    {showChatSidebar && (
                        <FloatingPanel onClose={() => setShowChatSidebar(false)} position="left">
                            <ChatHistorySidebar
                            searchTerm={searchTerm}
                            setSearchTerm={setSearchTerm}
                            companyList={companyList}
                            selectedCompany={selectedCompany}
                            setSelectedCompany={setSelectedCompany}
                            chatHistory={chatHistory}
                            sessionId={sessionId}
                            loadChatSession={loadChatSession}
                            deleteChatSession={deleteChatSession}
                            getOrGenerateTitle={getOrGenerateTitle}
                            setShowChatSidebar={setShowChatSidebar}
                            />
                        </FloatingPanel>
                        )}

                    {showMetricsSidebar && (
                        <FloatingPanel onClose={() => setShowMetricsSidebar(false)} position="left">
                            <MetricsSidebar
                            selectedCompany={selectedCompany}
                            metricsSearchTerm={metricsSearchTerm}
                            setMetricsSearchTerm={setMetricsSearchTerm}
                            filteredMetrics={filteredMetrics}
                            selectedMetric={selectedMetric}
                            handleMetricClick={handleMetricClick}
                            setShowMetricsSidebar={setShowMetricsSidebar}
                            />
                        </FloatingPanel>
                        )}

  

                    {/* Chat Window Section */}
                    <div className="chat-app-window">

                        {/* Display the selected company above the chat window */}
                        <div className="chat-app-selected-company">
                            {selectedCompany ? (
                                <>
                                    <div className="chat-app-selected-label-main">
                                        <span className="chat-app-selected-label">Selected Company: </span>
                                        <span className="chat-app-selected-name">{selectedCompany}</span>
                                    </div>
                                    
                                </>
                            ) : (
                                <p className="chat-app-select-company-message">Please select a company to start chatting.</p>
                            )}
                        </div>

                        <div className={`chat-app-messages ${currentChat.length > 0 ? "has-messages" : ""}`}>
                            {currentChat.length === 0 ? (
                                <p className="chat-app-placeholder">What can I help with?</p>
                            ) : (
                                currentChat.map((msg, idx) => (
                                    <p key={idx} className={msg.sender === "user" ? "chat-app-user-message" : "chat-app-bot-message"}>
                                        {msg.message}
                                    </p>
                                ))
                            )}
                            <div ref={chatEndRef}></div>
                        </div>

                        {/* Chat Input Box */}
                        <div className="chat-app-input-section">
                            <input
                                type="text"
                                className="chat-app-input"
                                placeholder="Type a message..."
                                value={message}
                                onChange={(e) => setMessage(e.target.value)}
                                onKeyPress={(e) => e.key === "Enter" && sendMessage()}
                            />


                            {/* Group buttons together for responsiveness */}
                            <div className="chat-app-button-group">
                                <button onClick={sendMessage} className="chat-button send">✉️ Send</button>
                                <button onClick={startNewChat} className="chat-button new">🔄 New Chat</button>
                            </div>
                        </div>
                    </div>


                </div>
            </div>
        </section>
    );

}

export default ChatPage;