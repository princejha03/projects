import os
from flask import Flask, request, render_template, jsonify
import pdfplumber
import nltk
import random
from nltk.tokenize import word_tokenize, sent_tokenize
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_PATH'] = 16 * 1024 * 1024  # Limit upload size to 16 MB

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

documents = []

def extract_text_from_pdf(file_path):
    try:
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return ""

def process_text(text):
    return sent_tokenize(text)

# Fun responses for the bot
fun_responses = [
    "Haha, that's hilarious!",
    "You crack me up!",
    "I'm rolling on the floor laughing!",
    "That's comedy gold!"
]

# Function to generate a random fun response
def get_fun_response():
    return random.choice(fun_responses)

# Function to generate a response with personality
def generate_response(query):
    words = word_tokenize(query.lower())
    
    # Check if the query is a greeting
    greetings = ["hello", "hi", "hey", "greetings"]
    if any(word in words for word in greetings):
        return "Hello! How can I assist you today?"
    
    relevant_sentences = [sent for sent in documents if any(word in sent.lower() for word in words)]
    if relevant_sentences:
        response = " ".join(relevant_sentences[:5])
        if random.random() < 0.3:  #Add a random chance for a fun response
            response += "\n" + get_fun_response()
        response += " "  # Add a space after the response
        return response
    return "Sorry, I couldn't find any information related to your query."

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and file.filename.endswith('.pdf'):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        text = extract_text_from_pdf(file_path)
        if not text:
            return jsonify({"error": "Failed to extract text from PDF"}), 500
        
        sentences = process_text(text)
        documents.extend(sentences)
        
        return jsonify({"message": "File uploaded and processed successfully"}), 200
    else:
        return jsonify({"error": "Invalid file type"}), 400

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get("message")
    if not user_message:
        return jsonify({"error": "No message provided"}), 400
    response = generate_response(user_message)
    return jsonify({"response": response})

if __name__ == '__main__':
    nltk.download('punkt')
    app.run(debug=True)
