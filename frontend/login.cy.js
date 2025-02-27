describe('Login Page', () => {
    beforeEach(() => {
      // Clear localStorage before each test to ensure a clean state
      localStorage.clear();
      cy.visit('http://localhost:3000/login'); // Visit the login page
    });
  
    it('should render the login form correctly', () => {
      // Ensure the login form and fields are visible
      cy.get('form').should('exist');
      cy.get('input[type="email"]').should('be.visible');
      cy.get('input[type="password"]').should('be.visible');
      cy.get('button[type="submit"]').contains('Sign in').should('be.visible');
      cy.get('a').contains('Forgot password?').should('be.visible');
      cy.get('a').contains('Sign up').should('be.visible');
    });
  
    it('should show an error message for invalid email format', () => {
      cy.get('input[type="email"]').type('invalid-email');
      cy.get('button[type="submit"]').click();
      
      // Check that the error message for the email is shown
      cy.contains('Enter a valid email address').should('be.visible');
    });
  
    it('should show an error message if email is missing', () => {
      cy.get('input[type="email"]').clear();
      cy.get('button[type="submit"]').click();
      
      // Check that the email required error is shown
      cy.contains('Email is required').should('be.visible');
    });
  
    it('should show an error message for invalid password (too short)', () => {
      cy.get('input[type="email"]').type('validemail@example.com');
      cy.get('input[type="password"]').type('123');
      cy.get('button[type="submit"]').click();
      
      // Check that the password error message is shown
      cy.contains('Password must be at least 6 characters long').should('be.visible');
    });
  
    it('should show an error message if password is missing', () => {
      cy.get('input[type="email"]').type('validemail@example.com');
      cy.get('input[type="password"]').clear();
      cy.get('button[type="submit"]').click();
      
      // Check that the password required error is shown
      cy.contains('Password is required').should('be.visible');
    });
  
    it('should submit the form with valid data and redirect to chat page', () => {
      const mockResponse = {
        status: 'success',
        user_id: '12345',
        user: { username: 'testuser' }
      };
      
      // Mock the API call to simulate a successful login
      cy.intercept('POST', 'http://127.0.0.1:5001/login', {
        statusCode: 200,
        body: mockResponse,
      }).as('loginRequest');
  
      cy.get('input[type="email"]').type('validemail@example.com');
      cy.get('input[type="password"]').type('validpassword');
      cy.get('button[type="submit"]').click();
      
      // Wait for the intercepted login request
      cy.wait('@loginRequest');
      
      // Check if localStorage contains the correct user data
      cy.window().then((win) => {
        expect(win.localStorage.getItem('user')).to.exist;
        expect(win.localStorage.getItem('userId')).to.equal('12345');
      });
  
      // Ensure the user is redirected to the Chat page
      cy.url().should('include', '/Chat');
    });
  
    it('should show an error message if login fails', () => {
      const mockErrorResponse = {
        status: 'error',
        message: 'Invalid email or password.',
      };
  
      // Mock the API call to simulate a failed login
      cy.intercept('POST', 'http://127.0.0.1:5001/login', {
        statusCode: 401,
        body: mockErrorResponse,
      }).as('loginRequest');
  
      cy.get('input[type="email"]').type('validemail@example.com');
      cy.get('input[type="password"]').type('wrongpassword');
      cy.get('button[type="submit"]').click();
      
      // Wait for the intercepted login request
      cy.wait('@loginRequest');
      
      // Check if the error message is displayed
      cy.contains('Invalid email or password.').should('be.visible');
    });
  
    it('should toggle password visibility when clicking the eye icon', () => {
      cy.get('input[type="password"]').type('validpassword');
      
      // Ensure the password is initially hidden
      cy.get('input[type="password"]').should('have.attr', 'type', 'password');
      
      // Click the eye icon to show the password
      cy.get('button[type="button"]').click();
      
      // Ensure the password is now visible
      cy.get('input[type="password"]').should('have.attr', 'type', 'text');
      
      // Click the eye icon again to hide the password
      cy.get('button[type="button"]').click();
      
      // Ensure the password is hidden again
      cy.get('input[type="password"]').should('have.attr', 'type', 'password');
    });
  });
  