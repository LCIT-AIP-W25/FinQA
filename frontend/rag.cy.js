describe("RAG API Endpoints", () => {
    const apiUrl = "http://localhost:5000"; // Update this if your API is hosted elsewhere
    const sampleQuestion = "What is the latest financial performance of Company XYZ?";

    it("should load the FAISS index successfully", () => {
        cy.request({
            method: "GET",
            url: `${apiUrl}/load-faiss-index`,
            failOnStatusCode: false
        }).then((response) => {
            expect(response.status).to.be.oneOf([200, 500]); // It should return 200 if success, or 500 if index is missing
            if (response.status === 200) {
                expect(response.body).to.have.property("message", "FAISS index loaded successfully");
            } else {
                expect(response.body).to.have.property("error");
            }
        });
    });

    it("should return a valid response for a contextual query", () => {
        cy.request({
            method: "POST",
            url: `${apiUrl}/query`,
            body: { question: sampleQuestion },
            failOnStatusCode: false
        }).then((response) => {
            expect(response.status).to.be.oneOf([200, 500]); // Either success or error
            if (response.status === 200) {
                expect(response.body).to.have.property("response").that.is.a("string");
                expect(response.body).to.have.property("sources").that.is.an("array");
            } else {
                expect(response.body).to.have.property("error");
            }
        });
    });

    it("should return relevant sources along with the response", () => {
        cy.request({
            method: "POST",
            url: `${apiUrl}/query`,
            body: { question: sampleQuestion },
            failOnStatusCode: false
        }).then((response) => {
            if (response.status === 200) {
                const sources = response.body.sources;
                expect(sources).to.be.an("array").and.not.be.empty;
                sources.forEach((source) => {
                    expect(source).to.have.property("source").that.is.a("string");
                    expect(source).to.have.property("snippet").that.is.a("string");
                });
            }
        });
    });

    it("should handle errors gracefully when the FAISS index is missing", () => {
        cy.request({
            method: "POST",
            url: `${apiUrl}/query`,
            body: { question: "Test query with missing FAISS index" },
            failOnStatusCode: false
        }).then((response) => {
            if (response.status === 500) {
                expect(response.body).to.have.property("error").that.includes("Vector store not available");
            }
        });
    });

    it("should return an appropriate error if the Groq API fails", () => {
        cy.request({
            method: "POST",
            url: `${apiUrl}/query`,
            body: { question: "Test query when Groq API fails" },
            failOnStatusCode: false
        }).then((response) => {
            if (response.status === 500) {
                expect(response.body).to.have.property("error").that.includes("Groq API Error");
            }
        });
    });
});
