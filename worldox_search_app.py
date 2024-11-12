import os
import requests
import streamlit as st
from datetime import datetime

# Streamlit UI
st.title("Worldox Boolean Search Generator")
user_input = st.text_input("Enter your search query in natural language:", "I need all liens from Northwestern Hospital this year.")
submit_button = st.button("Generate Boolean Search Query")

def generate_boolean_query(modified_input):
    # Define the API endpoint and retrieve the API key securely
    url = "https://api.openai.com/v1/chat/completions"
    api_key = ("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")
    if not api_key:
        return "API key is missing. Please set it in your environment variables."

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Define the payload with model and prompt information
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "user", "content": f"Convert the following natural language query into a Boolean search query following Worldox standards: {modified_input}"}
        ],
        "max_tokens": 100
    }
    
    try:
        # Make the request to OpenAI API
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  # Check if the request was successful
        data = response.json()
        
        # Extract and return the text response
        return data['choices'][0]['message']['content'].strip()
    except requests.exceptions.HTTPError as http_err:
        return f"HTTP error occurred: {http_err}"
    except Exception as e:
        return f"An error occurred: {e}"

if submit_button:
    st.write("Checkpoint: Starting OpenAI API request")

    # Replace "this year" and "last year" with actual years in the input text
    current_year = datetime.now().year
    last_year = current_year - 1
    modified_input = user_input.replace("this year", str(current_year)).replace("last year", str(last_year))

    # Generate a Boolean query based on modified input
    boolean_query = generate_boolean_query(modified_input)

    # Display the result
    st.write("Generated Boolean Query:")
    st.write(boolean_query)
