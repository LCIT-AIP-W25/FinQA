import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def init_groq_llm():
    """Initialize the Groq LLM."""
    try:
        llm = ChatGroq(
            groq_api_key=GROQ_API_KEY,
            model_name="mixtral-8x7b-32768",
            temperature=0.1
        )
        print("✅ Groq LLM initialized")
        return llm
    except Exception as e:
        print(f"❌ Groq LLM initialization failed: {e}")
        return None

def generate_answer(llm, question, retrieved_docs):
    """Generate an answer based on retrieved documents."""
    try:
        context = "\n\n".join([doc.page_content for doc in retrieved_docs])
        prompt = (
            "You are a financial analyst assistant. Answer the question based on the provided context.\n\n"
            f"Context:\n{context}\n\nQuestion: {question}\n\n"
            "Provide a concise and precise answer."
        )
        response = llm.invoke(prompt)
        answer = response.content
        print("✅ Answer generated successfully")
        return answer
    except Exception as e:
        print(f"❌ Answer generation failed: {e}")
        return "Error generating answer."

def validate_answer(answer):
    """Validate the generated answer."""
    if answer and not answer.startswith("Error"):
        print("✅ Answer generation validation successful")
        return True
    else:
        print("❌ Answer generation validation failed")
        return False

if __name__ == "__main__":
    # Test generation
    llm = init_groq_llm()
    if llm:
        sample_question = "What are AMD's forward-looking statements about?"
        sample_docs = [type("Doc", (), {"page_content": "AMD expects growth in AI."})()]
        answer = generate_answer(llm, sample_question, sample_docs)
        print(f"Answer: {answer}")
        validate_answer(answer)