import React, { useState, useEffect } from "react";
import "../styles/ChatApp.css";

function ChatApp() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [chatHistory, setChatHistory] = useState([]);

  // Fetch previous chat messages
  useEffect(() => {
    fetchMessages();
  }, []);

  const fetchMessages = () => {
    fetch("http://localhost:5000/api/messages")
      .then((response) => response.json())
      .then((data) => {
        console.log("📜 Fetched chat history:", data);
        setMessages(data);
        setChatHistory(data.map((chat, index) => `Chat ${index + 1}`)); // Display chat history as dummy names
      })
      .catch((error) => console.error("❌ Error fetching messages:", error));
  };

  const sendMessage = () => {
    if (!input.trim()) return;
  
    const userMessage = { user: "User", message: input };
  
    fetch("http://localhost:5000/api/messages", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(userMessage),
    })
      .then(() => {
        fetchMessages(); // Refresh messages
        setInput("");
  
        // Simulate a bot response
        setTimeout(() => {
          const botMessage = { user: "Bot", message: "This is a dummy bot reply!" };
          fetch("http://localhost:5000/api/messages", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(botMessage),
          }).then(fetchMessages);
        }, 1000);
      })
      .catch((error) => console.error("❌ Error sending message:", error));
  };  

  return (
    <div className="chat-container">
      <div className="chat-sidebar">
        <h3>Chat History</h3>
        <ul>
          {chatHistory.length > 0 ? (
            chatHistory.map((history, index) => (
              <li key={index} className="chat-history-item">
                {history}
              </li>
            ))
          ) : (
            <p className="no-messages">No chat history yet.</p>
          )}
        </ul>
      </div>

      <div className="chat-box">
        <h2>Chat</h2>
        <div className="chat-messages">
          {messages.length > 0 ? (
            messages.map((msg, index) => (
              <p key={index} className="chat-message">
                <strong>{msg.user}:</strong> {msg.message} <br />
                <em style={{ fontSize: "10px", color: "gray" }}>{msg.timestamp}</em>
              </p>
            ))
          ) : (
            <p className="no-messages">Start a conversation...</p>
          )}
        </div>

        <div className="chat-input-container">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Send a message..."
            className="chat-input"
          />
          <button onClick={sendMessage} className="send-button">📩</button>
        </div>
      </div>
    </div>
  );
}

export default ChatApp;
