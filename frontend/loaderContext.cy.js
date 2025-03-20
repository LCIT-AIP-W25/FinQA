/// <reference types="cypress" />
import React from "react";
import { mount } from "cypress/react";
import { LoaderProvider, useLoader } from "../../src/LoaderContext"; // Adjust the path as needed

// Sample test component to use the loader context
const TestComponent = () => {
  const { loading, setLoading } = useLoader();

  return (
    <div>
      <p data-testid="loading-status">{loading ? "Loading..." : "Not Loading"}</p>
      <button onClick={() => setLoading(true)} data-testid="start-loading">
        Start Loading
      </button>
      <button onClick={() => setLoading(false)} data-testid="stop-loading">
        Stop Loading
      </button>
    </div>
  );
};

describe("LoaderContext", () => {
  beforeEach(() => {
    mount(
      <LoaderProvider>
        <TestComponent />
      </LoaderProvider>
    );
  });

  it("should initialize loading as false", () => {
    cy.get("[data-testid=loading-status]").should("have.text", "Not Loading");
  });

  it("should update loading state when setLoading is called", () => {
    // Click to set loading to true
    cy.get("[data-testid=start-loading]").click();
    cy.get("[data-testid=loading-status]").should("have.text", "Loading...");

    // Click to set loading to false
    cy.get("[data-testid=stop-loading]").click();
    cy.get("[data-testid=loading-status]").should("have.text", "Not Loading");
  });

  it("should provide the loader context values", () => {
    cy.window().its("React").then((React) => {
      cy.wrap(React.useContext(LoaderContext)).should("have.property", "loading");
      cy.wrap(React.useContext(LoaderContext)).should("have.property", "setLoading");
    });
  });
});
