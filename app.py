import streamlit as st
import openai

# -------------- CONFIGURATION -----------------
openai.api_key = "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"  # Replace with your API key

# -------------- APP LAYOUT -----------------
st.set_page_config(page_title="MedIntel - AI for a Healthier Tomorrow", page_icon="💊")
st.title("💊 MedIntel - AI for a Healthier Tomorrow")
st.write("⚠️ **Disclaimer:** I am not a doctor. This chatbot provides general health information only.")

# -------------- SESSION STATE -----------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -------------- USER INPUT -----------------
def get_user_input():
    return st.text_input("Ask your health question here:")

user_input = get_user_input()

# -------------- CHAT FUNCTION -----------------
def generate_response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # You can use gpt-4 if available
        messages=[{"role": "system", "content": "You are a helpful health assistant."},
                  {"role": "user", "content": prompt}],
        max_tokens=200
    )
    return response['choices'][0]['message']['content']

# -------------- DISPLAY CHAT -----------------
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    bot_response = generate_response(user_input)
    st.session_state.messages.append({"role": "bot", "content": bot_response})

# -------------- SHOW CHAT HISTORY -----------------
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"**You:** {msg['content']}")
    else:
        st.markdown(f"**MedIntel:** {msg['content']}")
