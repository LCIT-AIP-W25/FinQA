import React, { useEffect, useRef, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import axios from "axios";
import { v4 as uuidv4 } from "uuid";
import "../styles/ChatPage.css"; // ✅ Import external CSS

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

    const chatEndRef = useRef(null);
    const navigate = useNavigate();

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
                user_id: user,        // Pass the user ID dynamically
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

    return (
        <section className="chat-bot">
            <div className="container-fluid">
                {/* ✅ Header Section with User Info */}
                <div className="row head-chat">
                    <div className="col-6">
                        <Link to="/chat">
                            <img className="we-img" src="/images/wes.png" alt="Logo" />
                        </Link>
                    </div>
                    <div className="col-6 text-end d-flex align-items-center justify-content-end">
                        {/* <button className="btn btn-primary me-3" onClick={() => navigate("/dashboard")}>
                            Go to Dashboard
                        </button> */}

                        {/* ✅ User Profile Dropdown */}
                        <div className="profile-section">
                            {user ? (
                                <>
                                    <span className="username">{user.username}</span>
                                    <div className="profile-dropdown" onClick={() => setDropdownOpen(!dropdownOpen)}>
                                        <div className="profile-icon">
                                            {user.username.charAt(0).toUpperCase()}
                                        </div>
                                        {dropdownOpen && (
                                            <div className="dropdown-menu">
                                                <div className="profile-info">
                                                    <div className="profile-avatar">
                                                        {user.username.charAt(0).toUpperCase()}
                                                    </div>
                                                    <p className="profile-name">Hi, {user.username}!</p>
                                                </div>
                                                <hr />
                                                <button className="dropdown-item">My Profile</button>
                                                <button
                                                    className="dropdown-item sign-out-btn"
                                                    onClick={handleSignOut}
                                                >
                                                    Sign Out
                                                </button>
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

                {/* ✅ Chat Interface */}
                <div className="row chat-row">
                    {/* ✅ Left Sidebar - Chat History */}
                    {/* ✅ Left Sidebar - Chat History */}
                    <div className="col-2 bg-chat">
                        <h5 className="text-white chat-history-header">Chat History</h5>
                        {chatHistory.length === 0 ? (
                            <p className="text-white">No previous chats</p>
                        ) : (
                            <div className="chat-history-list">
                                {chatHistory.map((chat) => (
                                    <div
                                        key={chat.session_id}
                                        className={`chat-history-item ${sessionId === chat.session_id ? "active-chat" : ""}`}
                                        onClick={() => loadChatSession(chat.session_id)} // Load messages on click
                                    >
                                        <div className="chat-history-content">
                                            <p className="chat-title">
                                                {chat.title || `Chat ${chat.session_id.slice(0, 8)}`}
                                            </p>
                                            <button
                                                onClick={(e) => {
                                                    e.stopPropagation(); // Prevents opening the chat when deleting
                                                    deleteChatSession(chat.session_id);
                                                }}
                                                className="delete-btn"
                                            >
                                                🗑️
                                            </button>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        )}
                    </div>

                    {/* ✅ Chat Window */}
                    <div className="col-8 d-flex flex-column align-items-center">
                        <div className="message-body">
                            {currentChat.length === 0 ? (
                                <p className="text-muted">What can I help with?</p>
                            ) : (
                                currentChat.map((msg, idx) => (
                                    <p key={idx} className={msg.sender === "user" ? "user-msg" : "bot-msg"}>
                                        {msg.message}
                                    </p>
                                ))
                            )}
                            <div ref={chatEndRef}></div>
                        </div>

                        {/* ✅ Chat Input Box */}
                        <div
                            className="d-flex justify-content-between align-items-center"
                            style={{
                                width: "100%",
                                maxWidth: "790px",
                                padding: "10px",
                                backgroundColor: "white",
                                boxShadow: "0 2px 5px rgba(0, 0, 0, 0.1)",
                                borderRadius: "10px",
                                marginTop: "10px",
                                marginLeft: "auto",
                                marginRight: "auto"
                            }}
                        >
                            <input
                                type="text"
                                className="form-control"
                                placeholder="Type a message..."
                                value={message}
                                onChange={(e) => setMessage(e.target.value)}
                                onKeyPress={(e) => e.key === "Enter" && sendMessage()}
                                style={{
                                    flex: 1,
                                    padding: "6px",
                                    borderRadius: "5px",
                                    fontSize: "13px",
                                    height: "35px",
                                    marginRight: "10px",
                                    minWidth: "200px"
                                }}
                            />

                                <button
                                    onClick={sendMessage}
                                    className="btn btn-primary"
                                    style={{
                                        display: "flex",
                                        justifyContent: "center",  // 🔥 Center horizontally
                                        alignItems: "center",      // 🔥 Center vertically
                                        padding: "6px 16px",
                                        borderRadius: "5px",
                                        height: "35px",
                                        minWidth: "80px"
                                    }}
                                >
                                    Send
                                </button>

                                <button
                                    onClick={startNewChat}
                                    className="btn btn-danger mx-2"
                                    style={{
                                        display: "flex",
                                        justifyContent: "center",  // 🔥 Center horizontally
                                        alignItems: "center",      // 🔥 Center vertically
                                        padding: "6px 16px",
                                        borderRadius: "5px",
                                        height: "35px",
                                        minWidth: "100px"
                                    }}
                                >
                                    New Chat
                                </button>

                        </div>
                    </div>
                </div>
            </div>
        </section>
    );
}

export default ChatPage;