import streamlit as st
import requests

st.set_page_config(page_title="HEAT Agents", layout="wide", initial_sidebar_state="expanded")

# NOTE: Ensure your secrets are configured in .streamlit/secrets.toml
try:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
except KeyError:
    GROQ_API_KEY = ""

# ── HEAT Design System — Master CSS ───────────────────────────────────────────
st.markdown("""
<style>
/* ── Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Inter:wght@300;400;500&display=swap');

/* ── Reset & Global Overrides ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

/* Force Link Colors to white/theme (removes Streamlit Blue) */
a, a:visited, .stMarkdown a {
    color: #FFFFFF !important;
    text-decoration: none !important;
    transition: opacity 0.2s ease !important;
}
a:hover, .stMarkdown a:hover {
    opacity: 0.7 !important;
}

/* ── HEAT Design Tokens ── */
:root {
    --bg:          #0B0B0B;
    --sidebar-bg:  #111111;
    --surface:     rgba(255,255,255,0.03);
    --border:      rgba(255,255,255,0.08);
    --text:        #FFFFFF;
    --text-sec:    rgba(255,255,255,0.6);
    --text-muted:  rgba(255,255,255,0.3);
    --orange:      #FF6A00;
}

/* ── Hide Streamlit Chrome ── */
#MainMenu, footer, header,
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"],
.stDeployButton { display: none !important; }

/* ── Base App Styling ── */
.stApp, [data-testid="stAppViewContainer"] {
    background: var(--bg) !important;
    font-family: 'Inter', sans-serif;
    color: var(--text);
}
[data-testid="stMain"] > div, .block-container {
    background: transparent !important;
    padding: 0 !important;
    max-width: 100% !important;
}

/* ── SIDEBAR STYLING ── */
[data-testid="stSidebar"] {
    background-color: var(--sidebar-bg) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] * {
    font-family: 'Inter', sans-serif;
}
/* Adjust Sidebar button */
[data-testid="stSidebar"] div[data-testid="stButton"] > button {
    background: transparent !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    justify-content: flex-start !important;
    padding: 10px 14px !important;
    border-radius: 8px !important;
    font-weight: 500 !important;
}
[data-testid="stSidebar"] div[data-testid="stButton"] > button:hover {
    background: var(--surface) !important;
}
/* Search Input in Sidebar */
[data-testid="stSidebar"] [data-testid="stTextInput"] div[data-baseweb="input"] {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid transparent !important;
    border-radius: 8px !important;
}
[data-testid="stSidebar"] [data-testid="stTextInput"] input {
    color: var(--text) !important;
}
/* Bottom User/Login Section */
.sidebar-bottom-container {
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    padding: 20px;
    border-top: 1px solid var(--border);
    background: var(--sidebar-bg);
    display: flex;
    align-items: center;
    gap: 12px;
}
.sidebar-avatar {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    background: var(--surface);
    border: 1px solid var(--border);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 14px;
}
.sidebar-login-text {
    font-size: 14px;
    font-weight: 500;
}

/* ── TOP NAV BAR ── */
.top-nav {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 16px 24px;
    background: transparent;
    border-bottom: 1px solid var(--border);
}
.nav-left, .nav-right {
    flex: 1;
    font-size: 14px;
    color: var(--text-sec);
}
.nav-right {
    text-align: right;
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 500;
    color: var(--text-muted);
}
.nav-center {
    flex: 1;
    text-align: center;
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 700;
    font-size: 20px;
    letter-spacing: 0.15em;
    text-transform: uppercase;
}

/* ── EMPTY STATE / GREETING ── */
.empty-state-wrapper {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 60vh;
    text-align: center;
    animation: fadeIn 0.8s ease forwards;
}
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}
.empty-state-wrapper h1 {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 52px;
    font-weight: 500;
    color: var(--text);
    margin-bottom: 16px;
    letter-spacing: -0.02em;
}
.empty-state-wrapper p {
    font-family: 'Inter', sans-serif;
    font-size: 16px;
    color: var(--text-sec);
    max-width: 450px;
    line-height: 1.6;
}

/* ── CHAT BUBBLES ── */
.chat-container {
    max-width: 800px;
    margin: 0 auto;
    padding: 40px 20px 120px 20px;
}
[data-testid="stChatMessage"] {
    border-radius: 12px !important;
    margin-bottom: 24px !important;
    padding: 0 !important;
    border: none !important;
    background: transparent !important;
    display: flex !important;
    gap: 16px !important;
}
[data-testid="stChatMessageAvatar"] {
    width: 32px !important;
    height: 32px !important;
    border-radius: 8px !important;
}
[data-testid="stChatMessageContent"] {
    flex: 1 !important;
}
[data-testid="stChatMessage"] p {
    color: var(--text) !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 15px !important;
    line-height: 1.7 !important;
}

/* ── CHAT INPUT (Transparent & Centered visually) ── */
/* Streamlit pins this to bottom, we style it to look floating and transparent */
[data-testid="stBottomBlockContainer"] {
    background: linear-gradient(180deg, transparent, var(--bg) 40%) !important;
    padding-bottom: 20px !important;
}
[data-testid="stChatInput"] {
    max-width: 800px !important;
    margin: 0 auto !important;
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
}
[data-testid="stChatInput"] textarea {
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid var(--border) !important;
    border-radius: 16px !important;
    padding: 16px 20px !important;
    color: var(--text) !important;
    font-size: 15px !important;
}
[data-testid="stChatInput"] textarea:focus {
    border-color: rgba(255,255,255,0.2) !important;
    background: rgba(255,255,255,0.08) !important;
}
[data-testid="stChatInputSubmitButton"] {
    background: transparent !important;
}
[data-testid="stChatInputSubmitButton"] svg { 
    fill: var(--text) !important; 
}

/* Scrollbar */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 4px; }
</style>
""", unsafe_allow_html=True)

# ── Core Logic ────────────────────────────────────────────────────────────────

def get_response(system_prompt, user_input):
    if not GROQ_API_KEY:
        return "System error: Missing API Key."
        
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ]
    }
    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        result = response.json()
        if "choices" not in result:
            error_msg = result.get("error", {}).get("message", str(result))
            st.error(f"API Error: {error_msg}")
            return None
        return result['choices'][0]['message']['content']
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None

agents = {
    "founder": {
        "name": "Startup Founder",
        "prompt": "You are a bold startup founder. Move fast, take risks, prioritize execution."
    },
    "strategist": {
        "name": "Corporate Strategist",
        "prompt": "You are a corporate strategist. Think in structures, mitigate risks, be data-driven."
    },
    "minimalist": {
        "name": "Minimalist Advisor",
        "prompt": "You are a minimalist advisor. Keep things incredibly simple. Avoid unnecessary effort."
    },
    "hustler": {
        "name": "Freelance Hustler",
        "prompt": "You are a freelancer hustler. Focus on cash flow and rapid practical execution."
    }
}

# ── Session State ─────────────────────────────────────────────────────────────
if "active_agent" not in st.session_state:
    st.session_state.active_agent = "minimalist" # Default based on screenshot
if "messages" not in st.session_state:
    st.session_state.messages = {}

# Handle URL params
if "agent" in st.query_params:
    agent_key = st.query_params["agent"]
    if agent_key in agents:
        st.session_state.active_agent = agent_key

key = st.session_state.active_agent
agent = agents.get(key, agents["minimalist"])

if key not in st.session_state.messages:
    st.session_state.messages[key] = []


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.button("⨁ New Chat", use_container_width=True)
    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
    
    st.text_input("search", placeholder="Search chat...", label_visibility="collapsed")
    st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)
    
    # Fake History for layout display
    st.markdown("<span style='font-size: 12px; color: var(--text-muted); font-weight: 600; letter-spacing: 1px; text-transform: uppercase;'>Recent</span>", unsafe_allow_html=True)
    st.markdown("<div style='padding: 10px 0; font-size: 14px; color: var(--text-sec); cursor: pointer;'>Q3 Efficiency Strategy</div>", unsafe_allow_html=True)
    st.markdown("<div style='padding: 10px 0; font-size: 14px; color: var(--text-sec); cursor: pointer;'>Simplifying onboarding</div>", unsafe_allow_html=True)

    # Bottom Login Section
    st.markdown("""
    <div class="sidebar-bottom-container">
        <div class="sidebar-avatar">?</div>
        <div class="sidebar-login-text">
            <a href="#">Sign in</a>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ── Top Navbar ────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="top-nav">
    <div class="nav-left">
        <a href="https://heat-ai.c36.airoapp.ai/explore">← Explore AI</a>
    </div>
    <div class="nav-center">
        <a href="https://heat-ai.c36.airoapp.ai/">HEAT</a>
    </div>
    <div class="nav-right">
        {agent['name']} <span style="color: var(--orange);">●</span>
    </div>
</div>
""", unsafe_allow_html=True)


# ── Chat Container ────────────────────────────────────────────────────────────
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

# Render Empty State OR Chat History
if len(st.session_state.messages[key]) == 0:
    # Centered Welcome Message
    st.markdown(f"""
    <div class="empty-state-wrapper">
        <h1>Good evening.</h1>
        <p>I am the <b>{agent['name']}</b>.<br>How can we align and proceed efficiently today?</p>
    </div>
    """, unsafe_allow_html=True)
else:
    for msg in st.session_state.messages[key]:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

st.markdown('</div>', unsafe_allow_html=True)


# ── Chat Input ────────────────────────────────────────────────────────────────
# Streamlit inherently keeps this at the bottom of the screen.
# Custom CSS above removes the background box to make it appear floating/clean.
user_input = st.chat_input("Message the advisor...")

if user_input:
    st.session_state.messages[key].append({"role": "user", "content": user_input})
    st.rerun()

# ── Handle Assistant Response generation ──
if len(st.session_state.messages[key]) > 0 and st.session_state.messages[key][-1]["role"] == "user":
    last_user_msg = st.session_state.messages[key][-1]["content"]
    
    with st.chat_message("assistant"):
        with st.spinner("Analyzing..."):
            response = get_response(agent["prompt"], last_user_msg)
            
        if response:
            st.write(response)
            st.session_state.messages[key].append({"role": "assistant", "content": response})