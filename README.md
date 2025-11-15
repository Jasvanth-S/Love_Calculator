# 💕 Love Calculator App

A beautiful and interactive love calculator web application built with Flask, HTML, CSS, JavaScript, and MongoDB.

## Features

- **User-friendly Interface**: Clean and modern design with responsive layout
- **Love Calculation**: Calculate love compatibility based on names and dates of birth
- **Database Storage**: All submissions are stored in MongoDB for admin viewing
- **Admin Dashboard**: View all form submissions with detailed information
- **WhatsApp Sharing**: Share results directly to WhatsApp
- **Mobile Responsive**: Works perfectly on all devices

## Setup Instructions

### Prerequisites
- Python 3.7+
- MongoDB installed and running on localhost:27017

### Installation

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start MongoDB:**
   Make sure MongoDB is running on your system. If you have MongoDB installed:
   ```bash
   mongod
   ```

3. **Run the application:**
   ```bash
   python app.py
   ```

4. **Access the application:**
   - Main app: http://localhost:5000
   - Admin dashboard: http://localhost:5000/admin

## Project Structure

```
Love_Calculator/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── templates/
│   ├── index.html        # Main love calculator page
│   └── admin.html        # Admin dashboard
└── static/
    ├── style.css         # Main page styling
    ├── admin.css         # Admin page styling
    └── script.js         # JavaScript functionality
```

## How It Works

1. **User Input**: Users enter two names and dates of birth
2. **Calculation**: The app uses a hash-based algorithm to generate a consistent percentage
3. **Storage**: All submissions are stored in MongoDB with timestamps
4. **Results**: Users see their love percentage with a fun message
5. **Sharing**: Results can be shared directly to WhatsApp
6. **Admin View**: Admin can view all submissions at /admin endpoint

## API Endpoints

- `GET /` - Main love calculator page
- `POST /calculate` - Calculate love percentage
- `GET /admin` - Admin dashboard
- `GET /share/<name1>/<name2>/<percentage>` - WhatsApp sharing

## Database Schema

The MongoDB collection `submissions` stores:
- `name1`: First person's name
- `name2`: Second person's name  
- `dob1`: First person's date of birth
- `dob2`: Second person's date of birth
- `percentage`: Calculated love percentage
- `timestamp`: When the calculation was made

## Customization

You can customize the love messages by editing the `loveMessages` object in `static/script.js`.

## Security Notes

- Input validation is implemented on both frontend and backend
- Dates cannot be in the future
- All user inputs are sanitized before database storage

Enjoy calculating love! 💕
