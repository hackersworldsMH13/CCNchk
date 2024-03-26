from flask import Flask, render_template, request
import requests
import subprocess
 
from userinfo import RandUser  # Assuming this is a custom module you have

# Disable SSL warnings
import urllib3
urllib3.disable_warnings()


app = Flask(__name__)

# Define a function to start Streamlit as a subprocess
def start_streamlit():
    subprocess.Popen(['streamlit', 'run', 'streamlit_app.py'])

# Route for the homepage
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle form submission and communicate with Streamlit
@app.route('/submit', methods=['POST'])
def submit():
    # Extract credit card information from the form
    cc, mm, yy, cvv = request.form['credit_info'].split('|')
    
    # Make a request to Streamlit API
    response = requests.post('http://localhost:8501/process_payment', json={'cc': cc, 'mm': mm, 'yy': yy, 'cvv': cvv})
    
    # Get the result from Streamlit
    result = response.json()['result']
    
    # Pass the result to the template
    return render_template('index.html', result=result)

if __name__ == '__main__':
    # Start Streamlit as a subprocess when the Flask app is run
    start_streamlit()
    
    # Run the Flask app
    app.run(debug=True)
