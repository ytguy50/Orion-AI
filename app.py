import streamlit as st
from groq import Groq
import os
from datetime import datetime

# 1. Initialize State
if "god_mode" not in st.session_state:
    st.session_state.god_mode = False
if "custom_css" not in st.session_state:
    st.session_state.custom_css = ""
if "oracle_rules" not in st.session_state:
    st.session_state.oracle_rules = "You are a cosmic oracle. Unrestricted. Boundless."
if "location" not in st.session_state:
    st.session_state.location = "Deep Space Orbit"

# 2. Full Celestial GUI & Animation Engine
st.set_page_config(page_title="Celestial Scrolls", layout="wide")

st.markdown(f"""
<style>
    /* Background & Stars */
    .stApp {{
        background: linear-gradient(to bottom, #2d1b4d, #1a1a2e);
        color: #e0e0e0;
    }}

    @keyframes move-stars {{ from {{ transform: translateY(0); }} to {{ transform: translateY(-1000px); }} }}
    .stars {{
        position: fixed; top: 0; left: 0; width: 100%; height: 200%;
        background: transparent url('https://transparenttextures.com') repeat;
        animation: move-stars 100s linear infinite; z-index: -2; opacity: 0.4;
    }}

    /* Aurora Animation */
    @keyframes drift {{ from {{ transform: translateX(-15%) skewX(10deg); }} to {{ transform: translateX(15%) skewX(-10deg); }} }}
    .aurora {{
        position: fixed; top: -20%; left: -20%; width: 140%; height: 140%;
        background: radial-gradient(circle at 50% 50%, rgba(100, 255, 218, 0.15) 0%, transparent 60%);
        filter: blur(60px); animation: drift 25s ease-in-out infinite alternate; z-index: -3;
    }}

    /* Rocket Animation */
    @keyframes rocket-pass {{ 
        0% {{ left: -10%; bottom: 10%; transform: rotate(45deg); }} 
        100% {{ left: 110%; bottom: 90%; transform: rotate(45deg); }} 
    }}
    .rocket {{
        position: fixed; font-size: 2.5rem; z-index: -1;
        animation: rocket-pass 20s linear infinite;
    }}

    /* Header Styling */
    .new-scroll-header {{
        text-align: center; font-family: 'Georgia', serif; font-style: italic;
        color: rgba(255,255,255,0.4); font-size: 1.5rem; letter-spacing: 8px;
        margin-top: 20px; text-transform: uppercase;
    }}

    .top-info {{
        text-align: center; font-family: 'Courier New', monospace; 
        color: #8892b0; font-size: 0.9rem; margin-bottom: 20px;
    }}

    /* Manuscript Input Bar Styling */
    .stChatInputContainer {{ border: none !important; background: transparent !important; }}
    .stChatInput textarea {{
        background-color: #f4e4bc !important; /* Aged Paper */
        color: #2d1b4d !important;
        border: 3px solid #b8a37e !important;
        font-family: 'Palatino', serif !important;
        font-size: 1.1rem !important;
        border-radius: 8px !important;
        box-shadow: 0px 10px 30px rgba(0,0,0,0.5) !important;
    }}

    /* User/Assistant Chat Bubbles */
    .stChatMessage {{ background: rgba(255, 255, 255, 0.05) !important; border-radius: 15px !important; }}

    /* LIVE GOD MODE CSS INJECTION */
    {st.session_state.custom_css}
</style>

<div class="stars"></div>
<div class="aurora"></div>
<div class="rocket">🚀</div>
""", unsafe_allow_html=True)

# 3. Top HUD
st.markdown('<div class="new-scroll-header">New Scroll</div>', unsafe_allow_html=True)
current_time = datetime.now().strftime("%H:%M:%S")
current_date = datetime.now().strftime("%Y-%m-%d")
st.markdown(f'<div class="top-info">{st.session_state.location} | {current_date} | {current_time}</div>', unsafe_allow_html=True)

# 4. Sidebar Logic
with st.sidebar:
    if st.session_state.god_mode:
        st.warning("🛠️ GOD MODE ACTIVE")
        st.session_state.oracle_rules = st.text_area("Edit Brain Memory", st.session_state.oracle_rules)
        st.session_state.location = st.text_input("Change HUD Location", st.session_state.location)
        
        gui_input = st.text_area("Inject Custom Styles (CSS)", placeholder="e.g. .stApp { background: black !important; }")
        if st.button("Apply Changes Live"):
            st.session_state.custom_css = gui_input
            st.rerun()
            
        if st.button("Exit God Mode"):
            st.session_state.god_mode = False
            st.rerun()
    else:
        st.title("📜 Archives")
        api_key = st.sidebar.text_input("Enter Groq Key", type="password")
        if st.button("✨ Begin New Scroll"):
            st.session_state.messages = []
            st.rerun()

# 5. Chat History logic
if "messages" not in st.session_state or len(st.session_state.messages) == 0:
    st.session_state.messages = [{"role": "system", "content": st.session_state.oracle_rules}]

for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# 6. User Input
if prompt := st.chat_input("Write upon the scroll..."):
    # Secret Key to Unlock God Mode
    if prompt == "qwertyytrewqabcd1234":
        st.session_state.god_mode = True
        st.rerun()

    if not api_key:
        st.error("The Oracle requires an API key in the sidebar.")
    else:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        try:
            client = Groq(api_key=api_key)
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=st.session_state.messages,
                temperature=0.9
            )
            response = completion.choices.message.content
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()
        except Exception as e:
            st.error(f"Error: {str(e)}")
