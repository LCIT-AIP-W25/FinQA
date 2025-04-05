// ChatHistorySidebar.js
import React from "react";
import "../styles/ChatHistorySidebar.css";

function ChatHistorySidebar({
  className = "chat-app-sidebar", // allows dynamic visibility class
  searchTerm,
  setSearchTerm,
  companyList,
  selectedCompany,
  setSelectedCompany,
  chatHistory,
  sessionId,
  loadChatSession,
  deleteChatSession,
  getOrGenerateTitle,
  setShowChatSidebar
}) {
  return (
    <div className={className}>

      {/* Chat History Section */}
      <h5 className="chat-app-chat-history-header">Chat History</h5>
      {chatHistory.length === 0 ? (
        <p>No previous chats</p>
      ) : (
        <div className="chat-app-chat-history">
          {chatHistory.map((chat) => (
            <div
              key={chat.session_id}
              className={`chat-app-chat-item ${sessionId === chat.session_id ? "active" : ""}`}
              onClick={() => {
                loadChatSession(chat.session_id);
                if (window.innerWidth < 768) {
                  setShowChatSidebar(false);  // Auto-close on mobile
                }
              }}              
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
      )}
    </div>
  );
}

export default ChatHistorySidebar;
