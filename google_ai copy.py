import os
import base64
import requests
from dotenv import load_dotenv
from flask import Flask, request, render_template, redirect, url_for, flash
from werkzeug.utils import secure_filename
import uuid

# Load .env file
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

# Gemini model endpoint (using REST API for Python)
MODEL_ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash-preview:generateContent"

# Flask app setup
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def detect_plant_disease(image_path, mime_type):
    """Analyze plant disease using Gemini AI"""
    # Read image and convert to base64
    with open(image_path, "rb") as f:
        image_bytes = f.read()
    image_base64 = base64.b64encode(image_bytes).decode("utf-8")

    # Build request payload (matching the React structure)
    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": "You are an agricultural expert. Analyze the plant image and: Identify the plant, detect any disease, explain simply for a farmer, and suggest treatment and prevention. Avoid technical words."
                    },
                    {
                        "inlineData": {
                            "mimeType": mime_type,
                            "data": image_base64
                        }
                    }
                ]
            }
        ]
    }

    # Send POST request
    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": API_KEY
    }

    response = requests.post(MODEL_ENDPOINT, json=payload, headers=headers)

    if response.status_code == 200:
        result_json = response.json()
        # Extract text from response
        if 'candidates' in result_json and len(result_json['candidates']) > 0:
            return result_json['candidates'][0]['content']['parts'][0]['text']
        else:
            return "No response generated"
    else:
        return f"Error: {response.status_code} - {response.text}"

@app.route('/', methods=['GET', 'POST'])
def index():
    response = ""
    image_path = None
    loading = False

    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            unique_filename = f"{uuid.uuid4()}_{filename}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            file.save(filepath)

            loading = True
            image_path = filepath

            # Analyze the image
            mime_type = file.mimetype or 'image/jpeg'
            analysis_result = detect_plant_disease(filepath, mime_type)
            response = analysis_result
            loading = False

    return render_template('google_ai_index.html',
                         response=response,
                         image_path=image_path,
                         loading=loading)

def allowed_file(filename):
    """Check if file extension is allowed"""
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'bmp'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

if __name__ == '__main__':
    app.run(debug=True)