import streamlit as st
import openai

# -------------- CONFIGURATION -----------------
openai.api_key = "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"  # Replace with your API key

import streamlit as st
import openai

# ---------------- CONFIG ------------------
openai.api_key = "YOUR_OPENAI_API_KEY"  # Replace with your OpenAI API key

st.set_page_config(page_title="MedIntel 💊", page_icon="💊", layout="wide")

# ---------------- SIDEBAR ------------------
st.sidebar.title("MedIntel - AI Health Assistant")
st.sidebar.write("⚠️ **Disclaimer:** I am not a doctor. I provide general health information only.")

topic = st.sidebar.selectbox(
    "Choose Health Topic",
    ["General Health", "Diet & Nutrition", "Exercise & Fitness", "Symptoms & Conditions"]
)

if st.sidebar.button("Clear Chat"):
    st.session_state.messages = []

# ---------------- SESSION STATE ------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "user_input" not in st.session_state:
    st.session_state.user_input = ""

# ---------------- USER INPUT FORM ------------------
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input(f"Ask a question about {topic}:", value="", key="input")
    submit_button = st.form_submit_button(label="Send")

if submit_button and user_input.strip() != "":
    st.session_state.messages.append({"role": "user", "content": user_input})

    # ---------------- CHAT FUNCTION ------------------
    try:
        system_message = f"You are a helpful health assistant. Answer questions about {topic} politely and clearly."
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_input}
            ],
            max_tokens=250
        )
        bot_response = response['choices'][0]['message']['content']
    except Exception as e:
        bot_response = f"Error: {str(e)}"

    st.session_state.messages.append({"role": "bot", "content": bot_response})

# ---------------- SHOW CHAT HISTORY ------------------
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"**You:** {msg['content']}")
    else:
        st.markdown(f"**MedIntel:** {msg['content']}")
