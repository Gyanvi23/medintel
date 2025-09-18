import streamlit as st
import openai

# -------------- CONFIGURATION -----------------
openai.api_key = "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"  # Replace with your API key

# -------------- APP LAYOUT -----------------
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

# ---------------- USER INPUT ------------------
def get_user_input():
    return st.text_input(f"Ask a question about {topic}:", key="input")

user_input = get_user_input()

# ---------------- CHAT FUNCTION ------------------
def generate_response(prompt, topic):
    system_message = f"You are a helpful health assistant. Answer questions about {topic} politely and clearly."
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Use gpt-4 if available
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt}
        ],
        max_tokens=250
    )
    return response['choices'][0]['message']['content']

# ---------------- DISPLAY CHAT ------------------
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    bot_response = generate_response(user_input, topic)
    st.session_state.messages.append({"role": "bot", "content": bot_response})

# ---------------- SHOW CHAT HISTORY ------------------
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"**You:** {msg['content']}")
    else:
        st.markdown(f"**MedIntel:** {msg['content']}")

# ---------------- OPTIONAL MUSIC ------------------
st.sidebar.write("🎵 Background Music (Optional)")
music = st.sidebar.selectbox("Choose music", ["None", "Calm", "Energetic"])
if music != "None":
    st.audio(f"medintel_music/{music}.mp3", format="audio/mp3", start_time=0)
