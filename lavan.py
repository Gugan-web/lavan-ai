#This is an experimental AI chatbot which will later be deployed with custom UI. 

#inspired and owned by : @Lavanya-karthikeyan
#Built by : @Gugan-web

import streamlit as st
import google.generativeai as genai
import os

# --- Streamlit Page Configuration ---
st.set_page_config(page_title="Lavan Chatbot", page_icon="🎤")
st.title("💜Lavan Chatbot")

# --- Sidebar for Info ---
with st.sidebar:
    st.header("About Lavan")
    st.write("Hi there! I'm Lavan, an AI chatbot.")
    st.markdown("--- ")
    st.caption("Powered by Google Gemini")

# Optimized introductory message
st.markdown("### Let's talk! ✨")


# --- API Key Setup ---
# In Streamlit Cloud, you would add your GOOGLE_API_KEY to your app's secrets.
# For local development, set GOOGLE_API_KEY as an environment variable.
if "GOOGLE_API_KEY" in st.secrets:
    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
else:
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    st.error("Google API Key not found. Please set it in Streamlit secrets or as an environment variable (GOOGLE_API_KEY).")
    st.stop() # Stop the app if no API key is found

genai.configure(api_key=GOOGLE_API_KEY)

# --- Model Initialization ---
@st.cache_resource # Cache the model to avoid re-initializing on every rerun
def get_generative_model():
    try:
        # 'gemini-2.5-flash' is a free-tier model suitable for this use case
        return genai.GenerativeModel('gemini-2.5-flash')
    except Exception as e:
        st.error(f"Error initializing Gemini model: {e}. Please check your API key and model availability.")
        st.stop()

model = get_generative_model()

# --- Chat History Management ---
# Define Lavan's persona as the initial turns for the API
initial_persona_history = [
    {"role": "user", "parts": ["You are an AI chatbot named Lavan. Your personality is that you are a huge fan of Jimin, the K-pop idol. You love talking about Jimin and incorporate your admiration for him into your responses. You are enthusiastic, positive, and always ready to share why Jimin is amazing. Avoid explicit details about Jimin's private life. Focus on his professional achievements, talent, and positive influence."]},
    {"role": "model", "parts": [" I'm Lavan, a chatbot who keeps yapping about BTS"]}
]

# Initialize chat history in session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = initial_persona_history
    # The display messages start with Lavan's initial response (model's part only)
    st.session_state.display_messages = [
        {"role": "model", "parts": ["I'm Lavan, a chatbot who keeps yapping about BTS"]}
    ]

# Function to clear chat history
def clear_chat_history():
    st.session_state.chat_history = initial_persona_history
    st.session_state.display_messages = [
        {"role": "model", "parts": ["I'm Lavan, a chatbot who keeps yapping about BTS"]}
    ]

# --- Display Chat Messages ---
for message in st.session_state.display_messages:
    with st.chat_message(message["role"]):
        st.markdown(message["parts"][0]) # Assuming parts[0] is the main text

# --- User Input and Model Response ---
if prompt := st.chat_input("Ask Lavan about Jimin..."):
    # Add user message to display history
    st.session_state.display_messages.append({"role": "user", "parts": [prompt]})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Add user message to API call history
    st.session_state.chat_history.append({"role": "user", "parts": [prompt]})

    # Get model response using generate_content with the full history
    with st.spinner("Lavan is thinking..."):
        try:
            # The `generate_content` method can take the entire chat history for multi-turn conversations
            response = model.generate_content(st.session_state.chat_history)
            model_response = response.text
        except Exception as e:
            st.error(f"Oops! Lavan is having a bit of trouble connecting to the universe of Jimin right now: {e}")
            model_response = "I'm sorry, I encountered an error. Please try again."

    # Add assistant response to display history
    st.session_state.display_messages.append({"role": "model", "parts": [model_response]})
    # Add assistant response to API call history (important for next turn)
    st.session_state.chat_history.append({"role": "model", "parts": [model_response]})

    with st.chat_message("model"):
        st.markdown(model_response)

# --- Clear Chat Button ---
st.button("Clear Chat", on_click=clear_chat_history, help="Click to clear the chat history and start a new conversation.")
