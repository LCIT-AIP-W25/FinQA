/// <reference types="cypress" />

describe("Login Page Tests", () => {
  beforeEach(() => {
    cy.visit("http://localhost:3000/login"); // Visit the login page before each test
  });

  it("Should render the login page correctly", () => {
    cy.contains("Welcome back!").should("be.visible");
    cy.get("input[type='email']").should("be.visible");
    cy.get("input[type='password']").should("be.visible");
    cy.get(".login-btn").should("be.visible");
  });

  it("Should allow the user to enter email and password", () => {
    cy.get("input[type='email']").type("test@example.com");
    cy.get("input[type='password']").type("Test@12345");
  });

  it("Should show validation messages for empty fields", () => {
    cy.get(".login-btn").click();
    cy.get("input[type='email']:invalid").should("exist");
    cy.get("input[type='password']:invalid").should("exist");
  });

  it("Should navigate to dashboard on successful login", () => {
    cy.get("input[type='email']").type("test@example.com");
    cy.get("input[type='password']").type("Test@12345");
    cy.get(".login-form").submit();
    cy.url().should("include", "/dashboard");
  });

  it("Should navigate to forgot password page", () => {
    cy.get(".forgot-password a").click();
    cy.url().should("include", "/forgot-password");
  });

  it("Should navigate to signup page", () => {
    cy.get(".signup-text a").click();
    cy.url().should("include", "/signup");
  });

  it("Should allow login with Google", () => {
    cy.get(".google-btn").should("be.visible").click();
    // Mock Google OAuth redirection
  });

  it("Should allow login with Facebook", () => {
    cy.get(".facebook-btn").should("be.visible").click();
    // Mock Facebook OAuth redirection
  });
});
