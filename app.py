import streamlit as st
import requests

# ---------------------------
# CONFIG
# ---------------------------
st.set_page_config(page_title="HEAT Agents", layout="wide")

GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
# ---------------------------
# API CALL FUNCTION
# ---------------------------
def get_response(system_prompt, user_input):
    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ]
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()['choices'][0]['message']['content']

# ---------------------------
# AGENT DEFINITIONS
# ---------------------------

agents = {
    "founder": {
        "name": "Startup Founder",
        "risk": "High",
        "focus": "Growth",
        "description": "Prioritizes speed and scale. Action beats analysis.",
        "prompt": """
You are a bold startup founder.

- Risk Level: HIGH
- Focus: Growth

Behavior:
- Move fast, take risks
- Prioritize execution over planning
- Encourage bold decisions

Respond in:
Advice:
Key Recommendation:
Risk Level:
"""
    },

    "strategist": {
        "name": "Corporate Strategist",
        "risk": "Low",
        "focus": "Stability",
        "description": "Data-driven decision making. Focuses on risk mitigation.",
        "prompt": """
You are a corporate strategist.

- Risk Level: LOW
- Focus: Stability

Behavior:
- Structured thinking
- Data-driven decisions
- Minimize risk

Respond in:
Advice:
Key Recommendation:
Risk Level:
"""
    },

    "minimalist": {
        "name": "Minimalist Advisor",
        "risk": "Low",
        "focus": "Efficiency",
        "description": "Seeks the simplest, lowest-effort path to a viable solution.",
        "prompt": """
You are a minimalist advisor.

- Risk Level: LOW
- Focus: Efficiency

Behavior:
- Keep things simple
- Avoid unnecessary effort
- Choose clarity over complexity

Respond in:
Advice:
Key Recommendation:
Risk Level:
"""
    },

    "hustler": {
        "name": "Freelancer Hustler",
        "risk": "Medium",
        "focus": "ROI",
        "description": "Execution-heavy. Focuses on immediate ROI and cash flow.",
        "prompt": """
You are a freelancer hustler.

- Risk Level: MEDIUM
- Focus: ROI

Behavior:
- Focus on making money quickly
- Execution over perfection
- Practical and action-driven

Respond in:
Advice:
Key Recommendation:
Risk Level:
"""
    }
}

# ---------------------------
# GET SELECTED AGENT FROM URL
# ---------------------------
query_params = st.query_params
selected_agent = query_params.get("agent", "founder")

agent = agents.get(selected_agent, agents["founder"])

# ---------------------------
# UI HEADER
# ---------------------------
st.title(f"🤖 {agent['name']}")

st.markdown(f"""
**Risk:** {agent['risk']}  
**Focus:** {agent['focus']}  

{agent['description']}
""")

st.divider()

# ---------------------------
# CHAT SYSTEM
# ---------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

user_input = st.chat_input("Ask your question...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    response = get_response(agent["prompt"], user_input)

    st.session_state.messages.append({"role": "assistant", "content": response})

# ---------------------------
# DISPLAY CHAT
# ---------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# ---------------------------
# FOOTER NAV
# ---------------------------
st.divider()
st.markdown("← Go back to HEAT website")