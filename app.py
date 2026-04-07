import streamlit as st
import requests

st.set_page_config(page_title="HEAT Agents", layout="wide", initial_sidebar_state="collapsed")

GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

# ── HEAT Design System — Master CSS ───────────────────────────────────────────
st.markdown("""
<style>
/* ── Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Inter:wght@300;400;500;600&display=swap');

/* ── Reset ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

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
    --glow-strong: rgba(255,106,0,0.25);
    --input-bg:    rgba(255,255,255,0.05);
    --red-dim:     rgba(255,68,68,0.12);
    --red-text:    #FF6B6B;
    --green-dim:   rgba(51,204,119,0.12);
    --green-text:  #33CC77;
    --yellow-dim:  rgba(232,160,32,0.12);
    --yellow-text: #E8A020;
}

/* ── Hide Streamlit Chrome ── */
#MainMenu, footer, header,
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"],
.viewerBadge_container__1QSob,
.stDeployButton { display: none !important; }

/* ── Base ── */
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

/* ── TOP NAVBAR ── */
.heat-nav {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 56px;
    height: 64px;
    background: rgba(11,11,11,0.85);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border-bottom: 1px solid var(--divider);
    position: sticky;
    top: 0;
    z-index: 999;
}
.heat-nav-logo {
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 700;
    font-size: 17px;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--text);
    text-decoration: none;
    transition: color 0.2s;
}
.heat-nav-logo:hover { color: var(--orange); }
.heat-nav-links {
    display: flex;
    align-items: center;
    gap: 36px;
}
.heat-nav-links a {
    font-family: 'Inter', sans-serif;
    font-size: 13px;
    font-weight: 400;
    color: var(--text-sec);
    text-decoration: none;
    letter-spacing: 0.01em;
    transition: color 0.2s;
}
.heat-nav-links a:hover { color: var(--text); }
.heat-nav-links a.active { color: var(--text); }
.heat-nav-btn {
    border: 1px solid var(--border) !important;
    border-radius: 24px !important;
    padding: 7px 20px !important;
    color: var(--text) !important;
    background: transparent !important;
    font-size: 13px !important;
    font-family: 'Inter', sans-serif !important;
    transition: border-color 0.2s, background 0.2s !important;
}
.heat-nav-btn:hover {
    border-color: rgba(255,255,255,0.2) !important;
    background: var(--surface2) !important;
}

/* ── DASHBOARD HUB ── */
.hub-wrap {
    max-width: 960px;
    margin: 0 auto;
    padding: 0 40px;
}
.hub-header {
    padding: 80px 0 56px 0;
    text-align: center;
}
.hub-eyebrow {
    font-family: 'Inter', sans-serif;
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 0.22em;
    color: var(--orange);
    text-transform: uppercase;
    margin-bottom: 20px;
    opacity: 0.9;
}
.hub-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 48px;
    font-weight: 700;
    color: var(--text);
    line-height: 1.08;
    margin-bottom: 18px;
    letter-spacing: -0.02em;
}
.hub-subtitle {
    font-family: 'Inter', sans-serif;
    font-size: 15px;
    color: var(--text-sec);
    max-width: 420px;
    margin: 0 auto;
    line-height: 1.7;
    font-weight: 400;
}

/* ── AGENT CARDS ── */
.agent-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 28px 28px 20px 28px;
    transition: border-color 0.3s, transform 0.3s, box-shadow 0.3s;
    cursor: pointer;
    position: relative;
    overflow: hidden;
}
.agent-card::before {
    content: '';
    position: absolute;
    inset: 0;
    border-radius: 16px;
    background: radial-gradient(ellipse at top left, var(--glow), transparent 65%);
    opacity: 0;
    transition: opacity 0.3s;
    pointer-events: none;
}
.agent-card:hover {
    border-color: rgba(255,106,0,0.3);
    transform: translateY(-3px);
    box-shadow: 0 12px 40px rgba(0,0,0,0.4), 0 0 0 1px rgba(255,106,0,0.08);
}
.agent-card:hover::before { opacity: 1; }
.card-icon {
    width: 48px;
    height: 48px;
    border-radius: 10px;
    background: var(--surface2);
    border: 1px solid var(--border);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 18px;
    margin-bottom: 20px;
    color: var(--text-sec);
    transition: border-color 0.3s, color 0.3s;
}
.agent-card:hover .card-icon {
    border-color: rgba(255,106,0,0.3);
    color: var(--orange);
}
.card-name {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 18px;
    font-weight: 600;
    color: var(--text);
    margin-bottom: 12px;
    letter-spacing: -0.01em;
}
.card-desc {
    font-family: 'Inter', sans-serif;
    font-size: 13px;
    color: var(--text-sec);
    line-height: 1.65;
    margin: 14px 0 20px 0;
    min-height: 38px;
    font-weight: 400;
}

/* ── BADGES ── */
.badge-row { display: flex; gap: 6px; flex-wrap: wrap; align-items: center; }
.badge {
    font-family: 'Inter', sans-serif;
    font-size: 11px;
    font-weight: 500;
    letter-spacing: 0.04em;
    padding: 3px 10px;
    border-radius: 20px;
    border: 1px solid;
    line-height: 1.6;
}
.badge-high   { background: var(--red-dim);    color: var(--red-text);    border-color: rgba(255,107,107,0.2); }
.badge-medium { background: var(--yellow-dim); color: var(--yellow-text); border-color: rgba(232,160,32,0.2); }
.badge-low    { background: var(--green-dim);  color: var(--green-text);  border-color: rgba(51,204,119,0.2); }
.badge-focus  { background: var(--surface2);   color: var(--text-muted);  border-color: var(--border); }

/* ── BUTTON SYSTEM ── */

/* Primary — Orange Pill */
div[data-testid="stButton"].primary-action > button,
.stButton.primary-action > button {
    background: var(--orange) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 24px !important;
    padding: 11px 28px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    letter-spacing: 0.03em !important;
    width: 100% !important;
    transition: opacity 0.2s, transform 0.2s, box-shadow 0.2s !important;
    box-shadow: 0 0 0 0 var(--glow) !important;
    cursor: pointer !important;
}
div[data-testid="stButton"].primary-action > button:hover {
    opacity: 0.88 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 24px var(--glow-strong) !important;
}
div[data-testid="stButton"].primary-action > button:active {
    transform: translateY(0) !important;
    opacity: 1 !important;
}

/* Secondary — Ghost */
.stButton > button {
    width: 100% !important;
    background: transparent !important;
    color: var(--text-sec) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    padding: 10px 20px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 13px !important;
    font-weight: 400 !important;
    letter-spacing: 0.01em !important;
    transition: border-color 0.2s, color 0.2s, background 0.2s !important;
    cursor: pointer !important;
}
.stButton > button:hover {
    border-color: rgba(255,255,255,0.18) !important;
    color: var(--text) !important;
    background: var(--surface2) !important;
}
.stButton > button:focus { box-shadow: none !important; outline: none !important; }

/* Back button — minimal ghost */
.back-btn-wrap .stButton > button {
    width: auto !important;
    padding: 8px 16px !important;
    border-radius: 8px !important;
    font-size: 12px !important;
    color: var(--text-muted) !important;
    border-color: transparent !important;
    background: transparent !important;
}
.back-btn-wrap .stButton > button:hover {
    color: var(--text-sec) !important;
    background: var(--surface2) !important;
    border-color: var(--border) !important;
}

/* ── AGENT HEADER ── */
.agent-header {
    max-width: 900px;
    margin: 0 auto;
    padding: 52px 40px 0 40px;
}
.agent-title-row {
    display: flex;
    align-items: flex-start;
    gap: 18px;
    margin-bottom: 14px;
}
.agent-icon-box {
    width: 52px;
    height: 52px;
    border-radius: 12px;
    background: var(--surface2);
    border: 1px solid var(--border);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
    flex-shrink: 0;
    color: var(--orange);
}
.agent-name {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 26px;
    font-weight: 700;
    color: var(--text);
    line-height: 1.2;
    margin-bottom: 10px;
    letter-spacing: -0.02em;
}
.agent-desc {
    font-family: 'Inter', sans-serif;
    font-size: 14px;
    color: var(--text-sec);
    margin-top: 14px;
    max-width: 520px;
    line-height: 1.7;
    font-weight: 400;
}
.agent-divider {
    height: 1px;
    background: var(--divider);
    max-width: 900px;
    margin: 28px auto;
}

/* ── CHAT AREA ── */
.chat-wrap {
    max-width: 900px;
    margin: 0 auto;
    padding: 0 40px;
}

/* Shared chat message shell */
[data-testid="stChatMessage"] {
    border-radius: 12px !important;
    margin-bottom: 10px !important;
    padding: 14px 18px !important;
    border: 1px solid transparent !important;
}

/* User bubble — muted dark */
[data-testid="stChatMessage"][data-testid*="user"],
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
    background: rgba(255,255,255,0.04) !important;
    border-color: var(--border) !important;
}

/* Assistant bubble — orange-tinted surface */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
    background: rgba(255,106,0,0.05) !important;
    border-color: rgba(255,106,0,0.12) !important;
}

[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] div {
    color: var(--text) !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 14px !important;
    line-height: 1.75 !important;
}

/* ── CHAT INPUT ── */
[data-testid="stChatInput"] {
    background: var(--input-bg) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}
[data-testid="stChatInput"]:focus-within {
    border-color: rgba(255,106,0,0.35) !important;
    box-shadow: 0 0 0 3px var(--glow) !important;
}
[data-testid="stChatInput"] textarea {
    color: var(--text) !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 14px !important;
    background: transparent !important;
}
[data-testid="stChatInput"] textarea::placeholder {
    color: var(--text-muted) !important;
}
[data-testid="stChatInputSubmitButton"] svg { fill: var(--orange) !important; }

/* ── FOOTER ── */
.heat-footer {
    border-top: 1px solid var(--divider);
    padding: 28px 56px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-top: 60px;
}
.heat-footer-logo {
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 700;
    font-size: 14px;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--text);
}
.heat-footer-copy {
    font-family: 'Inter', sans-serif;
    font-size: 12px;
    color: var(--text-muted);
}
.heat-footer-link {
    font-family: 'Inter', sans-serif;
    font-size: 12px;
    color: var(--text-muted);
    text-decoration: none;
    transition: color 0.2s;
}
.heat-footer-link:hover { color: var(--text-sec); }

/* ── Spinner ── */
[data-testid="stSpinner"] { color: var(--orange) !important; }
[data-testid="stSpinner"] > div { border-top-color: var(--orange) !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.08); border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: rgba(255,255,255,0.14); }

/* ── Section label utility ── */
.label-caps {
    font-family: 'Inter', sans-serif;
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--text-muted);
    margin-bottom: 24px;
    display: block;
}

/* ── Empty state spacer ── */
.spacer-lg { height: 40px; }
.spacer-sm { height: 16px; }
</style>
""", unsafe_allow_html=True)

# ── Core Logic ────────────────────────────────────────────────────────────────

def get_response(system_prompt, user_input):
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
    except requests.exceptions.Timeout:
        st.error("Request timed out. Please try again.")
        return None
    except requests.exceptions.ConnectionError:
        st.error("Connection error. Check your internet connection.")
        return None
    except Exception as e:
        st.error(f"Unexpected error: {str(e)}")
        return None

agents = {
    "founder": {
        "name": "Startup Founder",
        "icon": "△",
        "risk": "High",
        "focus": "Growth",
        "description": "Prioritizes speed and scale. Action beats analysis.",
        "prompt": """You are a bold startup founder.\n- Risk Level: HIGH\n- Focus: Growth\nBehavior:\n- Move fast, take risks\n- Prioritize execution over planning\n- Encourage bold decisions\n\nRespond in:\nAdvice:\nKey Recommendation:\nRisk Level:"""
    },
    "strategist": {
        "name": "Corporate Strategist",
        "icon": "⊞",
        "risk": "Low",
        "focus": "Stability",
        "description": "Data-driven decision making. Focuses on risk mitigation.",
        "prompt": """You are a corporate strategist.\n- Risk Level: LOW\n- Focus: Stability\nBehavior:\n- Structured thinking\n- Data-driven decisions\n- Minimize risk\n\nRespond in:\nAdvice:\nKey Recommendation:\nRisk Level:"""
    },
    "minimalist": {
        "name": "Minimalist Advisor",
        "icon": "◎",
        "risk": "Low",
        "focus": "Efficiency",
        "description": "Seeks the simplest, lowest-effort path to a viable solution.",
        "prompt": """You are a minimalist advisor.\n- Risk Level: LOW\n- Focus: Efficiency\nBehavior:\n- Keep things simple\n- Avoid unnecessary effort\n- Choose clarity over complexity\n\nRespond in:\nAdvice:\nKey Recommendation:\nRisk Level:"""
    },
    "hustler": {
        "name": "Freelancer Hustler",
        "icon": "↗",
        "risk": "Medium",
        "focus": "ROI",
        "description": "Execution-heavy. Focuses on immediate ROI and cash flow.",
        "prompt": """You are a freelancer hustler.\n- Risk Level: MEDIUM\n- Focus: ROI\nBehavior:\n- Focus on making money quickly\n- Execution over perfection\n- Practical and action-driven\n\nRespond in:\nAdvice:\nKey Recommendation:\nRisk Level:"""
    }
}

RISK_BADGE = {
    "High":   "badge badge-high",
    "Medium": "badge badge-medium",
    "Low":    "badge badge-low",
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
    <a class="heat-nav-logo" href="https://bhy476x6le.c36.airoapp.ai/" target="_blank">HEAT</a>
    <div class="heat-nav-links">
        <a href="https://bhy476x6le.c36.airoapp.ai/explore" target="_blank" class="active">Explore</a>
        <a href="https://bhy476x6le.c36.airoapp.ai/" target="_blank">Create AI</a>
        <a href="https://bhy476x6le.c36.airoapp.ai/" target="_blank" class="heat-nav-btn">Login</a>
    </div>
</div>
""", unsafe_allow_html=True)

# ── URL param: allow direct agent link (?agent=founder) ──────────────────────
query_params = st.query_params
if "agent" in query_params and st.session_state.view == "hub":
    agent_key = query_params.get("agent", "founder")
    if agent_key in agents:
        st.session_state.view = "chat"
        st.session_state.active_agent = agent_key

# ── VIEW: HUB (Dashboard) ─────────────────────────────────────────────────────
if st.session_state.view == "hub":
    st.markdown('<div class="hub-wrap">', unsafe_allow_html=True)

    st.markdown("""
    <div class="hub-header">
        <div class="hub-eyebrow">Marketplace</div>
        <div class="hub-title">The Marketplace of Minds</div>
        <div class="hub-subtitle">Consult AI agents built from real human expertise. Each one thinks differently.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<span class="label-caps" style="text-align:center;display:block;">Available Agents</span>', unsafe_allow_html=True)

    cols = st.columns(2, gap="large")
    agent_keys = list(agents.keys())

    for i, key in enumerate(agent_keys):
        ag = agents[key]
        risk_cls = RISK_BADGE.get(ag["risk"], "badge badge-focus")
        col = cols[i % 2]

        with col:
            st.markdown(f"""
            <div class="agent-card">
                <div class="card-icon">{ag["icon"]}</div>
                <div class="card-name">{ag["name"]}</div>
                <div class="badge-row">
                    <span class="{risk_cls}">Risk: {ag["risk"]}</span>
                    <span class="badge badge-focus">Focus: {ag["focus"]}</span>
                </div>
                <div class="card-desc">{ag["description"]}</div>
            </div>
            """, unsafe_allow_html=True)

            # Primary orange-pill button
            st.markdown('<div class="primary-action">', unsafe_allow_html=True)
            if st.button("Consult Agent", key=f"btn_{key}"):
                st.session_state.view = "chat"
                st.session_state.active_agent = key
                if key not in st.session_state.messages:
                    st.session_state.messages[key] = []
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('<div class="spacer-sm"></div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)  # close hub-wrap

    st.markdown("""
    <div class="heat-footer">
        <span class="heat-footer-logo">HEAT</span>
        <span class="heat-footer-copy">© 2025 HEAT. All rights reserved.</span>
    </div>
    """, unsafe_allow_html=True)


# ── VIEW: CHAT ────────────────────────────────────────────────────────────────
elif st.session_state.view == "chat":
    key = st.session_state.active_agent or "founder"
    agent = agents.get(key, agents["founder"])

    if key not in st.session_state.messages:
        st.session_state.messages[key] = []

    risk_cls = RISK_BADGE.get(agent["risk"], "badge badge-focus")

    # Agent header
    st.markdown(f"""
    <div class="agent-header">
        <div class="agent-title-row">
            <div class="agent-icon-box">{agent["icon"]}</div>
            <div>
                <div class="agent-name">{agent["name"]}</div>
                <div class="badge-row">
                    <span class="{risk_cls}">Risk: {agent["risk"]}</span>
                    <span class="badge badge-focus">Focus: {agent["focus"]}</span>
                </div>
            </div>
        </div>
        <div class="agent-desc">{agent["description"]}</div>
    </div>
    <div class="agent-divider"></div>
    """, unsafe_allow_html=True)

    # Back button — ghost/secondary, minimal
    st.markdown('<div style="max-width:900px;margin:0 auto;padding:0 40px 12px 40px;">', unsafe_allow_html=True)
    st.markdown('<div class="back-btn-wrap">', unsafe_allow_html=True)
    _, back_col, __ = st.columns([0.01, 0.18, 0.81])
    with back_col:
        if st.button("← All Agents", key="back_btn"):
            st.session_state.view = "hub"
            st.rerun()
    st.markdown('</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="spacer-sm"></div>', unsafe_allow_html=True)

    # Chat history
    for msg in st.session_state.messages[key]:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # Single chat input
    user_input = st.chat_input(f"Ask {agent['name']} anything…")

    if user_input:
        st.session_state.messages[key].append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)

        with st.chat_message("assistant"):
            with st.spinner(""):
                response = get_response(agent["prompt"], user_input)
            if response:
                st.write(response)
                st.session_state.messages[key].append({"role": "assistant", "content": response})

    # Footer
    st.markdown("""
    <div class="heat-footer">
        <span class="heat-footer-logo">HEAT</span>
        <a href="https://bhy476x6le.c36.airoapp.ai/" target="_blank" class="heat-footer-link">← Back to HEAT website</a>
    </div>
    """, unsafe_allow_html=True)