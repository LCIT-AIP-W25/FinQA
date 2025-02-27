describe("Chat Page", () => {
    beforeEach(() => {
      // Setting up user session before each test
      localStorage.setItem("user", JSON.stringify({ username: "testuser", user_id: "123" }));
      localStorage.setItem("userId", "123");
      cy.intercept("GET", "http://127.0.0.1:5000/get_all_sessions/123", { fixture: "chats.json" });
      cy.intercept("POST", "http://127.0.0.1:5000/query_chatbot", {
        body: { response: "Hello, this is a chatbot response." },
      }).as("sendMessage");
      cy.visit("http://localhost:3000/Chat");
    });
  
    it("should load the chat page correctly", () => {
      cy.get(".chat-app-header-title").should("contain", "WealthWiz AI Chat");
      cy.get(".chat-app-username").should("contain", "testuser");
      cy.get(".chat-app-search-input").should("be.visible");
      cy.get(".chat-app-chat-history-header").should("contain", "Chat History");
    });
  
    it("should search for a company in the search box", () => {
      const searchTerm = "Amazon";
      cy.get(".chat-app-search-input").type(searchTerm);
      cy.get(".chat-app-company-item").should("have.length", 1).and("contain", "Amazon");
    });
  
    it("should select a company from the list", () => {
      cy.get(".chat-app-search-input").type("Google");
      cy.get(".chat-app-company-item").contains("Google").click();
      cy.get(".chat-app-company-item.selected").should("have.text", "Google");
    });
  
    it("should display the chat history", () => {
      cy.get(".chat-app-chat-history").should("be.visible");
      cy.get(".chat-app-chat-item").should("have.length", 2); // Assuming 2 chats in fixture
    });
  
    it("should load the chat session when clicked", () => {
      cy.get(".chat-app-chat-item").first().click();
      cy.wait("@sendMessage");
      cy.get(".chat-app-messages").should("contain", "Hello, this is a chatbot response.");
    });
  
    it("should send a message and receive a bot response", () => {
      cy.get(".chat-app-input").type("How are you?");
      cy.get(".chat-app-send-btn").click();
      cy.wait("@sendMessage");
      cy.get(".chat-app-messages").should("contain", "Hello, this is a chatbot response.");
    });
  
    it("should start a new chat", () => {
      cy.get(".chat-app-new-chat-btn").click();
      cy.get(".chat-app-placeholder").should("contain", "What can I help with?");
      cy.get(".chat-app-chat-history").should("have.length", 3); // Assuming a new session is created
    });
  
    it("should delete a chat session", () => {
      cy.get(".chat-app-chat-item").first().within(() => {
        cy.get(".chat-app-delete-btn").click();
      });
      cy.on("window:confirm", () => true); // Handle the confirmation dialog
      cy.get(".chat-app-chat-history").should("have.length", 1); // Assuming one chat is deleted
    });
  
    it("should handle sign-out correctly", () => {
      cy.get(".chat-app-profile-dropdown").click();
      cy.get(".chat-app-sign-out").click();
      cy.url().should("include", "/login");
      cy.window().then((win) => {
        expect(win.localStorage.getItem("user")).to.be.null;
        expect(win.localStorage.getItem("sessionId")).to.be.null;
      });
    });
  
    afterEach(() => {
      localStorage.clear(); // Cleanup after each test
    });
  });
  