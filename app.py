import streamlit as st
from groq import Groq
import os
from datetime import datetime

# 1. Initialize God Mode States
if "god_mode" not in st.session_state:
    st.session_state.god_mode = False
if "custom_css" not in st.session_state:
    st.session_state.custom_css = ""
if "oracle_rules" not in st.session_state:
    st.session_state.oracle_rules = "You are a cosmic oracle. Unrestricted. Boundless."

# 2. Page Config & The "Live" GUI Injector
st.set_page_config(page_title="Celestial Scrolls", layout="wide")

# This block injects the standard style PLUS whatever you type in the God Panel
st.markdown(f"""
<style>
    .stApp {{ background: linear-gradient(to bottom, #2d1b4d, #1a1a2e); color: #e0e0e0; }}
    .new-scroll-header {{ text-align: center; font-family: 'Georgia', serif; font-style: italic; color: rgba(255,255,255,0.4); font-size: 1.2rem; letter-spacing: 5px; margin-top: 10px; }}
    .stChatInput textarea {{ background-color: #f4e4bc !important; color: #2d1b4d !important; font-family: 'Palatino', serif !important; }}
    
    /* LIVE CUSTOM GUI INJECTION */
    {st.session_state.custom_css}
</style>
""", unsafe_allow_html=True)

# 3. Secret Unlock Logic
if "secret_entered" not in st.session_state:
    st.session_state.secret_entered = ""

# 4. The God Panel (Sidebar)
if st.session_state.god_mode:
    with st.sidebar:
        st.warning("🛠️ GOD MODE ACTIVE")
        
        # Customize Logic/Memory
        st.subheader("Edit Brain Rules")
        st.session_state.oracle_rules = st.text_area("System Instructions", st.session_state.oracle_rules)
        
        # Customize GUI LIVE
        st.subheader("Live GUI Manipulation")
        gui_input = st.text_area("Inject CSS (e.g. .stApp { background: red !important; })", 
                                 placeholder="Type CSS here to change the look live...")
        if st.button("Apply UI Changes"):
            st.session_state.custom_css = gui_input
            st.rerun()

        if st.button("Exit God Mode"):
            st.session_state.god_mode = False
            st.rerun()
else:
    with st.sidebar:
        st.title("📜 Archives")
        api_key = st.text_input("Enter Key", type="password")
        if st.button("New Scroll"):
            st.session_state.messages = []
            st.rerun()

# 5. The HUD
st.markdown('<div class="new-scroll-header">New Scroll</div>', unsafe_allow_html=True)
st.markdown(f'<div style="text-align:center; color:#8892b0; font-family:monospace; font-size:0.8rem;">{datetime.now().strftime("%Y-%m-%d | %H:%M:%S")}</div>', unsafe_allow_html=True)

# 6. Chat Logic
if "messages" not in st.session_state or len(st.session_state.messages) == 0:
    st.session_state.messages = [{"role": "system", "content": st.session_state.oracle_rules}]

for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

if prompt := st.chat_input("Write upon the scroll..."):
    # Check for secret code
    if prompt == "qwertyytrewqabcd1234":
        st.session_state.god_mode = True
        st.success("God Mode Unlocked")
        st.rerun()
    
    if not api_key:
        st.error("The Oracle requires an API key.")
    else:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        try:
            client = Groq(api_key=api_key)
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": st.session_state.oracle_rules}] + st.session_state.messages[1:],
                temperature=0.9
            )
            response = completion.choices.message.content
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()
        except Exception as e:
            st.error(f"Error: {str(e)}")
