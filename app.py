import streamlit as st
from llm_chain import ask_fedex_bot
from login_ui import login_signup_ui
from tracking import track_shipment
import re

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="FedEx AI Assistant",
    page_icon="📦",
    layout="wide"
)

# ==========================================
# LOGIN CHECK
# ==========================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:

    login_signup_ui()

    st.stop()

# ==========================================
# SESSION STATE
# ==========================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "otp" not in st.session_state:
    st.session_state.otp = None

if "otp_verified" not in st.session_state:
    st.session_state.otp_verified = False

# ==========================================
# QUICK TOPICS
# ==========================================

quick_topics = [
    "How tracking system works in FedEx",
    "What happens if delivery fails?",
    "Can I change delivery address after shipping?",
    "International shipping rules",
    "Refund policy in FedEx",
    "Prohibited items in FedEx",
    "How reverse logistics works?",
    "Privacy and data protection",
]

# ==========================================
# CUSTOM CSS
# ==========================================

st.markdown("""
<style>

html, body, [class*="css"] {
    font-family: 'Segoe UI', sans-serif;
    background: #020617;
    color: white;
}

/* MAIN */
.main {
    background: linear-gradient(to bottom, #020617, #000814);
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background: #050816;
    width: 320px !important;
    border-right: 1px solid rgba(255,255,255,0.08);
}

/* FIX SIDEBAR */
.sidebar-fixed {
    position: fixed;
    top: 0;
    left: 0;
    width: 300px;
    height: 100vh;
    overflow-y: auto;
    padding: 20px;
}

/* TITLE */
.title-text {
    font-size: 58px;
    font-weight: 800;
    color: white;
    margin-bottom: 0px;
}

.subtitle {
    color: #cbd5e1;
    font-size: 22px;
    margin-top: -10px;
    margin-bottom: 30px;
}

/* CHAT CONTAINER */
.chat-container {
    max-height: 70vh;
    overflow-y: auto;
    padding-right: 10px;
}

/* USER MESSAGE */
.user-msg {
    display: flex;
    justify-content: flex-end;
    margin: 18px 0;
}

.user-bubble {
    background: linear-gradient(135deg, #6d28d9, #c026d3);
    color: white;
    padding: 16px 22px;
    border-radius: 22px;
    max-width: 70%;
    font-size: 18px;
    box-shadow: 0px 0px 20px rgba(168,85,247,0.35);
}

/* BOT MESSAGE */
.bot-msg {
    display: flex;
    justify-content: flex-start;
    margin: 18px 0;
}

.bot-bubble {
    background: rgba(15,23,42,0.95);
    border: 1px solid rgba(255,255,255,0.06);
    color: white;
    padding: 18px 24px;
    border-radius: 22px;
    max-width: 78%;
    font-size: 18px;
    line-height: 1.7;
    box-shadow: 0px 0px 18px rgba(0,0,0,0.4);
}

/* INPUT */
.stTextInput input {
    background: #0f172a !important;
    border: 1px solid #7c3aed !important;
    color: white !important;
    border-radius: 16px !important;
    height: 58px !important;
    font-size: 18px !important;
}

/* BUTTON */
.stButton button {
    width: 100%;
    border-radius: 14px;
    background: linear-gradient(135deg, #6d28d9, #c026d3);
    color: white;
    border: none;
    height: 52px;
    font-size: 17px;
    font-weight: 600;
}

/* TOPIC BUTTONS */
.topic-btn {
    background: rgba(255,255,255,0.05);
    padding: 16px;
    border-radius: 16px;
    margin-bottom: 12px;
    border: 1px solid rgba(255,255,255,0.08);
}

.topic-title {
    color: white;
    font-size: 16px;
    font-weight: 600;
}

/* SCROLLBAR */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-thumb {
    background: #7c3aed;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:

    st.markdown("""
    <div class="sidebar-fixed">
    """, unsafe_allow_html=True)

    st.markdown("""
    <h1 style='font-size:58px;
               font-weight:900;
               background: linear-gradient(to right,#7c3aed,#ec4899);
               -webkit-background-clip:text;
               -webkit-text-fill-color:transparent;'>
    FedEx
    </h1>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="
    background: rgba(255,255,255,0.04);
    padding:22px;
    border-radius:18px;
    margin-top:20px;
    border:1px solid rgba(255,255,255,0.05);
    ">
    <h2 style='color:white;'>🤖 AI Assistant</h2>
    <p style='color:#cbd5e1;font-size:18px;line-height:1.7;'>
    Your smart FedEx support companion.
    </p>
    </div>
    """, unsafe_allow_html=True)

    st.write("")
    st.write("")

    st.markdown("## ⚡ Quick Topics")

    for topic in quick_topics:

        if st.button(topic):

            # TRACKING MODE
            if topic.startswith("track shipment"):

                answer = track_shipment(topic)

            else:

                answer = ask_fedex_bot(topic)

            st.session_state.messages.append(
                {"role": "user", "content": topic}
            )

            st.session_state.messages.append(
                {"role": "assistant", "content": answer}
            )

    st.markdown("</div>", unsafe_allow_html=True)

    st.write("")
    st.write("")
    if st.button("🚪 Logout"):
        
        st.session_state.logged_in = False
        
        if "username" in st.session_state:
            st.session_state.username = ""
            
            st.rerun()
# ==========================================
# MAIN TITLE
# ==========================================

st.markdown("""
<div class="title-text">
🤖 FedEx AI Assistant
</div>

<div class="subtitle">
Ask anything about FedEx tracking, delivery, refunds, shipping and logistics.
</div>
""", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# ==========================================
# CHAT AREA
# ==========================================

st.markdown('<div class="chat-container">', unsafe_allow_html=True)

for msg in st.session_state.messages:

    if msg["role"] == "user":

        st.markdown(f"""
        <div class="user-msg">
            <div class="user-bubble">
                {msg["content"]}
            </div>
        </div>
        """, unsafe_allow_html=True)

    else:

        clean_answer = str(msg["content"]).replace("\n", "<br>")

        st.markdown(f"""
        <div class="bot-msg">
            <div class="bot-bubble">
                {clean_answer}
            </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)


# ==========================================
# OTP VERIFICATION
# ==========================================

if st.session_state.otp:

    st.markdown("### 🔐 OTP Verification")

    user_otp = st.text_input(
        "Enter OTP",
        key="otp_input"
    )

    if st.button("Verify OTP"):

        if user_otp == st.session_state.otp:

            st.success("✅ OTP Verified Successfully")

            st.session_state.otp_verified = True

            st.session_state.otp = None

        else:

            st.error("❌ Invalid OTP")

# ==========================================
# INPUT
# ==========================================

query = st.text_input(
    "",
    placeholder="Ask your FedEx question here..."
)

# ==========================================
# ASK BUTTON
# ==========================================

# ==========================================
# ASK BUTTON
# ==========================================

if st.button("🚀 Ask AI"):

    if query:

        # USER MESSAGE
        st.session_state.messages.append({
            "role": "user",
            "content": query
        })

        # ======================================
        # TRACKING DETECTION
        # ======================================

        tracking_match = re.search(
            r"(FDX[A-Z0-9]+)",
            query.upper()
        )

        if tracking_match:

            tracking_number = tracking_match.group(1)

            result = track_shipment(tracking_number)
            
            if isinstance(result, dict):
                st.session_state.otp = result["otp"]
                answer = result["message"]
                
            else:
                
                answer = result

        # ======================================
        # NORMAL RAG CHAT
        # ======================================

        else:

            answer = ask_fedex_bot(query)

        # ASSISTANT MESSAGE
        st.session_state.messages.append({
            "role": "assistant",
            "content": answer
        })

        st.rerun()