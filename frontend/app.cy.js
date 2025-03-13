describe('Chatbot API Tests', () => {
    const baseUrl = 'http://127.0.0.1:5000';
    let sessionId = '';
    let userId = 'test_user';
    
    // ✅ Test Creating a New Chat Session
    it('Should create a new chat session', () => {
        cy.request('POST', `${baseUrl}/new_session`, { user_id: userId })
            .then((response) => {
                expect(response.status).to.eq(201);
                expect(response.body).to.have.property('session_id');
                expect(response.body).to.have.property('title');
                sessionId = response.body.session_id;
            });
    });
    
    // ✅ Test Saving a Chat Message
    it('Should save a chat message', () => {
        cy.request('POST', `${baseUrl}/save_chat`, {
            session_id: sessionId,
            user_id: userId,
            sender: 'user',
            message: 'Hello, chatbot!'
        }).then((response) => {
            expect(response.status).to.eq(201);
            expect(response.body.status).to.eq('Message saved!');
        });
    });
    
    // ✅ Test Retrieving Chat Sessions
    it('Should retrieve chat sessions for the user', () => {
        cy.request('GET', `${baseUrl}/get_sessions/${userId}`)
            .then((response) => {
                expect(response.status).to.eq(200);
                expect(response.body).to.be.an('array');
                expect(response.body.length).to.be.greaterThan(0);
            });
    });
    
    // ✅ Test Retrieving Chats for a Session
    it('Should retrieve chats for a session', () => {
        cy.request('GET', `${baseUrl}/get_chats/${sessionId}`)
            .then((response) => {
                expect(response.status).to.eq(200);
                expect(response.body).to.be.an('array');
                expect(response.body[0]).to.have.property('sender', 'user');
                expect(response.body[0]).to.have.property('message', 'Hello, chatbot!');
            });
    });
    
    // ✅ Test Querying the Chatbot
    it('Should query the chatbot and get a response', () => {
        cy.request('POST', `${baseUrl}/query_chatbot`, {
            question: 'What is the revenue for Q1?',
            session_id: sessionId,
            user_id: userId,
            selected_company: 'TestCorp'
        }).then((response) => {
            expect(response.status).to.eq(200);
            expect(response.body).to.have.property('response');
        });
    });
    
    // ✅ Test Deleting a Chat Session
    it('Should delete a chat session', () => {
        cy.request('DELETE', `${baseUrl}/delete_chat/${sessionId}`)
            .then((response) => {
                expect(response.status).to.eq(200);
                expect(response.body.status).to.eq('Chat deleted successfully!');
            });
    });
});
