describe('Authentication API Tests', () => {
    
    const baseUrl = 'http://localhost:5001';
  
    const testUser = {
      username: 'testuser',
      email: 'testuser@example.com',
      password: 'Test@1234'
    };
  
    it('Should sign up a new user successfully', () => {
      cy.request({
        method: 'POST',
        url: `${baseUrl}/signup`,
        body: testUser,
        failOnStatusCode: false,
      }).then((response) => {
        expect(response.status).to.be.oneOf([200, 400]);
        if (response.status === 400) {
          expect(response.body.message).to.equal('Email already registered.');
        } else {
          expect(response.body.message).to.equal('User registered successfully.');
        }
      });
    });
  
    it('Should not sign up with existing email', () => {
      cy.request({
        method: 'POST',
        url: `${baseUrl}/signup`,
        body: testUser,
        failOnStatusCode: false,
      }).then((response) => {
        expect(response.status).to.equal(400);
        expect(response.body.message).to.equal('Email already registered.');
      });
    });
  
    it('Should log in successfully with valid credentials', () => {
      cy.request({
        method: 'POST',
        url: `${baseUrl}/login`,
        body: {
          email: testUser.email,
          password: testUser.password,
        },
        failOnStatusCode: false,
      }).then((response) => {
        expect(response.status).to.equal(200);
        expect(response.body.status).to.equal('success');
        expect(response.body).to.have.property('user_id');
      });
    });
  
    it('Should not log in with invalid credentials', () => {
      cy.request({
        method: 'POST',
        url: `${baseUrl}/login`,
        body: {
          email: testUser.email,
          password: 'WrongPassword',
        },
        failOnStatusCode: false,
      }).then((response) => {
        expect(response.status).to.equal(401);
        expect(response.body.message).to.equal('Invalid credentials.');
      });
    });
  
    it('Should send a password reset link for existing email', () => {
      cy.request({
        method: 'POST',
        url: `${baseUrl}/forget_password`,
        body: { email: testUser.email },
        failOnStatusCode: false,
      }).then((response) => {
        expect(response.status).to.equal(200);
        expect(response.body.message).to.equal('Password reset link sent to your email.');
      });
    });
  
    it('Should return error for non-registered email in forgot password', () => {
      cy.request({
        method: 'POST',
        url: `${baseUrl}/forget_password`,
        body: { email: 'nonexistent@example.com' },
        failOnStatusCode: false,
      }).then((response) => {
        expect(response.status).to.equal(404);
        expect(response.body.message).to.equal('Email not registered.');
      });
    });
  });
  