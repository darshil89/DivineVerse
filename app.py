import streamlit as st
import requests
import json

API_URL = "http://localhost:8000/chat"

st.set_page_config(page_title="Know More About God", page_icon="🕉️", layout="centered")

# Custom CSS for chat-like UI with transparent background
st.markdown(
    """
    <style>
    body {background: linear-gradient(135deg, #f5e6ff 0%, #ffe6e6 100%);}
    .main {background: none !important; border-radius: 18px; padding: 2rem 2rem 6rem 2rem; box-shadow: none;}
    .chat-container {height: 400px; overflow-y: auto; border-radius: 10px; padding: 1rem; margin-bottom: 1rem; font-size: 1.1rem; display: flex; flex-direction: column; background: rgba(255,255,255,0.7);}
    .bubble-unified {align-self: flex-start; background: #f3e5f5; color: #4a148c; border-radius: 18px 18px 18px 18px; padding: 0.7em 1.2em; margin: 0.3em 0; max-width: 70%; word-break: break-word;}
    .input-row {position: fixed; bottom: 2.5rem; left: 50%; transform: translateX(-50%); width: 60vw; max-width: 500px; z-index: 100; display: flex; gap: 0.5em;}
    .stTextArea textarea {min-height: 2.5em !important; max-height: 5em;}
    .stButton {margin-left: 0.5em;}
    </style>
    <script>
    // Auto-scroll chat to bottom
    window.addEventListener('DOMContentLoaded', (event) => {
        var chat = document.getElementById('chat-scroll');
        if(chat){ chat.scrollTop = chat.scrollHeight; }
    });
    // Also scroll on update
    new MutationObserver(function(mutations) {
        var chat = document.getElementById('chat-scroll');
        if(chat){ chat.scrollTop = chat.scrollHeight; }
    }).observe(document.body, { childList: true, subtree: true });
    </script>
    """,
    unsafe_allow_html=True
)

st.markdown("<h1 style='text-align:center; font-size:2.8rem; color:#d2691e; font-family: 'Georgia', 'Segoe UI', serif;'>🔱 Know More About God 🔱</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; font-size:1.3rem; color:#333; font-family: 'Segoe UI', 'Georgia', serif;'>Enter a question below to learn more about Sanatan Dharma, its deities, mantras, and more.</p>", unsafe_allow_html=True)

# Conversation state
if 'messages' not in st.session_state:
    st.session_state['messages'] = []

# Chat history in a scrollable container

for msg in st.session_state['messages']:
    st.markdown(f"<div class='bubble-unified'><b>{'You' if msg['role']=='user' else 'AI'}:</b> {msg['content']}</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

def send_message():
    user_query = st.session_state["chat_input"]
    if user_query.strip():
        st.session_state['messages'].append({'role': 'user', 'content': user_query})
        try:
            with st.spinner("Searching the knowledge graph..."):
                response = requests.post(
                    API_URL,
                    json={"text": user_query},
                    timeout=30
                )
                if response.status_code == 200:
                    data = response.json()
                    answer = data.get("message", "No answer returned.")

                    # Only display the 'story' text if present, else fallback to answer as string
                    story = None
                    if isinstance(answer, str):
                        try:
                            answer_json = json.loads(answer)
                            if isinstance(answer_json, dict) and 'story' in answer_json:
                                story = answer_json['story']
                            else:
                                story = str(answer_json)
                        except Exception:
                            story = answer
                    elif isinstance(answer, dict) and 'story' in answer:
                        story = answer['story']
                    else:
                        story = str(answer)

                    st.session_state['messages'].append({'role': 'ai', 'content': story})
                else:
                    st.session_state['messages'].append({'role': 'ai', 'content': f"Error: {response.status_code} - {response.text}"})
        except Exception as e:
            st.session_state['messages'].append({'role': 'ai', 'content': f"Failed to connect to backend: {e}"})
        st.session_state["chat_input"] = ""  # Clear input

# Input row fixed at the bottom
with st.container():
    st.markdown("<div class='input-row'>", unsafe_allow_html=True)
    st.text_area(
        "Ask anything about Sanatan Dharma",
        key="chat_input",
        placeholder="Ask anything about Sanatan Dharma, deities, mantras, meanings, etc...",
        height=60,
        label_visibility="collapsed"
    )
    st.button("Send", key="send_button", on_click=send_message)
    st.markdown("</div>", unsafe_allow_html=True)