import streamlit as st
import requests

st.set_page_config(page_title="HEAT Agents", layout="wide", initial_sidebar_state="collapsed")

GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

# ── HEAT Design System ────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Import Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

/* ── Reset & Base ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

:root {
    --bg:        #0d0d0d;
    --surface:   #161616;
    --surface2:  #1e1e1e;
    --border:    #2a2a2a;
    --orange:    #ff6600;
    --orange-dim:#7a3100;
    --white:     #ffffff;
    --grey:      #888888;
    --grey-light:#bbbbbb;
    --red-dim:   #3d1a1a;
    --red-text:  #ff4444;
    --green-dim: #0f2a1a;
    --green-text:#33cc77;
    --yellow-dim:#2a1f00;
    --yellow-text:#e8a020;
}

/* ── Hide Streamlit Chrome ── */
#MainMenu, footer, header,
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"],
.viewerBadge_container__1QSob,
.stDeployButton { display: none !important; }

/* ── Page Background ── */
.stApp, [data-testid="stAppViewContainer"] {
    background: var(--bg) !important;
    font-family: 'DM Sans', sans-serif;
    color: var(--white);
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
    padding: 0 48px;
    height: 60px;
    background: var(--bg);
    border-bottom: 1px solid var(--border);
    position: sticky;
    top: 0;
    z-index: 999;
}
.heat-nav-logo {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 18px;
    letter-spacing: 0.12em;
    color: var(--white);
    text-decoration: none;
}
.heat-nav-links {
    display: flex;
    align-items: center;
    gap: 32px;
}
.heat-nav-links a {
    font-family: 'DM Sans', sans-serif;
    font-size: 14px;
    font-weight: 400;
    color: var(--grey-light);
    text-decoration: none;
    transition: color 0.2s;
}
.heat-nav-links a:hover, .heat-nav-links a.active { color: var(--white); }
.heat-nav-btn {
    border: 1px solid var(--border) !important;
    border-radius: 20px !important;
    padding: 6px 18px !important;
    color: var(--white) !important;
    background: transparent !important;
    font-size: 13px !important;
}

/* ── AGENT VIEW HEADER ── */
.agent-header {
    padding: 40px 48px 0 48px;
}
.agent-back-link {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-size: 13px;
    color: var(--grey);
    text-decoration: none;
    margin-bottom: 28px;
    transition: color 0.2s;
}
.agent-back-link:hover { color: var(--orange); }
.agent-title-row {
    display: flex;
    align-items: flex-start;
    gap: 20px;
    margin-bottom: 16px;
}
.agent-icon-box {
    width: 56px;
    height: 56px;
    border-radius: 12px;
    background: var(--surface2);
    border: 1px solid var(--border);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 22px;
    flex-shrink: 0;
}
.agent-name {
    font-family: 'Syne', sans-serif;
    font-size: 28px;
    font-weight: 700;
    color: var(--white);
    line-height: 1.2;
    margin-bottom: 10px;
}
.badge-row { display: flex; gap: 8px; flex-wrap: wrap; }
.badge {
    font-size: 12px;
    font-weight: 500;
    padding: 4px 12px;
    border-radius: 20px;
    border: 1px solid;
}
.badge-high   { background: var(--red-dim);    color: var(--red-text);    border-color: var(--red-text); }
.badge-medium { background: var(--yellow-dim); color: var(--yellow-text); border-color: var(--yellow-text); }
.badge-low    { background: var(--green-dim);  color: var(--green-text);  border-color: var(--green-text); }
.badge-focus  { background: var(--surface2);   color: var(--grey-light);  border-color: var(--border); }
.agent-desc {
    font-size: 14px;
    color: var(--grey-light);
    margin-top: 12px;
    max-width: 560px;
    line-height: 1.6;
}
.agent-divider {
    height: 1px;
    background: var(--border);
    margin: 28px 48px;
}

/* ── CHAT AREA ── */
.chat-wrapper {
    padding: 0 48px;
    max-width: 900px;
}

/* Style Streamlit chat messages */
[data-testid="stChatMessage"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    margin-bottom: 12px !important;
    padding: 16px !important;
}
[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] div {
    color: var(--white) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 14px !important;
    line-height: 1.7 !important;
}

/* Chat input */
[data-testid="stChatInput"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
}
[data-testid="stChatInput"] textarea {
    color: var(--white) !important;
    font-family: 'DM Sans', sans-serif !important;
    background: transparent !important;
}
[data-testid="stChatInputSubmitButton"] svg { fill: var(--orange) !important; }

/* ── DASHBOARD (Hub) ── */
.hub-header {
    padding: 56px 48px 0 48px;
    text-align: center;
}
.hub-eyebrow {
    font-family: 'Syne', sans-serif;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.18em;
    color: var(--orange);
    text-transform: uppercase;
    margin-bottom: 16px;
}
.hub-title {
    font-family: 'Syne', sans-serif;
    font-size: 46px;
    font-weight: 800;
    color: var(--white);
    line-height: 1.1;
    margin-bottom: 14px;
}
.hub-subtitle {
    font-size: 16px;
    color: var(--grey-light);
    max-width: 480px;
    margin: 0 auto;
    line-height: 1.6;
}
.hub-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 20px;
    padding: 48px 48px 48px 48px;
    max-width: 1100px;
    margin: 0 auto;
}
.agent-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 28px;
    transition: border-color 0.25s, transform 0.25s, box-shadow 0.25s;
    cursor: pointer;
}
.agent-card:hover {
    border-color: var(--orange-dim);
    transform: translateY(-2px);
    box-shadow: 0 8px 32px rgba(255,102,0,0.08);
}
.card-icon {
    width: 52px;
    height: 52px;
    border-radius: 10px;
    background: var(--surface2);
    border: 1px solid var(--border);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
    margin-bottom: 18px;
}
.card-name {
    font-family: 'Syne', sans-serif;
    font-size: 20px;
    font-weight: 700;
    color: var(--white);
    margin-bottom: 12px;
}
.card-desc {
    font-size: 13px;
    color: var(--grey-light);
    line-height: 1.6;
    margin: 14px 0 20px 0;
    min-height: 40px;
}

/* ── Streamlit Button Overrides ── */
.stButton > button {
    width: 100% !important;
    background: transparent !important;
    color: var(--white) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    padding: 12px 20px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    letter-spacing: 0.02em !important;
    cursor: pointer !important;
    transition: background 0.2s, border-color 0.2s, color 0.2s !important;
}
.stButton > button:hover {
    background: var(--surface2) !important;
    border-color: var(--orange) !important;
    color: var(--white) !important;
}
.stButton > button:focus { box-shadow: none !important; outline: none !important; }

/* ── FOOTER ── */
.heat-footer {
    border-top: 1px solid var(--border);
    padding: 24px 48px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-top: 40px;
}
.heat-footer-logo {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 15px;
    letter-spacing: 0.12em;
    color: var(--white);
}
.heat-footer-copy {
    font-size: 12px;
    color: var(--grey);
}

/* ── Spinner ── */
[data-testid="stSpinner"] { color: var(--orange) !important; }
[data-testid="stSpinner"] > div { border-top-color: var(--orange) !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--grey); }
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
    st.markdown("""
    <div class="hub-header">
        <div class="hub-eyebrow">MARKETPLACE</div>
        <div class="hub-title">The Marketplace of Minds</div>
        <div class="hub-subtitle">Consult AI agents built from real human expertise. Each one thinks differently.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="hub-grid">', unsafe_allow_html=True)
    cols = st.columns(2, gap="medium")

    agent_keys = list(agents.keys())
    for i, key in enumerate(agent_keys):
        ag = agents[key]
        risk_cls = RISK_BADGE.get(ag["risk"], "badge badge-focus")
        col = cols[i % 2]

        with col:
            # Card HTML (non-interactive portion)
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

            # Streamlit button (overlaid below card visually)
            if st.button("Consult Agent", key=f"btn_{key}"):
                st.session_state.view = "chat"
                st.session_state.active_agent = key
                if key not in st.session_state.messages:
                    st.session_state.messages[key] = []
                st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

    # Footer
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

    # Header
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

    # Back button
    left_col, _ = st.columns([1, 8])
    with left_col:
        if st.button("← All Agents", key="back_btn"):
            st.session_state.view = "hub"
            st.rerun()

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    # Chat history
    for msg in st.session_state.messages[key]:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # Chat input
    user_input = st.chat_input(f"Ask {agent['name']} anything...")

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

    # Footer
    st.markdown("""
    <div class="heat-footer">
        <span class="heat-footer-logo">HEAT</span>
        <a href="https://bhy476x6le.c36.airoapp.ai/" target="_blank" style="font-size:12px;color:#888;text-decoration:none;">← Back to HEAT website</a>
    </div>
    """, unsafe_allow_html=True)