from flask import Flask, request, jsonify
import pickle
import re
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from flask_cors import CORS
import nltk
nltk.download('wordnet')
nltk.download('omw-1.4')

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing

# Paths to saved artifacts
xgboost_model_path = 'xgboost_model.pkl'
vectorizer_path = 'tfidf_vectorizer.pkl'

# Load the XGBoost model
with open(xgboost_model_path, 'rb') as f:
    xgb_model = pickle.load(f)

# Load the TF-IDF vectorizer
with open(vectorizer_path, 'rb') as f:
    tfidf = pickle.load(f)

# Define preprocessing function
lemmatizer = WordNetLemmatizer()
def preprocess(text):
    text = text.lower()
    text = re.sub(r"[^\w\s]", '', text)
    tokens = word_tokenize(text)
    try:
        tokens = [lemmatizer.lemmatize(token) for token in tokens]
    except Exception as e:
        print(f"Error during lemmatization: {e}")
    # Handle the error, perhaps return a message to the user
    
    return ' '.join(tokens)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    user_input = data.get('input', '')

    if not user_input:
        return jsonify({'error': 'No input provided'}), 400

    # Preprocess the input
    preprocessed_input = preprocess(user_input)

    # Transform input using TF-IDF vectorizer
    input_vectorized = tfidf.transform([preprocessed_input])

    # Predict using the XGBoost model
    prediction = xgb_model.predict(input_vectorized)

    # Map prediction to class
    output_class = 'numerical' if prediction[0] == 1 else 'contextual'

    return jsonify({'input': user_input, 'prediction': output_class})

if __name__ == '__main__':
    app.run(debug=True)
