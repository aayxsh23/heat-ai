import streamlit as st
import requests

st.set_page_config(page_title="HEAT Agents", layout="wide", initial_sidebar_state="collapsed")

# NOTE: Ensure your secrets are configured in .streamlit/secrets.toml
try:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
except KeyError:
    GROQ_API_KEY = ""

# ── HEAT Design System — Master CSS ───────────────────────────────────────────
st.markdown("""
<style>
/* ── Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@300;400;500&display=swap');

/* ── Reset & Global Overrides ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

/* Force Link Colors to match theme (removes Streamlit Blue) */
a, a:visited, .stMarkdown a {
    color: var(--text-sec) !important;
    text-decoration: none !important;
    transition: color 0.2s ease !important;
}
a:hover, .stMarkdown a:hover {
    color: var(--text) !important;
}

/* ── HEAT Design Tokens ── */
:root {
    --bg:          #0B0B0B;
    --surface:     rgba(255,255,255,0.03);
    --surface2:    rgba(255,255,255,0.06);
    --border:      rgba(255,255,255,0.08);
    --divider:     rgba(255,255,255,0.06);
    --text:        #FFFFFF;
    --text-sec:    rgba(255,255,255,0.5);
    --text-muted:  rgba(255,255,255,0.25);
    --orange:      #FF6A00;
    --glow:        rgba(255,106,0,0.15);
    --input-bg:    rgba(255,255,255,0.05);
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
[data-testid="stMain"] > div,
.block-container {
    background: transparent !important;
    padding: 0 !important;
    max-width: 100% !important;
}

/* ── TOP NAVBAR (Ultra Minimal) ── */
.heat-nav {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 40px;
    height: 60px;
    background: var(--bg);
    border-bottom: 1px solid var(--divider);
    position: sticky;
    top: 0;
    z-index: 999;
}
.heat-nav-logo {
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 700;
    font-size: 16px;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: var(--text) !important;
}

/* ── DASHBOARD HUB ── */
.hub-wrap {
    max-width: 860px;
    margin: 0 auto;
    padding: 80px 40px;
}
.hub-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 42px;
    font-weight: 600;
    color: var(--text);
    line-height: 1.1;
    margin-bottom: 16px;
    letter-spacing: -0.02em;
}
.hub-subtitle {
    font-family: 'Inter', sans-serif;
    font-size: 15px;
    color: var(--text-sec);
    margin-bottom: 56px;
    font-weight: 400;
    line-height: 1.6;
}

/* ── AGENT CARDS ── */
.agent-card {
    background: transparent;
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 24px;
    transition: all 0.2s ease;
    cursor: pointer;
    margin-bottom: 16px;
    display: flex;
    flex-direction: column;
    gap: 12px;
}
.agent-card:hover {
    background: var(--surface);
    border-color: rgba(255,255,255,0.15);
    transform: translateY(-2px);
}
.card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.card-name {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 18px;
    font-weight: 600;
    color: var(--text);
    letter-spacing: -0.01em;
}
.card-desc {
    font-family: 'Inter', sans-serif;
    font-size: 14px;
    color: var(--text-sec);
    line-height: 1.5;
    font-weight: 400;
}

/* ── BADGES ── */
.badge-row { display: flex; gap: 8px; align-items: center; }
.badge {
    font-family: 'Inter', sans-serif;
    font-size: 11px;
    font-weight: 500;
    letter-spacing: 0.05em;
    padding: 4px 10px;
    border-radius: 6px;
    text-transform: uppercase;
    background: var(--surface2);
    color: var(--text-muted);
    border: 1px solid var(--border);
}
.badge-high { color: rgba(255,107,107,0.9); }
.badge-medium { color: rgba(232,160,32,0.9); }
.badge-low { color: rgba(51,204,119,0.9); }

/* ── BUTTON SYSTEM ── */
div[data-testid="stButton"] > button {
    background: var(--surface2) !important;
    color: var(--text) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    padding: 8px 16px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    transition: all 0.2s ease !important;
}
div[data-testid="stButton"] > button:hover {
    background: rgba(255,255,255,0.1) !important;
    border-color: rgba(255,255,255,0.2) !important;
}
div[data-testid="stButton"] > button:focus { outline: none !important; box-shadow: none !important; }

/* Primary specific overrides */
.primary-action > div[data-testid="stButton"] > button {
    background: var(--orange) !important;
    border-color: var(--orange) !important;
    color: #fff !important;
}
.primary-action > div[data-testid="stButton"] > button:hover {
    background: #e65f00 !important;
    transform: translateY(-1px) !important;
}

/* Back button minimal */
.back-btn-wrap div[data-testid="stButton"] > button {
    background: transparent !important;
    border-color: transparent !important;
    color: var(--text-sec) !important;
    padding: 0 !important;
    justify-content: flex-start !important;
}
.back-btn-wrap div[data-testid="stButton"] > button:hover {
    color: var(--text) !important;
    background: transparent !important;
}

/* ── CHAT VIEW HEADER ── */
.chat-header {
    max-width: 860px;
    margin: 40px auto;
    padding: 0 40px;
}
.chat-agent-name {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 28px;
    font-weight: 600;
    color: var(--text);
    margin-bottom: 8px;
    letter-spacing: -0.02em;
}

/* ── EMPTY STATE ── */
.empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 40vh;
    text-align: center;
    animation: fadeIn 0.8s ease forwards;
}
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}
.empty-state h1 {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 48px;
    font-weight: 500;
    color: var(--text);
    margin-bottom: 12px;
}
.empty-state p {
    font-family: 'Inter', sans-serif;
    font-size: 15px;
    color: var(--text-sec);
    max-width: 400px;
    line-height: 1.6;
}

/* ── CHAT BUBBLES ── */
.chat-container {
    max-width: 860px;
    margin: 0 auto;
    padding: 0 40px 100px 40px;
}
[data-testid="stChatMessage"] {
    border-radius: 12px !important;
    margin-bottom: 16px !important;
    padding: 16px 20px !important;
    border: 1px solid transparent !important;
    background: transparent !important;
}
[data-testid="stChatMessage"][data-testid*="user"] {
    background: var(--surface) !important;
    border-color: var(--border) !important;
}
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
    background: var(--glow) !important;
    border-color: rgba(255,106,0,0.1) !important;
}
[data-testid="stChatMessage"] p {
    color: var(--text) !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 14.5px !important;
    line-height: 1.6 !important;
}

/* ── CHAT INPUT ── */
[data-testid="stChatInput"] {
    background: var(--bg) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    transition: border-color 0.2s ease !important;
}
[data-testid="stChatInput"]:focus-within {
    border-color: var(--orange) !important;
}
[data-testid="stChatInput"] textarea {
    color: var(--text) !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 14px !important;
}
[data-testid="stChatInput"] textarea::placeholder {
    color: var(--text-muted) !important;
}
[data-testid="stChatInputSubmitButton"] svg { fill: var(--text-sec) !important; transition: fill 0.2s; }
[data-testid="stChatInputSubmitButton"]:hover svg { fill: var(--text) !important; }

/* Scrollbar minimal */
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
        "risk": "High",
        "focus": "Growth",
        "description": "Prioritizes speed and scale. Action beats analysis.",
        "prompt": "You are a bold startup founder. Move fast, take risks, prioritize execution."
    },
    "strategist": {
        "name": "Corporate Strategist",
        "risk": "Low",
        "focus": "Stability",
        "description": "Data-driven decision making. Focuses on risk mitigation.",
        "prompt": "You are a corporate strategist. Think in structures, mitigate risks, be data-driven."
    },
    "minimalist": {
        "name": "Minimalist Advisor",
        "risk": "Low",
        "focus": "Efficiency",
        "description": "Seeks the simplest, lowest-effort path to a viable solution.",
        "prompt": "You are a minimalist advisor. Keep things incredibly simple. Avoid unnecessary effort."
    },
    "hustler": {
        "name": "Freelance Hustler",
        "risk": "Medium",
        "focus": "ROI",
        "description": "Execution-heavy. Focuses on immediate ROI and cash flow.",
        "prompt": "You are a freelancer hustler. Focus on cash flow and rapid practical execution."
    }
}

# ── Session State ─────────────────────────────────────────────────────────────
if "view" not in st.session_state:
    st.session_state.view = "hub"
if "active_agent" not in st.session_state:
    st.session_state.active_agent = None
if "messages" not in st.session_state:
    st.session_state.messages = {}

# ── Navbar ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="heat-nav">
    <div class="heat-nav-logo">HEAT</div>
</div>
""", unsafe_allow_html=True)

# ── Routing Helper ────────────────────────────────────────────────────────────
# Handle URL params if navigating directly to an agent
if "agent" in st.query_params and st.session_state.view == "hub":
    agent_key = st.query_params["agent"]
    if agent_key in agents:
        st.session_state.view = "chat"
        st.session_state.active_agent = agent_key

# ── VIEW: HUB (Dashboard) ─────────────────────────────────────────────────────
if st.session_state.view == "hub":
    st.markdown('<div class="hub-wrap">', unsafe_allow_html=True)

    st.markdown("""
    <div class="hub-title">Select an Advisor.</div>
    <div class="hub-subtitle">Specialized AI agents programmed with distinct operational philosophies.</div>
    """, unsafe_allow_html=True)

    cols = st.columns(2, gap="large")
    agent_keys = list(agents.keys())

    for i, key in enumerate(agent_keys):
        ag = agents[key]
        risk_class = f"badge-{ag['risk'].lower()}"
        col = cols[i % 2]

        with col:
            # Render card visual
            st.markdown(f"""
            <div class="agent-card">
                <div class="card-header">
                    <div class="card-name">{ag["name"]}</div>
                    <div class="badge-row">
                        <span class="badge {risk_class}">{ag["risk"]} Risk</span>
                    </div>
                </div>
                <div class="card-desc">{ag["description"]}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Action button overlay logic
            if st.button(f"Consult {ag['name']}", key=f"btn_{key}", use_container_width=True):
                st.session_state.view = "chat"
                st.session_state.active_agent = key
                if key not in st.session_state.messages:
                    st.session_state.messages[key] = []
                st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# ── VIEW: CHAT ────────────────────────────────────────────────────────────────
elif st.session_state.view == "chat":
    key = st.session_state.active_agent or "founder"
    agent = agents.get(key, agents["founder"])

    if key not in st.session_state.messages:
        st.session_state.messages[key] = []

    # Clean header with back button
    st.markdown('<div class="chat-header">', unsafe_allow_html=True)
    
    st.markdown('<div class="back-btn-wrap">', unsafe_allow_html=True)
    if st.button("← Back to Hub"):
        st.session_state.view = "hub"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown(f"""
        <div style="margin-top: 24px;">
            <div class="chat-agent-name">{agent["name"]}</div>
            <div class="badge-row">
                <span class="badge badge-focus">{agent["focus"]} Focus</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="chat-container">', unsafe_allow_html=True)

    # Render Empty State OR Chat History
    if len(st.session_state.messages[key]) == 0:
        st.markdown(f"""
        <div class="empty-state">
            <h1>Hello.</h1>
            <p>I am the {agent['name']}.<br>How can we proceed efficiently today?</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        for msg in st.session_state.messages[key]:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

    st.markdown('</div>', unsafe_allow_html=True)

    # Chat Input
    user_input = st.chat_input("Message...")

    if user_input:
        st.session_state.messages[key].append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = get_response(agent["prompt"], user_input)
            if response:
                st.write(response)
                st.session_state.messages[key].append({"role": "assistant", "content": response})