import streamlit as st
import requests

st.set_page_config(page_title="HEAT Agents", layout="wide")

GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

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
        "risk": "High",
        "focus": "Growth",
        "description": "Prioritizes speed and scale. Action beats analysis.",
        "prompt": """You are a bold startup founder.\n- Risk Level: HIGH\n- Focus: Growth\nBehavior:\n- Move fast, take risks\n- Prioritize execution over planning\n- Encourage bold decisions\n\nRespond in:\nAdvice:\nKey Recommendation:\nRisk Level:"""
    },
    "strategist": {
        "name": "Corporate Strategist",
        "risk": "Low",
        "focus": "Stability",
        "description": "Data-driven decision making. Focuses on risk mitigation.",
        "prompt": """You are a corporate strategist.\n- Risk Level: LOW\n- Focus: Stability\nBehavior:\n- Structured thinking\n- Data-driven decisions\n- Minimize risk\n\nRespond in:\nAdvice:\nKey Recommendation:\nRisk Level:"""
    },
    "minimalist": {
        "name": "Minimalist Advisor",
        "risk": "Low",
        "focus": "Efficiency",
        "description": "Seeks the simplest, lowest-effort path to a viable solution.",
        "prompt": """You are a minimalist advisor.\n- Risk Level: LOW\n- Focus: Efficiency\nBehavior:\n- Keep things simple\n- Avoid unnecessary effort\n- Choose clarity over complexity\n\nRespond in:\nAdvice:\nKey Recommendation:\nRisk Level:"""
    },
    "hustler": {
        "name": "Freelancer Hustler",
        "risk": "Medium",
        "focus": "ROI",
        "description": "Execution-heavy. Focuses on immediate ROI and cash flow.",
        "prompt": """You are a freelancer hustler.\n- Risk Level: MEDIUM\n- Focus: ROI\nBehavior:\n- Focus on making money quickly\n- Execution over perfection\n- Practical and action-driven\n\nRespond in:\nAdvice:\nKey Recommendation:\nRisk Level:"""
    }
}

query_params = st.query_params
selected_agent = query_params.get("agent", "founder")
agent = agents.get(selected_agent, agents["founder"])

st.title(f"🤖 {agent['name']}")
st.markdown(f"**Risk:** {agent['risk']}  \n**Focus:** {agent['focus']}  \n\n{agent['description']}")
st.divider()

if "messages" not in st.session_state:
    st.session_state.messages = []

# ✅ Display existing chat history FIRST
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# ✅ Then define and handle user input
user_input = st.chat_input("Ask your question...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = get_response(agent["prompt"], user_input)
        if response:
            st.write(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

st.divider()
st.markdown("← [Go back to HEAT website](https://bhy476x6le.c36.airoapp.ai/)")