import streamlit as st
import openai
import sqlite3
import time
import uuid

# ---------------- CONFIG ------------------
st.set_page_config(page_title="MedIntel 💊", page_icon="💊", layout="centered")

# OpenAI API key from Streamlit secrets
client = openai.OpenAI(api_key=st.secrets["openai"]["api_key"])

# ---------------- USER SESSION ------------------
if "user_id" not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())  # unique id for each user session
if "current_topic" not in st.session_state:
    st.session_state.current_topic = None
if "step" not in st.session_state:
    st.session_state.step = 0

# ---------------- DATABASE ------------------
conn = sqlite3.connect("medintel_chat.db", check_same_thread=False)
c = conn.cursor()
c.execute("""
CREATE TABLE IF NOT EXISTS chat_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT,
    role TEXT,
    message TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")
conn.commit()

# ---------------- SIDEBAR ------------------
st.sidebar.title("MedIntel - AI Health Assistant")
st.sidebar.write("⚠️ Disclaimer: I am not a real doctor. Advice is for informational purposes only.")
if st.sidebar.button("Clear Chat"):
    st.session_state.step = 0
    st.session_state.current_topic = None
    c.execute("DELETE FROM chat_history WHERE user_id = ?", (st.session_state.user_id,))
    conn.commit()

# ---------------- TOPIC BUTTONS ------------------
topic = st.sidebar.radio(
    "Choose a topic to start:",
    ("Symptoms", "Diet & Nutrition", "Fitness & Exercise")
)
st.session_state.current_topic = topic

# ---------------- LOAD PREVIOUS MESSAGES ------------------
st.session_state.messages = []
c.execute("SELECT role, message FROM chat_history WHERE user_id=? ORDER BY id ASC", (st.session_state.user_id,))
rows = c.fetchall()
for row in rows:
    st.session_state.messages.append({"role": row[0], "content": row[1]})

# ---------------- CSS FOR MOBILE-LIKE CHAT ------------------
st.markdown("""
<style>
.chat-container {
    max-width: 450px;
    margin: auto;
    max-height: 550px;
    overflow-y: auto;
    padding: 15px;
    border: 1px solid #ddd;
    border-radius: 20px;
    background-color: #f9f9f9;
}
.user-bubble {
    background-color: #DCF8C6;
    padding: 12px 18px;
    border-radius: 18px 18px 0 18px;
    max-width: 75%;
    margin-left: auto;
    margin-bottom: 10px;
    word-wrap: break-word;
}
.bot-bubble {
    background-color: #F1F0F0;
    padding: 12px 18px;
    border-radius: 18px 18px 18px 0;
    max-width: 75%;
    margin-right: auto;
    margin-bottom: 10px;
    word-wrap: break-word;
}
.avatar {
    width: 35px;
    height: 35px;
    border-radius: 50%;
    display: inline-block;
    vertical-align: top;
    margin: 0 10px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- CHAT CONTAINER ------------------
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

# ---------------- USER INPUT ------------------
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("Type your message here...", "")
    submit_button = st.form_submit_button("Send")

# ---------------- STEP-BY-STEP AI RESPONSE ------------------
system_message = f"""
You are MedIntel, a professional AI virtual doctor.
- Be empathetic, professional, and clear.
- If topic is 'Symptoms', ask for step-by-step symptom details.
- Once symptoms are provided, suggest possible diseases and general medicines.
- If topic is 'Diet & Nutrition' or 'Fitness & Exercise', provide informative advice.
- Always include disclaimer: '⚠️ I am not a real doctor; consult a healthcare professional.'
"""

if submit_button and user_input.strip() != "":
    # Show typing animation
    placeholder = st.empty()
    with placeholder.container():
        st.markdown("**MedIntel is typing...**")
        time.sleep(1)  # simulate typing

    # Save user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    c.execute("INSERT INTO chat_history (user_id, role, message) VALUES (?, ?, ?)",
              (st.session_state.user_id, "user", user_input))
    conn.commit()

    # Call OpenAI API
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": system_message}] + st.session_state.messages,
            max_tokens=450,
            temperature=0.7
        )
        bot_response = response.choices[0].message.content
    except Exception as e:
        bot_response = f"Error: {str(e)}"

    # Save bot response
    st.session_state.messages.append({"role": "bot", "content": bot_response})
    c.execute("INSERT INTO chat_history (user_id, role, message) VALUES (?, ?, ?)",
              (st.session_state.user_id, "bot", bot_response))
    conn.commit()

    # Clear typing animation
    placeholder.empty()

    # Rerun to display updated chat
    st.experimental_rerun()


