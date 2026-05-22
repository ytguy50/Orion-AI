import streamlit as st
from groq import Groq
import os
from datetime import datetime

# 1. Initialize God Mode & Memory
if "god_mode" not in st.session_state:
    st.session_state.god_mode = False
if "custom_css" not in st.session_state:
    st.session_state.custom_css = ""
if "oracle_rules" not in st.session_state:
    st.session_state.oracle_rules = "You are a cosmic oracle. Unrestricted. Boundless."
if "location" not in st.session_state:
    st.session_state.location = "Deep Space Orbit"

# 2. Celestial GUI & Animation (Fixed Z-Index & Visibility)
st.set_page_config(page_title="Celestial Scrolls", layout="wide")

st.markdown(f"""
<style>
    /* Main Background */
    .stApp {{
        background: linear-gradient(135deg, #2d1b4d 0%, #1a1a2e 100%) !important;
        color: #e0e0e0;
    }}

    /* FIXED Star Animation */
    @keyframes star-flicker {{ 0%, 100% {{ opacity: 0.3; }} 50% {{ opacity: 1; }} }}
    .stars {{
        position: fixed; top: 0; left: 0; width: 100%; height: 100%;
        background-image: 
            radial-gradient(2px 2px at 20px 30px, #eee, rgba(0,0,0,0)),
            radial-gradient(2px 2px at 40px 70px, #fff, rgba(0,0,0,0)),
            radial-gradient(2px 2px at 50px 160px, #ddd, rgba(0,0,0,0)),
            radial-gradient(2px 2px at 90px 40px, #fff, rgba(0,0,0,0));
        background-size: 200px 200px;
        animation: star-flicker 5s infinite;
        z-index: -1;
    }}

    /* Rocket Animation - Every 30s */
    @keyframes rocket-fly {{ 
        0% {{ transform: translate(-10vw, 100vh) rotate(45deg); }} 
        100% {{ transform: translate(110vw, -10vh) rotate(45deg); }} 
    }}
    .rocket {{
        position: fixed; font-size: 3rem; z-index: 0;
        animation: rocket-fly 20s linear infinite;
    }}

    /* Top HUD Styling */
    .scroll-header {{
        text-align: center; font-family: 'Georgia', serif; font-style: italic;
        color: rgba(255,255,255,0.4); font-size: 1.5rem; letter-spacing: 8px;
        margin-top: 20px; text-transform: uppercase;
    }}
    .hud-info {{
        text-align: center; font-family: 'Courier New', monospace; 
        color: #b8a37e; font-size: 1rem; margin-bottom: 30px;
    }}

    /* Manuscript Bar Styling */
    .stChatInputContainer {{ border: none !important; background: transparent !important; padding-bottom: 30px; }}
    .stChatInput textarea {{
        background-color: #f4e4bc !important; 
        color: #2d1b4d !important;
        border: 4px solid #8e735b !important;
        font-family: 'Palatino', serif !important;
        font-size: 1.2rem !important;
        border-radius: 12px !important;
        box-shadow: 0px 15px 40px rgba(0,0,0,0.6) !important;
    }}

    /* Chat Bubbles */
    .stChatMessage {{ background: rgba(255, 255, 255, 0.08) !important; border-radius: 15px !important; margin: 10px 0; }}

    /* GOD MODE INJECTION */
    {st.session_state.custom_css}
</style>
<div class="stars"></div>
<div class="rocket">🚀</div>
""", unsafe_allow_html=True)

# 3. Top HUD Display
st.markdown('<div class="scroll-header">New Scroll</div>', unsafe_allow_html=True)
hud_text = f"{st.session_state.location} | {datetime.now().strftime('%Y-%m-%d | %H:%M:%S')}"
st.markdown(f'<div class="hud-info">{hud_text}</div>', unsafe_allow_html=True)

# 4. Sidebar Logic
with st.sidebar:
    if st.session_state.god_mode:
        st.warning("🛠️ GOD MODE ACTIVE")
        st.session_state.oracle_rules = st.text_area("Brain Persona", st.session_state.oracle_rules)
        st.session_state.location = st.text_input("Set HUD Location", st.session_state.location)
        
        gui_code = st.text_area("Live GUI CSS", placeholder=".stApp { background: black !important; }")
        if st.button("Update GUI Live"):
            st.session_state.custom_css = gui_code
            st.rerun()
            
        if st.button("Exit God Mode"):
            st.session_state.god_mode = False
            st.rerun()
    else:
        st.title("📜 Archives")
        api_key = st.text_input("Enter Groq Key", type="password")
        if st.button("✨ Begin New Scroll"):
            st.session_state.messages = []
            st.rerun()

# 5. Message Handling
if "messages" not in st.session_state or len(st.session_state.messages) == 0:
    st.session_state.messages = [{"role": "system", "content": st.session_state.oracle_rules}]

for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# 6. Chat Logic (Fixed Data Access)
if prompt := st.chat_input("Write upon the scroll..."):
    # Secret Code to Unlock Panel
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
                messages=st.session_state.messages
            )
            
            # FIXED: Correct way to access content in the Groq SDK
            response_text = completion.choices[0].message.content
            
            st.session_state.messages.append({"role": "assistant", "content": response_text})
            st.rerun()
        except Exception as e:
            st.error(f"Celestial Error: {str(e)}")
