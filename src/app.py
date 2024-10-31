from flask import Flask, request, jsonify, send_from_directory
import os
from onboarding_and_emails import onboarding

app = Flask(__name__, static_folder='static')

@app.route('/')
def home():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/sign-in')
def sign_in():
    return send_from_directory(app.static_folder, 'sign-in.html')

@app.route('/api/onboard', methods=['POST'])
def handle_onboard():
    try:
        data = request.get_json()
        email = data.get('email')
        
        if not email:
            return jsonify({'error': 'Email is required'}), 400

        # Call your existing onboarding function
        onboarding(email)
        
        return jsonify({'message': 'Registration successful'}), 201
    
    except Exception as e:
        print(f"Error during onboarding: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)