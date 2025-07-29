import React, { useState, useRef, useEffect } from "react";
import { Link , useNavigate} from "react-router-dom";
import axios from "axios";
import "../styles/PDFChatPage.css"; //  Uses same styles as ChatPage

const PDFChatPage = () => {
    const [message, setMessage] = useState("");
    const [currentChat, setCurrentChat] = useState([]);
    const [loading, setLoading] = useState(false);
    const chatEndRef = useRef(null); //  Auto-scroll reference
    const CHATBOT_API_URL = process.env.REACT_APP_CHATBOT_API_URL || "http://127.0.0.1:5000";
    const user_id = localStorage.getItem("pdfChat_userId");
    const filename = localStorage.getItem("pdfChat_filename");
    const navigate = useNavigate();

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

  
    // ✅ Block access with a redirect inside useEffect
    useEffect(() => {
          if (!user_id || !filename) {
              alert("⚠️ Please upload a PDF before using this feature.");
              navigate("/chat");
          }
      }, [user_id, filename, navigate]);

    //  Scroll to bottom on new messages
    useEffect(() => {
        if (chatEndRef.current) {
            chatEndRef.current.scrollIntoView({ behavior: "smooth" });
        }
    }, [currentChat]);
    
    
    //  Send user question & get response from backend
    const sendMessage = async () => {
        if (!message.trim()) return;
    
        const userMessage = { sender: "user", message };
        setCurrentChat((prevChat) => [...prevChat, userMessage]);
        setMessage("");
        setLoading(true);


        if (!user_id || !filename) {
            alert("Missing file or user context. Please upload a PDF again.");
            return;
        }
    
        try {
            const response = await axios.post(`${CHATBOT_API_URL}/query_pdf_chatbot`, {
                question: message,
                user_id: user_id,
                filename: filename
            });
            
    
            console.log("Response received:", response.data);  //  Add this for debugging
    
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
        <section className="PDF-chat-app-container">
            <div className="PDF-chat-app-wrapper">
                {/* ✅ Header Section */}
                <div className="PDF-chat-app-header">
                    <div className="PDF-chat-app-logo">
                        <Link to="/chat">
                            <img className="PDF-chat-app-logo-img" src="/images/Logo.png" alt="Logo" />
                        </Link>
                        <h2 className="PDF-chat-app-header-title">WealthWiz AI (PDF Mode)</h2>
                    </div>

                    {/* ✅ Profile & Back Button */}
                    <div className="PDF-chat-app-user-section">
                        <Link to="/chat" className="PDF-chat-app-back-btn">⬅ Back</Link>
                    </div>
                </div>

                {/* ✅ Chat Window */}
                <div className="PDF-chat-app-window">
                    <div className={`PDF-chat-app-messages ${currentChat.length > 0 ? "has-messages" : ""}`}>
                        {currentChat.length === 0 ? (
                            <p className="PDF-chat-app-placeholder">Ask anything about the uploaded PDF...</p>
                        ) : (
                            currentChat.map((msg, idx) => (
                                <p key={idx} className={msg.sender === "user" ? "PDF-chat-app-user-message" : "PDF-chat-app-bot-message"}>
                                    {msg.message}
                                </p>
                            ))
                        )}
                        <div ref={chatEndRef}></div>
                    </div>

                    {/* ✅ Chat Input Box */}
                    <div className="PDF-chat-app-input-section">
                        <input
                            type="text"
                            className="PDF-chat-app-input"
                            placeholder="Type a message..."
                            value={message}
                            onChange={(e) => setMessage(e.target.value)}
                            onKeyPress={(e) => e.key === "Enter" && sendMessage()}
                        />
                        <button onClick={sendMessage} className="PDF-chat-button send" disabled={loading}>
                            {loading ? "Sending..." : "✉️ Send"}
                        </button>
                    </div>
                </div>
            </div>
        </section>
    );
};

export default PDFChatPage;
