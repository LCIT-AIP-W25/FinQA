import { render, screen, fireEvent } from "@testing-library/react";
import "@testing-library/jest-dom";
import App from "./App";

describe("App Component", () => {
  test("App launches successfully", () => {
    render(<App />);

    // Check if the header is rendered
    const headerElement = screen.getByRole("banner");
    expect(headerElement).toBeInTheDocument();

    // Check if the logo is rendered
    const logoElement = screen.getByAltText("WealthWiz Logo");
    expect(logoElement).toBeInTheDocument();

    // Check if the title is rendered
    const titleElement = screen.getByText("WealthWiz");
    expect(titleElement).toBeInTheDocument();

    // Check if the main chatbot section is rendered
    const mainElement = screen.getByRole("main");
    expect(mainElement).toBeInTheDocument();

    // Check if the footer is rendered
    const footerElement = screen.getByRole("contentinfo");
    expect(footerElement).toBeInTheDocument();
  });

  test("Theme toggle button switches modes", () => {
    render(<App />);

    // Get the theme toggle button
    const themeToggleButton = screen.getByRole("button", { name: /switch to dark mode/i });
    expect(themeToggleButton).toBeInTheDocument();

    // Simulate a click to enable dark mode
    fireEvent.click(themeToggleButton);
    expect(document.documentElement.classList.contains("dark-theme")).toBe(true);

    // Simulate another click to disable dark mode
    fireEvent.click(themeToggleButton);
    expect(document.documentElement.classList.contains("dark-theme")).toBe(false);
  });

  test("Footer contains privacy policy and terms links", () => {
    render(<App />);

    // Check for Privacy Policy link
    const privacyPolicyLink = screen.getByText("Privacy Policy");
    expect(privacyPolicyLink).toBeInTheDocument();
    expect(privacyPolicyLink).toHaveAttribute("href", "#privacy-policy");

    // Check for Terms of Service link
    const termsLink = screen.getByText("Terms of Service");
    expect(termsLink).toBeInTheDocument();
    expect(termsLink).toHaveAttribute("href", "#terms");
  });
});
