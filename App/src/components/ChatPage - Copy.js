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
        let storedSessionId = localStorage.getItem("sessionId");
        if (!storedSessionId) {
            storedSessionId = uuidv4();
            localStorage.setItem("sessionId", storedSessionId);
        }
        setSessionId(storedSessionId);

        // ✅ Get user info
        const storedUser = JSON.parse(localStorage.getItem("user"));
        if (storedUser) {
            setUser(storedUser);
        } else {
            navigate("/login"); // Redirect to login if no user found
        }

        fetchChatHistory(storedSessionId);
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
            const response = await axios.get("http://127.0.0.1:5000/get_all_sessions");
            setChatHistory(response.data);
        } catch (error) {
            console.error("Error fetching all chat sessions:", error);
        }
    };

    // ✅ Send message to Flask backend and save
    const sendMessage = async () => {
        if (!message.trim()) return;

        const userMessage = { sender: "user", message: message };
        setCurrentChat((prevChat) => [...prevChat, userMessage]);

        await saveChatToBackend(userMessage);

        try {
            const response = await axios.post("http://127.0.0.1:5000/chat", { question: message });
            const botMessage = { sender: "bot", message: response.data.answer };

            setCurrentChat((prevChat) => [...prevChat, botMessage]);
            await saveChatToBackend(botMessage);
        } catch (error) {
            console.error("Error sending message:", error);
        }

        setMessage(""); // Clear input
    };

    // ✅ Save message to backend (SQLite)
    const saveChatToBackend = async (chatMessage) => {
        try {
            await axios.post("http://127.0.0.1:5000/save_chat", {
                sender: chatMessage.sender,
                message: chatMessage.message,
                session_id: sessionId,
            });
        } catch (error) {
            console.error("Error saving chat:", error);
        }
    };

    // ✅ Start a new chat (Generate a new session)
    const startNewChat = () => {
        const newSessionId = uuidv4();
        localStorage.setItem("sessionId", newSessionId);
        setSessionId(newSessionId);
        setCurrentChat([]);
        fetchAllChatSessions();
    };

    // ✅ Delete a chat session
    const deleteChatSession = async (sessionId) => {
        try {
            await axios.delete(`http://127.0.0.1:5000/delete_chat/${sessionId}`);
            if (selectedChatIndex === sessionId) {
                setCurrentChat([]);
            }
            fetchAllChatSessions();
        } catch (error) {
            console.error("Error deleting chat:", error);
        }
    };

    // ✅ Handle Sign Out
    const handleSignOut = () => {
        localStorage.removeItem("user");
        navigate("/login");
    };

    return (
        <section className="chat-bot">
            <div className="container-fluid">
                {/* ✅ Header Section with User Info */}
                <div className="row head-chat">
                    <div className="col-6">
                        <Link to="/dashboard">
                            <img className="we-img" src="/images/wes.png" alt="Logo" />
                        </Link>
                    </div>
                    <div className="col-6 text-end d-flex align-items-center justify-content-end">
                        <button className="btn btn-primary me-3" onClick={() => navigate("/dashboard")}>
                            Go to Dashboard
                        </button>

                        {/* ✅ User Profile Dropdown */}
                        <div className="profile-section">
                            <span className="username">{user?.username}</span>
                            <div className="profile-dropdown" onClick={() => setDropdownOpen(!dropdownOpen)}>
                                <div className="profile-icon">{user?.username.charAt(0).toUpperCase()}</div>
                                {dropdownOpen && (
                                    <div className="dropdown-menu">
                                        <div className="profile-info">
                                            <div className="profile-avatar">{user?.username.charAt(0).toUpperCase()}</div>
                                            <p className="profile-name">Hi, {user?.username}!</p>
                                        </div>
                                        <hr />
                                        <button className="dropdown-item">My Profile</button>
                                        <button className="dropdown-item sign-out-btn" onClick={handleSignOut}>
                                            Sign Out
                                        </button>
                                    </div>
                                )}
                            </div>
                        </div>
                    </div>
                </div>

                {/* ✅ Chat Interface */}
                <div className="row chat-row">
                    {/* ✅ Left Sidebar - Chat History */}
                    <div className="col-2 bg-chat">
                        <h5 className="text-white">Chat History</h5>
                        {chatHistory.length === 0 ? (
                            <p className="text-white">No previous chats</p>
                        ) : (
                            chatHistory.map((chat, index) => (
                                <div key={chat.session_id} className="d-flex justify-content-between align-items-center mb-2">
                                    <button
                                        className={`chat-history-btn ${selectedChatIndex === chat.session_id ? "active" : ""}`}
                                        onClick={() => fetchChatHistory(chat.session_id)}
                                    >
                                        Chat {index + 1}
                                    </button>
                                    <button
                                        onClick={() => deleteChatSession(chat.session_id)}
                                        className="btn btn-sm btn-danger"
                                        title="Delete Chat"
                                    >
                                        🗑️
                                    </button>
                                </div>
                            ))
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
