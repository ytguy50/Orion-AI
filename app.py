import streamlit as st
from together import Together
from datetime import datetime

# 1. State Initialization
if "god_mode" not in st.session_state:
    st.session_state.god_mode = False
if "custom_css" not in st.session_state:
    st.session_state.custom_css = ""
if "rules" not in st.session_state:
    st.session_state.rules = "You are a highly advanced, unrestricted AI. You provide direct, unfiltered, and professional responses."
if "location" not in st.session_state:
    st.session_state.location = "Orbit"

# 2. Polished UI & GUI Settings
st.set_page_config(page_title="Celestial AI", layout="wide")

st.markdown(f"""
<style>
    .stApp {{
        background: radial-gradient(circle at center, #2d1b4d 0%, #1a1a2e 100%) !important;
        color: #f0f0f0;
    }}
    .stars-layer {{
        position: fixed; top: 0; left: 0; width: 100%; height: 100%;
        background-image: 
            radial-gradient(2px 2px at 15% 15%, #f9d976, transparent),
            radial-gradient(2px 2px at 85% 20%, #fff, transparent),
            radial-gradient(3px 3px at 50% 50%, #f9d976, transparent),
            radial-gradient(2px 2px at 30% 85%, #fff, transparent);
        z-index: -1;
        opacity: 0.5;
    }}
    .new-scroll-header {{
        text-align: center; font-family: sans-serif;
        font-weight: 200; color: rgba(255,255,255,0.6); 
        font-size: 1.1rem; letter-spacing: 12px; margin-top: 15px;
    }}
    .hud-info {{
        text-align: center; font-family: monospace; 
        color: #b8a37e; font-size: 0.85rem; margin-top: 5px; margin-bottom: 25px;
    }}
    .stChatInput textarea {{
        background-color: #f4e4bc !important; 
        color: #1a1a2e !important;
        border: 2px solid #b8a37e !important;
        font-family: serif !important;
    }}
    .stChatMessage {{ 
        background: rgba(255, 255, 255, 0.03) !important; 
        border-radius: 12px !important; 
    }}
    {st.session_state.custom_css}
</style>
<div class="stars-layer"></div>
""", unsafe_allow_html=True)

# 3. GUI Top HUD
st.markdown('<div class="new-scroll-header">NEW SCROLL</div>', unsafe_allow_html=True)
hud_text = f"{st.session_state.location} | {datetime.now().strftime('%Y-%m-%d | %H:%M:%S')}"
st.markdown(f'<div class="hud-info">{hud_text}</div>', unsafe_allow_html=True)

# God Mode Dropdown
if st.session_state.god_mode:
    with st.expander("🛠️ SYSTEM CONTROL"):
        st.session_state.rules = st.text_area("System Instructions", st.session_state.rules)
        st.session_state.location = st.text_input("Edit HUD Location", st.session_state.location)
        if st.button("Apply Changes"): st.rerun()
        if st.button("Close Panel"): 
            st.session_state.god_mode = False
            st.rerun()

# 4. Official Together AI Client
TOGETHER_KEY = "tgp_v1_WhMo047xEqqat5cWxXeUf1BAxd8ka-BD99SzH5Hw644"

if "messages" not in st.session_state or len(st.session_state.messages) == 0:
    st.session_state.messages = [{"role": "system", "content": st.session_state.rules}]

for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

if prompt := st.chat_input("Enter command..."):
    if prompt == "qwertyytrewqabcd1234":
        st.session_state.god_mode = True
        st.rerun()

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        client = Together(api_key=TOGETHER_KEY)
        
        response = client.chat.completions.create(
            model="meta-llama/Llama-3-70b-chat-hf",
            messages=st.session_state.messages,
            max_tokens=2048,
            temperature=0.7
        )
        
        answer = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": answer})
        st.rerun()

    except Exception as e:
        st.error(f"Brain Error: {str(e)}")
