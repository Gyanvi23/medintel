import streamlit as st
import os
from openai import OpenAI

# Page title
st.title("🩺 MedIntel")

# Disclaimer
st.markdown("⚠️ This chatbot is for **general health information only**. Not a substitute for a doctor.")

# Load API key
api_key = os.getenv("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")
if not api_key:
    st.error("🚨 OPENAI_API_KEY is missing! Please add it in Streamlit Secrets.")
else:
    client = OpenAI(api_key=api_key)

    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {"role": "system", "content": "You are a helpful health assistant. Always include a doctor disclaimer."}
        ]

    # Chat input
    if prompt := st.chat_input("Ask me a health question..."):
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            try:
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=st.session_state.messages
                )
                reply = response.choices[0].message.content
                st.markdown(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})
            except Exception as e:
                st.error(f"Error: {e}")


