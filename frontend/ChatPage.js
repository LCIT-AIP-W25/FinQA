import React, { useEffect, useRef, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import axios from "axios";
import { v4 as uuidv4 } from "uuid";
import "../styles/ChatPage.css"; // ✅ Import external CSS


const companyList = [
    'Amazon', 'McDonald\'s', 'Meta', 'Coca-Cola', 'Google', 'Alphabet',
    'S&P Global', 'Tesla', 'Microsoft', 'Netflix', 'HSBC', 'JPMorgan',
    'Shell', 'AT&T', 'Verizon', 'AMD', 'Mastercard', 'PepsiCo'
  ];  

function ChatPage() {
    const [message, setMessage] = useState("");
    const [currentChat, setCurrentChat] = useState([]);
    const [chatHistory, setChatHistory] = useState([]);
    const [sessionId, setSessionId] = useState("");
    const [selectedChatIndex, setSelectedChatIndex] = useState(null);
    const [user, setUser] = useState(null);
    const [dropdownOpen, setDropdownOpen] = useState(false);
    const [userInput, setUserInput] = useState('');
    
    const [isLoading, setIsLoading] = useState(false);
    const [selectedCompany, setSelectedCompany] = useState('');
    const [searchTerm, setSearchTerm] = useState('');
    

    const chatEndRef = useRef(null);
    const navigate = useNavigate();

    const [modalOpen, setModalOpen] = useState(false);
const [modalContent, setModalContent] = useState([]);

const [hoveredMenu, setHoveredMenu, index] = useState(null);


    // ✅ Auto-scroll to the latest message
    const scrollToBottom = () => {
        if (chatEndRef.current) {
            chatEndRef.current.parentNode.scrollTop = chatEndRef.current.parentNode.scrollHeight;
        }
    };

    // ✅ Initialize session ID or generate a new one
    useEffect(() => {
        // ✅ Fetch user data from localStorage
        const storedUser = JSON.parse(localStorage.getItem("user"));
        if (storedUser && storedUser.username) {
            setUser(storedUser); // Set user if found
        } else {
            navigate("/login"); // Redirect to login if not found
        }
    
        // ✅ Initialize session ID
        const storedSessionId = localStorage.getItem("sessionId");
        const userId = localStorage.getItem("userId");
    
        if (!storedSessionId) {
            // Start a new session if there's no active session
            startNewChat();
        } else {
            // Load the existing session on reload
            loadChatSession(storedSessionId);
        }
    
        // ✅ Fetch all chat sessions from the server
        fetchAllChatSessions();
    }, []);
      

    useEffect(() => {
        scrollToBottom();
    }, [currentChat]);

    // ✅ Fetch chat history for the current session
    const fetchChatHistory = async (id) => {
        try {
            const response = await axios.get(`http://127.0.0.1:5000/get_chats/${id}`);
            setCurrentChat(response.data);
        } catch (error) {
            console.error("Error fetching chat history:", error);
        }
    };

    // ✅ Fetch all chat sessions for displaying history
    const fetchAllChatSessions = async () => {
        try {
            const userId = localStorage.getItem("userId");
            const response = await axios.get(`http://127.0.0.1:5000/get_all_sessions/${userId}`);
            
            // Filter out empty chats (sessions with no messages)
            const validSessions = await Promise.all(
                response.data.map(async (chat) => {
                    const chatMessages = await axios.get(`http://127.0.0.1:5000/get_chats/${chat.session_id}`);
                    return chatMessages.data.length > 0 ? chat : null;  // Only keep sessions with messages
                })
            );
    
            // Remove null values (unsent/empty sessions)
            setChatHistory(validSessions.filter(session => session !== null));
        } catch (error) {
            console.error("Error fetching user-specific chat sessions:", error);
        }
    };
      

    // ✅ Send message to Flask backend and save
    const sendMessage = async () => {
        if (!message.trim()) return;
    
        const userMessage = { sender: "user", message: message };
        setCurrentChat((prevChat) => [...prevChat, userMessage]);
    
        await saveChatToBackend(userMessage);
    
        try {
            // ✅ Updated API call to the real chatbot
            const response = await axios.post("http://127.0.0.1:5000/query_chatbot", {
                question: message,
                session_id: sessionId,  // Pass the session ID dynamically
                user_id: user.user_id,
                selected_company: selectedCompany        // Pass the user ID dynamically
            });
    
            // ✅ Handle the chatbot's real response
            const botMessage = response.data.response
                ? { sender: "bot", message: response.data.response }
                : { sender: "bot", message: "Sorry, I could not process that request." };
    
            setCurrentChat((prevChat) => [...prevChat, botMessage]);
            await saveChatToBackend(botMessage);
        } catch (error) {
            console.error("Error sending message:", error);
    
            // ✅ Add error handling message
            const errorMessage = { sender: "bot", message: "Error communicating with the chatbot." };
            setCurrentChat((prevChat) => [...prevChat, errorMessage]);
            await saveChatToBackend(errorMessage);
        }
    
        setMessage(""); // Clear input
    };
    

    // ✅ Save message to backend (SQLite)
    const saveChatToBackend = async (chatMessage) => {
        try {
            const userId = localStorage.getItem("userId");
            await axios.post("http://127.0.0.1:5000/save_chat", {
                sender: chatMessage.sender,
                message: chatMessage.message,
                session_id: sessionId,
                user_id: userId
            });
        } catch (error) {
            console.error("Error saving chat:", error);
        }
    };    

    // ✅ Start a new chat (Generate a new session)
    const startNewChat = async () => {
        try {
            const userId = localStorage.getItem("userId");
            const response = await axios.post("http://127.0.0.1:5000/new_session", { user_id: userId });
    
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
            const response = await axios.get(`http://127.0.0.1:5000/get_chat/${selectedSessionId}`);
            setSessionId(selectedSessionId);
            setCurrentChat(response.data.messages);  // Load the fetched messages
        } catch (error) {
            console.error("Error loading chat session:", error);
        }
    };
    
      
    
    const handleChatSelection = async (selectedSessionId) => {
        try {
            // Fetch chat messages for the selected session from the backend
            const response = await axios.get(`http://127.0.0.1:5000/get_chat/${selectedSessionId}`);
            
            // Update state with the selected session's messages
            setSessionId(selectedSessionId);
            setCurrentChat(response.data.messages);  // Display chat messages in the chat window
        } catch (error) {
            console.error("Error fetching selected chat:", error);
        }
    };
    
    // ✅ Delete a chat session
    const deleteChatSession = async (sessionIdToDelete) => {
        const confirmDelete = window.confirm("Are you sure you want to delete this chat?");
        if (!confirmDelete) return;
    
        try {
            await axios.delete(`http://127.0.0.1:5000/delete_chat/${sessionIdToDelete}`);
    
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

    // ✅ Handle Sign Out
    const handleSignOut = () => {
        localStorage.removeItem("user"); // Remove user data from local storage
        localStorage.removeItem("sessionId"); // Remove session ID
        navigate("/login"); // Redirect to login page
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
        newTitle = `Chat - ${new Date().toLocaleString()}`;
        }
    
        // Save the new title
        storedTitles[sessionId] = newTitle;
        localStorage.setItem("chatTitles", JSON.stringify(storedTitles));
    
        return newTitle;
    };

    return (
        <section className="chat-app-container">
            <div className="chat-app-wrapper">
                {/* ✅ Header Section with User Info */}
                <div className="chat-app-header">
                    <div className="chat-app-logo">
                        <Link to="/chat">
                            <img className="chat-app-logo-img" src="/images/wes.png" alt="Logo" />
                        </Link>
                        {/* Header Text */}
                        <h2 className="chat-app-header-title">WealthWiz</h2>
                    </div>


                    
                    <div className="chat-app-user-section">
    <div className="chat-app-profile" onClick={() => setDropdownOpen(!dropdownOpen)}>
        {/* Modern Circular Avatar with Initials */}
        <div className="chat-app-profile-icon">
            {user?.username?.charAt(0).toUpperCase()}
        </div>

        {/* User's Name (Displayed Only on Large Screens) */}
        <span className="chat-app-username">{user?.username}</span>
        


        {/* Animated Dropdown */}
        {dropdownOpen && (
            <div className="chat-app-dropdown-menu">
                <div className="chat-app-profile-info">
                    <div className="chat-app-avatar">
                        {user?.username?.charAt(0).toUpperCase()}
                    </div>
                    <p className="chat-app-profile-name">Hi, {user?.username}!</p>
                    
                    
                </div>
                <hr />

                <button className="chat-app-dropdown-item" type="button" data-bs-toggle="modal" data-bs-target="#myProfile">My Profile</button>

                <div class="modal fade" id="myProfile" tabindex="-1" aria-labelledby="modalTitle" aria-hidden="true">
                    {/* ✅ Modal */}
                    <div className="modal-dialog modal-dialog-centered">
                <div className="modal-content p-4 shadow-lg rounded-4">
                 {/* Modal Header */}
                <div className="modal-header border-0">
                  <h5 className="modal-title fw-bold text-primary" id="modalTitle">
                    <i className="bi bi-person-circle me-2"></i> My Profile
                        </h5>
                    <button type="button" className="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>

                    {/* Modal Body */}
                    <div className="modal-body text-center">
                    {/* Profile Image Placeholder */}
    

                    {/* User Information */}
                    <p className="mb-2">
                        <strong className="text-secondary">Username:</strong> <span className="text-dark">{user?.username}</span>
                    </p>
                    <p className="mb-3">
                        <strong className="text-secondary">Email:</strong> <span className="text-dark">{user?.email}</span>
                    </p>
                    </div>

                    {/* Modal Footer */}
                    <div className="modal-footer border-0 d-flex justify-content-center">
                    
                    <button type="button" className="btn btn-success">
                        <i className="bi bi-check-circle"></i> Save Changes
                    </button>
                    </div>
                </div>
                </div>

                    </div>

                <button className="chat-app-dropdown-item chat-app-sign-out" onClick={handleSignOut}><i className="fas fa-sign-out-alt" aria-hidden="true"></i>Logout</button>
            </div>
        )}
    </div>
</div>
</div>

                <div className="chat-app-content">
                    {/* ✅ Sidebar Section */}
                    <div className="chat-app-sidebar">
                        <div className="chat-app-company-search">
                            <input
                                type="text"
                                placeholder="Search company..."
                                value={searchTerm}
                                onChange={(e) => setSearchTerm(e.target.value)}
                                className="chat-app-search-input"
                            />
                            <div className="chat-app-company-list">
                                <ul className="menu">
                                {companyList
                                .filter(company => company.toLowerCase().includes(searchTerm.toLowerCase()))
                                .map((company) => (
                                    <li
                                    key={company}
                                    className={`menu-item chat-app-company-item ${selectedCompany === company ? 'selected' : ''}`}
                                    onClick={() => setSelectedCompany(company)}
                                    onMouseEnter={() => setHoveredMenu(index)}
                                    onMouseLeave={() => setHoveredMenu(null)}
                                    >
                
                                    {company}
                                        {hoveredMenu === index && (
                                            <ul className="submenu chat-app-company-submenu">
                                                <h6 className="sub-heading">Matrix</h6>
                                                <li className="chat-app-company-item">Nedddsdws</li>
                                                <li className="chat-app-company-item">Compadsdny Info</li>
                                                <li className="chat-app-company-item">Stdsdock Info</li>
                                                <li className="chat-app-company-item">News</li>
                                                <li className="chat-app-company-item">Company Info</li>
                                                <li className="chat-app-company-item">Stock Info</li>
                                                <li className="chat-app-company-item">Stdsdock Info</li>
                                                <li className="chat-app-company-item">News</li>
                                                <li className="chat-app-company-item">Company Info</li>
                                                <li className="chat-app-company-item">Stock Info</li>
                                            </ul>
                                        )}
                                    </li>
                                ))}</ul>
                            </div>
                        </div>
                        {chatHistory.length === 0 ? (
                            <p>No previous chats</p>
                        ) : (
                            <div className="chat-app-chat-history">
                                <h5 className="chat-app-chat-history-header">Chat History</h5>
                                <div className="chat-app-chat-list">
                                    {chatHistory.map((chat) => (
                                        <div
                                            key={chat.session_id}
                                            className={`chat-app-chat-item ${sessionId === chat.session_id ? "active" : ""}`}
                                            onClick={() => loadChatSession(chat.session_id)}
                                        >
                                            <div className="chat-app-chat-content">
                                                <p className="chat-app-chat-title">
                                                    {getOrGenerateTitle(chat.session_id, chat.messages)}
                                                </p>
                                                <button
                                                    onClick={(e) => {
                                                        e.stopPropagation();
                                                        deleteChatSession(chat.session_id);
                                                    }}
                                                    className="chat-app-delete-btn"
                                                >
                                                    🗑️
                                                </button>
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        )}
                    </div>

                    {/* ✅ Chat Window Section */}
                    <div className="chat-app-window">
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

                        {/* ✅ Chat Input Box */}
                        <div className="chat-app-input-section">
                            <input
                                type="text"
                                className="chat-app-input"
                                placeholder="Type a message..."
                                value={message}
                                onChange={(e) => setMessage(e.target.value)}
                                onKeyPress={(e) => e.key === "Enter" && sendMessage()}
                            />
                            <button onClick={sendMessage} className="chat-app-send-btn"><i class="fa-solid fa-paper-plane"></i></button>
                            <button onClick={startNewChat} className="chat-app-new-chat-btn"><i class="fa fa-plus"></i></button>
                        </div>

                    </div>

                    <div className=" chat-app-company-suggestions">
                        <h5 className="chat-app-company-suggestions-header">Quick Suggestions</h5>
                        <div className="chat-app-company-suggestions-list">
                            <ul className="menu">
                                {companyList.map((company) => (
                                    <li key={company} className="menu-item chat-app-company-item">
                                        {company}
                                    </li>
                                ))}
                            </ul>
                        </div>

                    </div>
                    
                </div>
            </div>

            
        </section>
        

    );
       
}



export default ChatPage;