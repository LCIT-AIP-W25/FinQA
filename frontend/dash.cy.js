describe('Dashboard Component Tests', () => {
    beforeEach(() => {
      cy.visit('http://localhost:3000/dashboard'); // Adjust the path as necessary
    });
  
    it('should display the sidebar and header', () => {
      cy.get('.sidebar').should('be.visible');
      cy.get('.header').should('be.visible');
    });
  
    it('should toggle the sidebar on button click', () => {
      cy.get('.sidebar-toggle').click();
      cy.get('.sidebar').should('not.be.visible');
      cy.get('.sidebar-toggle').click();
      cy.get('.sidebar').should('be.visible');
    });
  
    it('should navigate to profile when clicking the profile image', () => {
      cy.get('.img-profile').click();
      cy.get('.profile-menu').should('be.visible');
    });
  
    it('should close the profile dropdown when clicking outside', () => {
      cy.get('.img-profile').click();
      cy.get('.profile-menu').should('be.visible');
      cy.get('body').click(0, 0); // Click outside
      cy.get('.profile-menu').should('not.be.visible');
    });
  
    it('should navigate to a different page when clicking sidebar links', () => {
      cy.get('.sidebar a').contains('Dashboard').click();
      cy.url().should('include', '/dashboard');
      
      cy.get('.sidebar a').contains('Settings').click();
      cy.url().should('include', '/settings');
    });
  
    it('should resize and toggle mobile view', () => {
      cy.viewport(500, 800);
      cy.get('.sidebar').should('not.be.visible');
      cy.get('.sidebar-toggle').click();
      cy.get('.sidebar').should('be.visible');
    });
  });
  