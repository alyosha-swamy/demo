import streamlit as st
import requests
import json

# Show title and description
st.title("💬 Tensoic Chatbot")
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("API_KEY")# API endpoint
url = "https://tensoic-api.pipeshift.ai/v1/completions"

# Request headers
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

# Create a session state variable to store the chat messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display the existing chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Create a chat input field
if prompt := st.chat_input("What is up?"):
    # Store and display the current prompt
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Prepare the request payload
    data = {
        "model": "Tensoic/Kan-Llama-7B-SFT-v0.5",
        "prompt": prompt,
        "max_tokens": 150,
        "temperature": 0.7,
        "top_p": 1,
        "frequency_penalty": 0,
        "presence_penalty": 0,
        "stop": ["\n", " Human:", " AI:"]
    }

    # Make the API call
    response = requests.post(url, headers=headers, json=data)

    # Check if the request was successful
    if response.status_code == 200:
        response_data = response.json()
        if 'choices' in response_data and len(response_data['choices']) > 0:
            assistant_response = response_data['choices'][0]['text'].strip()

            # Display and store the assistant's response
            with st.chat_message("assistant"):
                st.markdown(assistant_response)
            st.session_state.messages.append({"role": "assistant", "content": assistant_response})
        else:
            st.error("Unexpected response format from the API")
    else:
        st.error(f"Request failed with status code: {response.status_code}")
        st.error(f"Error message: {response.text}")
