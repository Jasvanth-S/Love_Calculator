from flask import Flask, render_template, request, jsonify, redirect, url_for
from pymongo import MongoClient
from datetime import datetime
import hashlib
import os
from urllib.parse import quote

app = Flask(__name__)

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['love_calculator']
submissions = db['submissions']

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
        
        submissions.insert_one(submission_data)
        
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
    all_submissions = list(submissions.find().sort('timestamp', -1))
    
    # Convert ObjectId to string for JSON serialization
    for submission in all_submissions:
        submission['_id'] = str(submission['_id'])
        submission['timestamp'] = submission['timestamp'].strftime('%Y-%m-%d %H:%M:%S')
    
    return render_template('admin.html', submissions=all_submissions)

@app.route('/share/<name1>/<name2>/<percentage>')
def share(name1, name2, percentage):
    """Generate WhatsApp share URL"""
    message = f"💕 Love Calculator Result 💕\n{name1} ❤️ {name2}\nLove Percentage: {percentage}%\n\nTry it yourself: {request.host_url}"
    whatsapp_url = f"https://wa.me/?text={quote(message)}"
    return redirect(whatsapp_url)

if __name__ == '__main__':
    app.run(debug=True)
