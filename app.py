import streamlit as st
import openai
import sqlite3

# ---------------- CONFIG ------------------
# Initialize OpenAI client
client = openai.OpenAI(api_key="YOUR_OPENAI_API_KEY")  # Replace with your API key

st.set_page_config(page_title="MedIntel 💊", page_icon="💊", layout="wide")

# ---------------- DATABASE ------------------
conn = sqlite3.connect("medintel_chat.db", check_same_thread=False)
c = conn.cursor()
c.execute("""
CREATE TABLE IF NOT EXISTS chat_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    role TEXT,
    message TEXT
)
""")
conn.commit()

# ---------------- SESSION STATE ------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# Load messages from database
c.execute("SELECT role, message FROM chat_history ORDER BY id ASC")
rows = c.fetchall()
for row in rows:
    st.session_state.messages.append({"role": row[0], "content": row[1]})

# ---------------- SIDEBAR ------------------
st.sidebar.title("MedIntel - AI Health Assistant")
st.sidebar.write("⚠️ Disclaimer: I am not a doctor. Advice is for informational purposes only.")
if st.sidebar.button("Clear Chat"):
    st.session_state.messages = []
    c.execute("DELETE FROM chat_history")
    conn.commit()

# ---------------- USER INPUT FORM ------------------
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("Ask any health-related question:", "")
    submit_button = st.form_submit_button("Send")

# ---------------- SYSTEM MESSAGE ------------------
system_message = """
You are MedIntel, a highly intelligent, polite, and professional AI healthcare assistant.
Answer all questions accurately, clearly, and provide useful guidance.
Always give disclaimers where necessary: You are not a doctor and your advice is for informational purposes only.
"""

# ---------------- GENERATE RESPONSE ------------------
if submit_button and user_input.strip() != "":
    # Save user message to session and DB
    st.session_state.messages.append({"role": "user", "content": user_input})
    c.execute("INSERT INTO chat_history (role, message) VALUES (?, ?)", ("user", user_input))
    conn.commit()

    try:
        # OpenAI API call
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": system_message}] + st.session_state.messages,
            max_tokens=400,
            temperature=0.7
        )
        bot_response = response.choices[0].message.content

    except Exception as e:
        bot_response = f"Error: {str(e)}"

    # Save bot response to session and DB
    st.session_state.messages.append({"role": "bot", "content": bot_response})
    c.execute("INSERT INTO chat_history (role, message) VALUES (?, ?)", ("bot", bot_response))
    conn.commit()

# ---------------- CSS & HTML MOBILE-LIKE DESIGN ------------------
chat_style = """
<style>
.chat-container {
    max-height: 550px;
    overflow-y: auto;
    padding: 15px;
    border: 1px solid #ddd;
    border-radius: 20px;
    background-color: #f9f9f9;
    margin-bottom: 10px;
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
body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}
</style>
"""
st.markdown(chat_style, unsafe_allow_html=True)

# ---------------- DISPLAY CHAT ------------------
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
