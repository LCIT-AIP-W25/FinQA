describe('Forget Password Page', () => {
  beforeEach(() => {
      cy.visit('http://localhost:3000/forget'); // Ensure this route matches your app setup
  });

  it('renders the Forget Password page correctly', () => {
      cy.contains('Forget Password').should('be.visible');
      cy.contains('Please enter your email').should('be.visible');
      cy.get('input[type="email"]').should('exist');
      cy.get('button[type="submit"]').contains('Forget Password').should('exist');
  });

  it('validates empty email field', () => {
      cy.get('button[type="submit"]').click();
      cy.contains('Email is required').should('be.visible');
  });

  it('validates incorrect email format', () => {
      cy.get('input[type="email"]').type('invalidemail');
      cy.get('button[type="submit"]').click();
      cy.contains('Enter a valid email address').should('be.visible');
  });

  it('submits the form with valid email', () => {
      cy.get('input[type="email"]').type('test@example.com');
      cy.get('button[type="submit"]').click();
      cy.url().should('include', '/login');
  });

  it('navigates to signup page when clicking Sign up link', () => {
      cy.contains("Don't have an account?").should('be.visible');
      cy.contains('Sign up').click();
      cy.url().should('include', '/signup');
  });
});
