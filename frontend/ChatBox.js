import React, { useState } from "react";
import "./Chatbox.css";
import { FaPaperPlane } from 'react-icons/fa';



const ChatBox = () => {
  const [input, setInput] = useState("");
  const [response, setResponse] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    const requestBody = { input };

    try {
      const res = await fetch("http://127.0.0.1:5000/predict", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(requestBody),
      });

      const data = await res.json();
      if (data.prediction) {
        setResponse(`Prediction: ${data.prediction}`);
      } else {
        setResponse("Error: Unable to process request");
      }
    } catch (error) {
      setResponse("Error connecting to the server");
    }
  };

  return (
    <div className="chat-box-container">
      <div className="chat-box">
        <div className="response-container">
          {response && <p className="bot-response">{response}</p>}
        </div>
        <form onSubmit={handleSubmit} className="chat-input">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask a financial question..."
            required
          />
         <button type="submit" className="send-button">
                    <FaPaperPlane />
                </button>
        </form>
      </div>
    </div>
  );
};

export default ChatBox;
