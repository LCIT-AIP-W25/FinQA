describe('Signup Form', () => {
    beforeEach(() => {
      // Visit the Signup page
      cy.visit('http://localhost:3000/signup');
    });
  
    it('should display the signup form correctly', () => {
      // Check for presence of form elements
      cy.get('input[name="name"]').should('be.visible');
      cy.get('input[name="email"]').should('be.visible');
      cy.get('input[name="password"]').should('be.visible');
      cy.get('button[type="submit"]').contains('Sign up').should('be.visible');
      cy.get('a').contains('Login').should('be.visible');
    });
  
    it('should show error when required fields are not filled', () => {
      // Submit form with empty fields
      cy.get('button[type="submit"]').click();
  
      // Check for validation error messages
      cy.get('.error-text').should('contain', 'Full name is required');
      cy.get('.error-text').should('contain', 'Email is required');
      cy.get('.error-text').should('contain', 'Password is required');
    });
  
    it('should show error for invalid email format', () => {
      // Fill invalid email
      cy.get('input[name="name"]').type('John Doe');
      cy.get('input[name="email"]').type('invalid-email');
      cy.get('input[name="password"]').type('Password123');
  
      // Submit form
      cy.get('button[type="submit"]').click();
  
      // Check for invalid email error
      cy.get('.error-text').should('contain', 'Enter a valid email address');
    });
  
    it('should show error for password less than 6 characters', () => {
      // Fill short password
      cy.get('input[name="name"]').type('John Doe');
      cy.get('input[name="email"]').type('johndoe@example.com');
      cy.get('input[name="password"]').type('short');
  
      // Submit form
      cy.get('button[type="submit"]').click();
  
      // Check for password length error
      cy.get('.error-text').should('contain', 'Password must be at least 6 characters long');
    });
  
    it('should successfully submit the form with valid data', () => {
      // Intercept API request and mock success response
      cy.intercept('POST', 'http://127.0.0.1:5001/signup', {
        statusCode: 200,
        body: {
          status: 'success',
          user_id: 1,
          username: 'John Doe',
          email: 'johndoe@example.com',
        },
      }).as('signupRequest');
  
      // Fill in valid form data
      cy.get('input[name="name"]').type('John Doe');
      cy.get('input[name="email"]').type('johndoe@example.com');
      cy.get('input[name="password"]').type('Password123');
  
      // Submit form
      cy.get('button[type="submit"]').click();
  
      // Wait for the API request to finish
      cy.wait('@signupRequest');
  
      // Verify localStorage was set
      cy.window().then((win) => {
        expect(win.localStorage.getItem('user')).to.exist;
        expect(win.localStorage.getItem('userId')).to.exist;
      });
  
      // Check if redirection happens to the login page
      cy.url().should('include', '/login');
    });
  
    it('should toggle password visibility', () => {
      // Initially password input type should be 'password'
      cy.get('input[name="password"]').should('have.attr', 'type', 'password');
  
      // Click on toggle button to show password
      cy.get('button').click();
  
      // Password input type should change to 'text'
      cy.get('input[name="password"]').should('have.attr', 'type', 'text');
  
      // Click again to hide password
      cy.get('button').click();
  
      // Password input type should revert to 'password'
      cy.get('input[name="password"]').should('have.attr', 'type', 'password');
    });
  
    it('should show error when user already exists', () => {
      // Intercept API request and mock error response (user already exists)
      cy.intercept('POST', 'http://127.0.0.1:5001/signup', {
        statusCode: 400,
        body: { message: 'User already exists' },
      }).as('signupRequest');
  
      // Fill in valid form data
      cy.get('input[name="name"]').type('John Doe');
      cy.get('input[name="email"]').type('johndoe@example.com');
      cy.get('input[name="password"]').type('Password123');
  
      // Submit form
      cy.get('button[type="submit"]').click();
  
      // Wait for the API request to finish
      cy.wait('@signupRequest');
  
      // Check for error message
      cy.get('.error-text').should('contain', 'User already exists');
    });
  
    it('should redirect to login page when clicking on "Login" link', () => {
      // Click on "Login" link
      cy.get('a').contains('Login').click();
  
      // Verify the URL contains '/login'
      cy.url().should('include', '/login');
    });
  });
  