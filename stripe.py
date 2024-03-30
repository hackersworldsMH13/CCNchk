import streamlit as st
import itertools
import re
import requests
import random
import string
import uuid
import time

# Function to generate a random email, password, and username
def generate_password(length=8):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))

    domains = ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com']
    username = ''.join(random.choice(string.ascii_lowercase) for _ in range(6))
    domain = random.choice(domains)
    email = f"{username}@{domain}"

    return email, password, username

# Function to find substring between two substrings
def find_between(s, start, end):
    try:
        """Return substring between two substrings."""
        start_index = s.find(start)
        if start_index == -1:
            return None
        start_index += len(start)
        end_index = s.find(end, start_index)
        if end_index == -1:
            return None
        return s[start_index:end_index].replace('\\"', '"')
    except ValueError:
        return

# Function to obtain the brand of a credit card
def bin(cc):
    response = requests.get(f'https://bins.antipublic.cc/bins/{cc[:6]}')
    brand_mapping = {
        "VISA": "visa",
        "MASTERCARD": "mc",
        "AMERICAN EXPRESS": "amex",
        "DINERS CLUB": "diners",
        "DISCOVER": "discover"
    }
    
    response_data = response.json()
    brand = brand_mapping.get(response_data.get("brand", ""))
    
    return brand

# Main function to simulate the credit card payment process
def main(cc, mm, yy, cvv, brand):
    # Place your main function code here

    # Example placeholder
    result = f'{cc}|{mm}|{yy}|{cvv} -> Placeholder result'
    
    return result

# Streamlit app UI
def main():
    st.title("Credit Card Payment Simulator")
    cc = st.text_input("Enter Credit Card Number")
    mm = st.text_input("Enter Expiry Month")
    yy = st.text_input("Enter Expiry Year")
    cvv = st.text_input("Enter CVV")
    submit_button = st.button("Submit")

    if submit_button:
        if cc and mm and yy and cvv:
            # Generate random brand for demo
            brand = bin(cc)
            # Call main function
            result = main(cc, mm, yy, cvv, brand)
            st.write(result)
        else:
            st.error("Please fill in all the fields.")

if __name__ == "__main__":
    main()
