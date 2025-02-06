describe("Chatbot Test", () => {
  beforeEach(() => {
    // Intercept the chatbot API request BEFORE the test runs
    cy.intercept("POST", "/api/chatbot").as("chatbotResponse");
  });

  it("Tests chatbot response", () => {
    // Visit the dashboard or relevant page
    cy.visit("http://localhost:3000/dashboard");

    // Ensure chatbot input is visible before interacting
    cy.get("#chatbot-input").should("be.visible").type("Hello{enter}");

    // Debug: Confirm request is triggered by logging it
    cy.wait("@chatbotResponse", { timeout: 20000 }).then((interception) => {
      expect(interception.response.statusCode).to.eq(200);
      cy.log("Chatbot response intercepted:", interception.response);
    });

    // Ensure chatbot response area is updated
    cy.get("#chatbot-response").should("be.visible").and("not.be.empty");
  });
});
