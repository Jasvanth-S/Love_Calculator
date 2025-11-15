from flask import Flask, render_template, request, jsonify, redirect, url_for
from pymongo import MongoClient
from datetime import datetime
import hashlib
import os
from urllib.parse import quote

app = Flask(__name__)

# Configure Flask for ngrok
app.config['SERVER_NAME'] = None  # Allow any host
app.config['APPLICATION_ROOT'] = '/'

# Global variable to store ngrok URL
NGROK_URL = None

# MongoDB connection - fallback to in-memory for ngrok demo
MONGODB_URI = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/')
try:
    client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=3000)
    db = client['love_calculator']
    submissions = db['submissions']
    # Test connection
    client.admin.command('ping')
    print("MongoDB connected successfully!")
except Exception as e:
    print(f"MongoDB connection failed: {e}")
    print("Using in-memory storage for ngrok demo")
    # Fallback to in-memory storage for ngrok demo
    submissions = []

def calculate_love_percentage(name1, name2, dob1, dob2):
    """Calculate love percentage based on names and dates of birth"""
    # Combine names and dates for calculation
    combined_string = f"{name1.lower()}{name2.lower()}{dob1}{dob2}"
    
    # Create a hash and convert to percentage
    hash_object = hashlib.md5(combined_string.encode())
    hash_hex = hash_object.hexdigest()
    
    # Convert first 8 characters of hash to integer and get percentage
    percentage = int(hash_hex[:8], 16) % 101  # 0-100
    
    return percentage

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        data = request.get_json()
        
        name1 = data.get('name1', '').strip()
        name2 = data.get('name2', '').strip()
        dob1 = data.get('dob1', '')
        dob2 = data.get('dob2', '')
        
        if not all([name1, name2, dob1, dob2]):
            return jsonify({'error': 'All fields are required'}), 400
        
        # Calculate love percentage
        percentage = calculate_love_percentage(name1, name2, dob1, dob2)
        
        # Store in database
        submission_data = {
            'name1': name1,
            'name2': name2,
            'dob1': dob1,
            'dob2': dob2,
            'percentage': percentage,
            'timestamp': datetime.now()
        }
        
        try:
            if isinstance(submissions, list):
                # Fallback storage
                submission_data['_id'] = str(len(submissions) + 1)
                submission_data['timestamp'] = submission_data['timestamp'].strftime('%Y-%m-%d %H:%M:%S')
                submissions.append(submission_data)
            else:
                # MongoDB storage
                submissions.insert_one(submission_data)
        except Exception as e:
            print(f"Database storage failed: {e}")
        
        return jsonify({
            'percentage': percentage,
            'name1': name1,
            'name2': name2
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/admin')
def admin():
    """Admin view to see all submissions"""
    try:
        if isinstance(submissions, list):
            # Fallback storage
            all_submissions = sorted(submissions, key=lambda x: x['timestamp'], reverse=True)
        else:
            # MongoDB storage
            all_submissions = list(submissions.find().sort('timestamp', -1))
            # Convert ObjectId to string for JSON serialization
            for submission in all_submissions:
                submission['_id'] = str(submission['_id'])
                submission['timestamp'] = submission['timestamp'].strftime('%Y-%m-%d %H:%M:%S')
    except Exception as e:
        print(f"Error fetching submissions: {e}")
        all_submissions = []
    
    return render_template('admin.html', submissions=all_submissions)

@app.route('/share/<name1>/<name2>/<percentage>')
def share(name1, name2, percentage):
    """Generate WhatsApp share URL"""
    # Use ngrok URL if available, otherwise use request host
    base_url = NGROK_URL if NGROK_URL else request.host_url
    message = f"💕 Love Calculator Result 💕\n{name1} ❤️ {name2}\nLove Percentage: {percentage}%\n\nTry it yourself: {base_url}"
    whatsapp_url = f"https://wa.me/?text={quote(message)}"
    return redirect(whatsapp_url)

@app.route('/set-ngrok-url', methods=['POST'])
def set_ngrok_url():
    """Set the ngrok URL for sharing"""
    global NGROK_URL
    data = request.get_json()
    NGROK_URL = data.get('url')
    return jsonify({'status': 'success', 'url': NGROK_URL})

if __name__ == '__main__':
    print("🚀 Starting Love Calculator for ngrok sharing...")
    print("📱 After starting ngrok, your app will be accessible worldwide!")
    print("🔗 Don't forget to run: ngrok http 5000")
    app.run(debug=False, host='0.0.0.0', port=5000)
