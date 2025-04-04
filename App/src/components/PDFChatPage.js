import React, { useState, useRef, useEffect } from "react";
import { Link } from "react-router-dom";
import axios from "axios";
import "../styles/ChatPage.css"; // ✅ Uses same styles as ChatPage

const PDFChatPage = () => {
    const [message, setMessage] = useState("");
    const [currentChat, setCurrentChat] = useState([]);
    const [loading, setLoading] = useState(false);
    const chatEndRef = useRef(null); // ✅ Auto-scroll reference

    // ✅ Scroll to bottom on new messages
    useEffect(() => {
        if (chatEndRef.current) {
            chatEndRef.current.scrollIntoView({ behavior: "smooth" });
        }
    }, [currentChat]);

    // ✅ Send user question & get response from backend
    const sendMessage = async () => {
        if (!message.trim()) return;
    
        const userMessage = { sender: "user", message };
        setCurrentChat((prevChat) => [...prevChat, userMessage]);
        setMessage("");
        setLoading(true);
    
        try {
            const response = await axios.post("http://127.0.0.1:5000/query_pdf_chatbot", {
                question: message,
            });
    
            console.log("Response received:", response.data);  // ✅ Add this for debugging
    
            const botMessage = response.data.response
                ? { sender: "bot", message: response.data.response }
                : { sender: "bot", message: "I'm not sure how to respond to that." };
    
            setCurrentChat((prevChat) => [...prevChat, botMessage]);
        } catch (error) {
            console.error("Error querying:", error);
            setCurrentChat((prevChat) => [...prevChat, { sender: "bot", message: "Error retrieving data." }]);
        }
    
        setLoading(false);
    };
    

    return (
        <section className="chat-app-container">
            <div className="chat-app-wrapper">
                {/* ✅ Header Section */}
                <div className="chat-app-header">
                    <div className="chat-app-logo">
                        <Link to="/chat">
                            <img className="chat-app-logo-img" src="/images/wes.png" alt="Logo" />
                        </Link>
                        <h2 className="chat-app-header-title">WealthWiz AI Chat (PDF Mode)</h2>
                    </div>

                    {/* ✅ Profile & Back Button */}
                    <div className="chat-app-user-section">
                        <Link to="/chat" className="chat-app-back-btn">⬅ Go Back</Link>
                    </div>
                </div>

                {/* ✅ Chat Window */}
                <div className="chat-app-window">
                    <div className={`chat-app-messages ${currentChat.length > 0 ? "has-messages" : ""}`}>
                        {currentChat.length === 0 ? (
                            <p className="chat-app-placeholder">Ask something about the uploaded PDF...</p>
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
                        <button onClick={sendMessage} className="chat-app-send-btn" disabled={loading}>
                            {loading ? "Sending..." : "Send"}
                        </button>
                    </div>
                </div>
            </div>
        </section>
    );
};

export default PDFChatPage;
