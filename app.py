import streamlit as st
import openai

# -------------- CONFIGURATION -----------------
openai.api_key = "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"  # Replace with your API key



st.set_page_config(page_title="MedIntel 💊", page_icon="💊", layout="wide")

# ---------------- SIDEBAR ------------------
st.sidebar.title("MedIntel - AI Health Assistant")
st.sidebar.write("⚠️ **Disclaimer:** I am not a doctor. Advice is for informational purposes only.")
if st.sidebar.button("Clear Chat"):
    st.session_state.messages = []

# ---------------- SESSION STATE ------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------- USER INPUT FORM ------------------
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("Ask any health-related question:", "")
    submit_button = st.form_submit_button("Send")

# ---------------- GENERATE RESPONSE ------------------
if submit_button and user_input.strip() != "":
    st.session_state.messages.append({"role": "user", "content": user_input})

    system_message = """
    You are MedIntel, a highly intelligent, polite, and professional AI healthcare assistant.
    Answer all questions accurately, clearly, and provide useful guidance.
    Always give disclaimers where necessary: You are not a doctor and your advice is for informational purposes only.
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": system_message}] + st.session_state.messages,
            max_tokens=350,
            temperature=0.7
        )
        bot_response = response['choices'][0]['message']['content']
    except Exception as e:
        bot_response = f"Error: {str(e)}"

    st.session_state.messages.append({"role": "bot", "content": bot_response})

# ---------------- DISPLAY CHAT WITH BUBBLES ------------------
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(
            f"""
            <div style='display:flex; justify-content:flex-end; margin-bottom:10px;'>
                <div style='background-color:#DCF8C6; padding:10px 15px; border-radius:15px; max-width:70%;'>
                    <strong>You:</strong><br>{msg["content"]}
                </div>
            </div>
            """, unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"""
            <div style='display:flex; justify-content:flex-start; margin-bottom:10px;'>
                <div style='background-color:#F1F0F0; padding:10px 15px; border-radius:15px; max-width:70%;'>
                    <strong>MedIntel:</strong><br>{msg["content"]}
                </div>
            </div>
            """, unsafe_allow_html=True
        )
