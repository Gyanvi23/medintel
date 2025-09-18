
import streamlit as st
import openai

# ---------------- CONFIG ------------------
client = openai.OpenAI(api_key=st.secrets["openai"]["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"])

st.set_page_config(page_title="MedIntel 💊", page_icon="💊", layout="wide")
st.markdown("<h1 style='text-align:center;'>💊 MedIntel - Your Intelligent Health Assistant</h1>", unsafe_allow_html=True)

# ---------------- SIDEBAR ------------------
st.sidebar.title("MedIntel - AI Health Assistant")
st.sidebar.write("⚠️ Disclaimer: I am not a doctor. Advice is for informational purposes only.")
if st.sidebar.button("Clear Chat"):
    st.session_state.messages = []

# ---------------- SESSION STATE ------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------- USER INPUT FORM ------------------
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("Type your message here...", "")
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
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": system_message}] + st.session_state.messages,
            max_tokens=350,
            temperature=0.7
        )
        bot_response = response.choices[0].message.content
    except Exception as e:
        bot_response = f"Error: {str(e)}"

    st.session_state.messages.append({"role": "bot", "content": bot_response})

# ---------------- CHAT WINDOW STYLE ------------------
chat_style = """
<style>
.chat-container {
    max-height: 500px;
    overflow-y: auto;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 15px;
    background-color: #f9f9f9;
}
.user-bubble {
    background-color: #DCF8C6;
    padding: 10px 15px;
    border-radius: 15px 15px 0 15px;
    max-width: 70%;
    margin-left: auto;
    margin-bottom: 10px;
}
.bot-bubble {
    background-color: #F1F0F0;
    padding: 10px 15px;
    border-radius: 15px 15px 15px 0;
    max-width: 70%;
    margin-right: auto;
    margin-bottom: 10px;
}
.avatar {
    width: 35px;
    height: 35px;
    border-radius: 50%;
    display: inline-block;
    vertical-align: top;
    margin-right: 10px;
}
</style>
"""

st.markdown(chat_style, unsafe_allow_html=True)

st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(
            f"""
            <div style='display:flex; justify-content:flex-end; align-items:flex-start;'>
                <div class='user-bubble'>
                    <strong>You:</strong><br>{msg["content"]}
                </div>
                <img class='avatar' src='https://i.imgur.com/7k12EPD.png'>
            </div>
            """, unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"""
            <div style='display:flex; justify-content:flex-start; align-items:flex-start;'>
                <img class='avatar' src='https://i.imgur.com/6YVq5M3.png'>
                <div class='bot-bubble'>
                    <strong>MedIntel:</strong><br>{msg["content"]}
                </div>
            </div>
            """, unsafe_allow_html=True
        )
st.markdown("</div>", unsafe_allow_html=True)


