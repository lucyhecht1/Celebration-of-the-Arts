import os
import json
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
import sqlite3
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from flask import Flask, render_template
from flask_compress import Compress

app = Flask(__name__)
Compress(app)  # Enable compression

# Load environment variables from .env file
load_dotenv()

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
google_credentials_json = os.getenv("GOOGLE_CREDENTIALS_JSON")
creds_dict = None

if google_credentials_json:
    try:
        creds_dict = json.loads(google_credentials_json)
        # Fix private key formatting
        private_key = creds_dict.get("private_key", "")
        # Replace escaped newlines with actual newlines
        private_key = private_key.replace("\\n", "\n")
        # Fix header/footer if they're missing spaces
        private_key = private_key.replace("-----BEGINPRIVATEKEY-----", "-----BEGIN PRIVATE KEY-----")
        private_key = private_key.replace("-----ENDPRIVATEKEY-----", "-----END PRIVATE KEY-----")
        # Ensure proper formatting
        if not private_key.startswith("-----BEGIN"):
            print("⚠️  Warning: Private key format may be invalid")
        creds_dict["private_key"] = private_key

        print("✅ Google Credentials Loaded Successfully")
        print(f"Private Key Exists: {'private_key' in creds_dict}")
        print(f"First 50 characters of Private Key: {creds_dict.get('private_key', '')[:50]}")

    except json.JSONDecodeError:
        print("⚠️  Warning: Failed to parse GOOGLE_CREDENTIALS_JSON. Google Sheets will be disabled.")
        creds_dict = None
    except KeyError as e:
        print(f"⚠️  Warning: Missing required field in credentials: {e}. Google Sheets will be disabled.")
        creds_dict = None
else:
    print("⚠️  Warning: GOOGLE_CREDENTIALS_JSON not set. Google Sheets integration will be disabled.")

# Initialize Google Sheets client (lazy loading)
client = None
sheet = None

def get_google_sheet():
    """Lazy load Google Sheets connection"""
    global client, sheet
    if creds_dict is None:
        return None
    if client is None:
        try:
            print("🔗 Connecting to Google Sheets...")
            creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
            client = gspread.authorize(creds)
            sheet = client.open("Yavneh-Arts-RSVP").sheet1
            print("✅ Google Sheets connected successfully")
        except Exception as e:
            print(f"⚠️  Warning: Could not connect to Google Sheets: {e}")
            print("⚠️  RSVP submissions will not be saved to Google Sheets")
            return None
    return sheet

def create_db():
    conn = sqlite3.connect('rsvp.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS rsvps (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            guests INTEGER NOT NULL,
            comments TEXT
        )
    ''')
    conn.commit()
    conn.close()

create_db()

# Home route
@app.route('/')
def homepage():
    return render_template('homepage.html')

# About route
@app.route('/about')
def about():
    return render_template('about.html')

# Gallery routes
@app.route('/gallery')
def gallery():
    return render_template('gallery.html')

@app.route('/gallery/2024')
def gallery_2024():
    return render_template('gallery_2024.html')

@app.route('/gallery/2025')
def gallery_2025():
    return render_template('gallery_2025.html')

@app.route('/gallery/2026')
def gallery_2026():
    return render_template('gallery_2026.html')

# Register route
@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/submit-rsvp', methods=['POST'])
def submit_rsvp():
    firstName = request.form.get('firstName')
    lastName = request.form.get('lastName')
    email = request.form.get('email')

    if not firstName or not lastName or not email:
        return jsonify({"error": "All fields are required!"}), 400

    # Try to save to Google Sheets (if available)
    google_sheet = get_google_sheet()
    if google_sheet:
        try:
            google_sheet.append_row([firstName, lastName, email])
        except Exception as e:
            print(f"⚠️  Error saving to Google Sheets: {e}")
    
    return jsonify({"message": "Thank you! Your response has been submitted!"})

@app.route('/export-rsvp', methods=['GET'])
def export_rsvps():
    conn = sqlite3.connect('rsvp.db')
    df = pd.read_sql_query("SELECT * FROM rsvps", conn)
    df.to_csv('rsvp.csv', index=False)
    conn.close()
    return jsonify({"message": "RSVPs exported to rsvp.csv!"})

# Contact route
@app.route('/contact')
def contact():
    return render_template('contact.html')

# Chessed route
@app.route('/chessed')
def chessed():
    return render_template('chessed.html')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Render requires this
    print(f"🚀 Starting server on http://localhost:{port}")
    app.run(debug=True, host='0.0.0.0', port=port)
