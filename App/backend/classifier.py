import pickle
import re
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import nltk
nltk.download('wordnet')

# Paths to saved artifacts
xgboost_model_path = 'artifacts/rf_model.pkl'
vectorizer_path = 'artifacts/tfidf_vectorizer 2.pkl'

# Load the XGBoost model
with open(xgboost_model_path, 'rb') as f:
    xgb_model = pickle.load(f)
    print(f"✅ Loaded XGBoost model from {xgboost_model_path}")

# Load the TF-IDF vectorizer
with open(vectorizer_path, 'rb') as f:
    tfidf = pickle.load(f)
    print(f"✅ Loaded TF-IDF vectorizer from {vectorizer_path}")

# ✅ Define the preprocessing function
lemmatizer = WordNetLemmatizer()

def preprocess(text):
    """Preprocess the input text."""
    text = text.lower()  # Convert to lowercase
    text = re.sub(r"[^\w\s]", '', text)  # Remove punctuation
    tokens = word_tokenize(text)
    tokens = [lemmatizer.lemmatize(token) for token in tokens]  # Lemmatize each token
    return ' '.join(tokens)

# ✅ Classification function
def classify_question(user_input):
    """
    Classifies the user input as either 'numerical' or 'contextual'.
    
    Args:
        user_input (str): The text input from the user.
    
    Returns:
        str: 'numerical' if numerical, 'contextual' otherwise.
    """
    preprocessed_input = preprocess(user_input)
    input_vectorized = tfidf.transform([preprocessed_input])
    prediction = xgb_model.predict(input_vectorized)
    return 'numerical' if prediction[0] == 1 else 'contextual'

# ✅ Example usage for testing
if __name__ == "__main__":
    input_user = "What is the percentage change in revenue?"
    result = classify_question(input_user)
    print(f"Input: {input_user}")
    print(f"Prediction: {result}")
