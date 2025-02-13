describe('Signup Page', () => {
    beforeEach(() => {
      // Visit the signup page before each test
      cy.visit('http://localhost:3000/signup');
    });
  
    it('should render the signup form with Full Name, Email, Password fields', () => {
      cy.get('h2').contains('Sign Up'); // Check if the Sign Up heading exists
      cy.get('input[type="text"]').should('be.visible'); // Check for Full Name input field
      cy.get('input[type="email"]').should('be.visible'); // Check for Email input field
      cy.get('input[type="password"]').should('be.visible'); // Check for Password input field
      cy.get('button[type="submit"]').contains('Sign Up'); // Check if sign up button is visible
    });
  
    it('should allow a user to type in the Full Name, Email, and Password fields', () => {
      cy.get('input[type="text"]').type('John Doe').should('have.value', 'John Doe');
      cy.get('input[type="email"]').type('user@example.com').should('have.value', 'user@example.com');
      cy.get('input[type="password"]').type('password123').should('have.value', 'password123');
    });
  
    it('should navigate to /login page when clicking on the "Login" link', () => {
      cy.get('p').contains("Already have an account?").find('a').contains('Login');
      cy.get('a').click();
      cy.url().should('include', '/login'); // Ensure we navigate to the login page
    });
  
    it('should prevent submission if any input field is empty', () => {
      // Leave Full Name empty and try to submit
      cy.get('input[type="text"]').clear();
      cy.get('input[type="email"]').type('user@example.com');
      cy.get('input[type="password"]').type('password123');
      cy.get('button[type="submit"]').click();
  
      // Wait for the focus event to trigger
      cy.wait(500); // Optional, for debugging purposes
      cy.get('input[type="text"]').should('have.focus'); // Focus should stay on Full Name field
  
      // Now leave Email empty and try to submit
      cy.get('input[type="text"]').type('John Doe');
      cy.get('input[type="email"]').clear();
      cy.get('input[type="password"]').type('password123');
      cy.get('button[type="submit"]').click();
  
      // Wait for the focus event to trigger
      cy.wait(1000); // Optional, for debugging purposes
      cy.get('input[type="email"]').should('have.focus'); // Focus should stay on Email field
  
      // Now leave Password empty and try to submit
      cy.get('input[type="text"]').type('John Doe');
      cy.get('input[type="email"]').type('user@example.com');
      cy.get('input[type="password"]').clear();
      cy.get('button[type="submit"]').click();
  
      // Wait for the focus event to trigger
      cy.wait(1000); // Optional, for debugging purposes
      cy.get('input[type="password"]').should('have.focus'); // Focus should stay on Password field
    });
  });
  