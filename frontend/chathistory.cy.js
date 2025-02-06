describe('ChatHistory Component', () => {
    beforeEach(() => {
      cy.visit('http://localhost:3000'); // Adjust if needed to where the ChatHistory is rendered
    });
  
    it('should display the chat history section', () => {
      cy.get('.chat-history').should('exist');
    });
  
    it('should display the correct heading for chat history', () => {
      cy.get('.chat-history h4').should('contain', '📜 Chat History');
    });
  
    
    it('should display a list of past chat messages', () => {
      cy.get('.chat-history ul').should('exist');
      cy.get('.chat-history ul li').should('have.length', 2); // Ensure there are 2 messages
    });
  
    it('should contain specific chat messages with correct dates', () => {
      cy.get('.chat-history ul li').eq(0).should('contain', 'What is compound interest? (3/10/2024)');
      cy.get('.chat-history ul li').eq(1).should('contain', 'How do I start investing? (3/11/2024)');
    });
  });
  