import requests
from flask import Flask, render_template, request, jsonify

app = Flask(_name_)

# The public API endpoint for LibreTranslate
LIBRETRANSLATE_API_URL = "https://libretranslate.de/translate"

# A list of supported languages with their codes for the dropdown menus
# You can add more languages by checking the LibreTranslate documentation
LANGUAGES = {
    'en': 'English',
    'hi': 'Hindi',
    'ml': 'Malayalam',
    'es': 'Spanish',
    'fr': 'French',
    'de': 'German',
    'ko': 'Korean',
    'ja': 'Japanese'
}

@app.route('/')
def index():
    """Renders the main translation page."""
    # Pass the language dictionary to the template
    return render_template('index.html', languages=LANGUAGES)

@app.route('/translate', methods=['POST'])
def translate_tweet():
    """Handles the translation request from the frontend."""
    data = request.json
    tweet_text = data.get('text')
    source_lang = data.get('source')
    target_lang = data.get('target')

    # Basic input validation
    if not tweet_text or not source_lang or not target_lang:
        return jsonify({"error": "Missing input data."}), 400

    # The payload for the LibreTranslate API request
    payload = {
        "q": tweet_text,
        "source": source_lang,
        "target": target_lang
    }
    
    try:
        # Make the POST request to the LibreTranslate API
        response = requests.post(LIBRETRANSLATE_API_URL, json=payload)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        translated_text = response.json().get('translatedText')
        
        # Return the translated text as a JSON response
        return jsonify({"translated_text": translated_text})
    except requests.exceptions.RequestException as e:
        # Handle potential network or API errors
        return jsonify({"error": f"Translation API error: {e}"}), 500

if _name_ == '_main_':
    # Run the Flask development server
    app.run(debug=True)
