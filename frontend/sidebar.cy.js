/// <reference types="cypress" />
import React from "react";
import Sidebar from "../../src/components/Sidebar";
import { mount } from "cypress/react"; // Import mount from Cypress React library

describe("Sidebar Component", () => {
  beforeEach(() => {
    cy.visit("http://localhost:3000/dashboard");
    mount(<Sidebar />); // Use mount correctly
    cy.get('[data-cy-root]').should('exist'); // Ensure it's mounted
  });

  it("should display the profile information", () => {
    cy.get(".profile h3").should("contain.text", "Komal Negah");
    cy.get(".profile img").should("have.attr", "src", "/profile-pic.jpg");
  });

  it("should open the favorites dialog when clicking on 'Favorite Companies'", () => {
    cy.get(".favorites h4").click();
    cy.get(".MuiDialog-root").should("be.visible");
    cy.contains("Select Favorite Companies").should("exist");
  });

  it("should close the favorites dialog when clicking 'Close'", () => {
    cy.get(".favorites h4").click();
    cy.get(".MuiDialog-root").should("be.visible");
    cy.contains("Close").click();
    cy.get(".MuiDialog-root").should("not.exist");
  });

  it("should select and display favorite companies", () => {
    cy.get(".favorites h4").click();
    
    cy.contains("Apple").prev("input").check();
    cy.contains("Microsoft").prev("input").check();
    
    cy.contains("Close").click();
    
    cy.get(".favorites ul").should("contain.text", "Apple");
    cy.get(".favorites ul").should("contain.text", "Microsoft");
  });

  it("should unselect a company and remove it from the list", () => {
    cy.get(".favorites h4").click();
    
    cy.contains("Apple").prev("input").check();
    cy.contains("Close").click();
    
    cy.get(".favorites ul").should("contain.text", "Apple");
    
    cy.get(".favorites h4").click();
    cy.contains("Apple").prev("input").uncheck();
    cy.contains("Close").click();
    
    cy.get(".favorites ul").should("not.contain.text", "Apple");
  });
});
