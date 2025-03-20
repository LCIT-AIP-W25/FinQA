/// <reference types="cypress" />
import React from "react";
import { mount } from "cypress/react";
import { LoaderProvider, useLoader } from "../../src/LoaderContext"; // Adjust path accordingly
import GlobalLoader from "../../src/GlobalLoader"; // Adjust path accordingly

// Sample component to toggle loading
const TestComponent = () => {
  const { loading, setLoading } = useLoader();

  return (
    <div>
      <button
        onClick={() => setLoading(true)}
        data-testid="start-loading"
      >
        Start Loading
      </button>
      <button
        onClick={() => setLoading(false)}
        data-testid="stop-loading"
      >
        Stop Loading
      </button>
      <GlobalLoader />
    </div>
  );
};

describe("GlobalLoader Component", () => {
  beforeEach(() => {
    mount(
      <LoaderProvider>
        <TestComponent />
      </LoaderProvider>
    );
  });

  it("should not show the loader when loading is false", () => {
    cy.get(".global-loader-overlay").should("not.exist"); // The loader should not be in the DOM
  });

  it("should show the loader when loading is true", () => {
    cy.get("[data-testid=start-loading]").click(); // Set loading to true
    cy.get(".global-loader-overlay").should("exist"); // The loader should appear
    cy.get(".loader-text").should("have.text", "Processing..."); // Check the text inside loader
  });

  it("should hide the loader when loading is false again", () => {
    cy.get("[data-testid=start-loading]").click(); // Set loading to true
    cy.get(".global-loader-overlay").should("exist"); // Loader should appear
    cy.get("[data-testid=stop-loading]").click(); // Set loading to false
    cy.get(".global-loader-overlay").should("not.exist"); // Loader should disappear
  });
});
