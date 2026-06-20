import streamlit as st
from llm_chain import ask_fedex_bot
from login_ui import login_signup_ui
from tracking import track_shipment
from shipment_booking import shipment_booking_ui
import database
import re
from streamlit_mic_recorder import speech_to_text

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
# PAGE NAVIGATION
# ==========================================

if "page" not in st.session_state:
    st.session_state.page = "🤖 AI Assistant"

# ==========================================
# SESSION STATE
# ==========================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "otp" not in st.session_state:
    st.session_state.otp = None

if "otp_verified" not in st.session_state:
    st.session_state.otp_verified = False

# custom css 

st.markdown("""
<style>

html, body, [class*="css"] {
    font-family: 'Segoe UI', sans-serif;
}

/* MAIN PAGE */

.main {
    background: #020617;
}

/* SIDEBAR */

section[data-testid="stSidebar"] {
    background: #050816;
}

/* TITLE */

.title-text {
    font-size: 58px;
    font-weight: 800;
    color: white;
}

.subtitle {
    color: #cbd5e1;
    font-size: 22px;
}

/* ALL BUTTONS */

.stButton > button {

    width: 100% !important;
    height: 50px !important;

    border-radius: 6px !important;

    background: linear-gradient(
        135deg,
        #6d28d9,
        #c026d3
    ) !important;

    color: white !important;

    border: none !important;

    font-size: 16px !important;

    font-weight: 600 !important;

    transition: 0.3s ease !important;
}

/* BUTTON HOVER */

.stButton > button:hover {

    transform: translateY(-2px);

    box-shadow: 0px 6px 20px
    rgba(124,58,237,0.4);
}

/* CHAT INPUT FIXED AT BOTTOM */

[data-testid="stChatInput"] {

    position: fixed !important;

    bottom: 15px !important;

    left: 340px !important;

    right: 20px !important;

    z-index: 9999 !important;

    background: white !important;
}

/* CHAT INPUT BOX */

[data-testid="stChatInput"] textarea {

    border-radius: 12px !important;
}

/* SUCCESS MESSAGE */

[data-testid="stAlert"] {

    border-radius: 10px !important;
}

/* METRICS */

[data-testid="metric-container"] {

    border-radius: 12px !important;

    padding: 15px !important;

    border: 1px solid
    rgba(255,255,255,0.08);
}

/* SCROLLBAR */

::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-thumb {

    background: #7c3aed;

    border-radius: 10px;
}

/* REMOVE ROUNDED SECONDARY BUTTONS */

button[kind="secondary"] {

    border-radius: 6px !important;
}

</style>
""", unsafe_allow_html=True)
# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:

    st.markdown("""
    <h1 style='font-size:58px;
               font-weight:900;
               background:linear-gradient(
                   to right,
                   #7c3aed,
                   #ec4899
               );
               -webkit-background-clip:text;
               -webkit-text-fill-color:transparent;'>
    FedEx
    </h1>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="
    background:rgba(255,255,255,0.04);
    padding:20px;
    border-radius:15px;
    margin-bottom:20px;
    ">
    <h3>🤖 AI Assistant</h3>
    <p>
    Your smart FedEx support companion.
    </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("## 📋 Navigation")

    if st.button(
        "🤖 AI Assistant",
        use_container_width=True
    ):
        st.session_state.page = "🤖 AI Assistant"
        st.rerun()

    if st.button(
        "📦 Shipment Booking",
        use_container_width=True
    ):
        st.session_state.page = "📦 Shipment Booking"
        st.rerun()

    st.markdown("---")

    if st.button(
        "🚪 Logout",
        use_container_width=True
    ):

        st.session_state.logged_in = False

        if "username" in st.session_state:
            del st.session_state["username"]

        st.rerun()

# ==========================================
# SHIPMENT BOOKING PAGE
# ==========================================

if st.session_state.page == "📦 Shipment Booking":

    shipment_booking_ui()

    st.stop()

# ==========================================
# MAIN TITLE
# ==========================================

st.markdown("""
<div class="title-text">
🤖 FedEx AI Assistant
</div>

<div class="subtitle">
Ask anything about FedEx tracking,
delivery, refunds, shipping and logistics.
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ==========================================
# CHAT AREA
# ==========================================

for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):

        st.markdown(msg["content"])

# ==========================================
# SPACING FOR FIXED CHAT INPUT
# ==========================================

st.markdown(
    "<div style='height:120px'></div>",
    unsafe_allow_html=True
)

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

            st.success(
                "✅ OTP Verified Successfully"
            )

            st.session_state.otp_verified = True

            st.session_state.otp = None

            st.rerun()

        else:

            st.error(
                "❌ Invalid OTP"
            )
# ==========================================
# CHAT INPUT + MIC
# ==========================================

col1, col2 = st.columns([9, 1])

with col1:

    query = st.chat_input(
        "Ask anything about FedEx..."
    )

with col2:

    voice_text = speech_to_text(
        language="en",
        start_prompt="🎙️",
        stop_prompt="⏹️",
        just_once=True,
        key="fedex_mic"
    )

if voice_text:
    query = voice_text

if query:

    st.session_state.messages.append({
        "role": "user",
        "content": query
    })

    tracking_match = re.search(
        r"(FDX[A-Z0-9]+)",
        query.upper()
    )

    if tracking_match:

        tracking_number = tracking_match.group(1)

        result = track_shipment(
            tracking_number
        )

        if isinstance(result, dict):

            st.session_state.otp = result["otp"]

            answer = result["message"]

        else:

            answer = result

    else:

        with st.spinner(
            "🤖 FedAssist is thinking..."
        ):

            answer = ask_fedex_bot(query)

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })

    st.rerun()
if query:

    # ======================================
    # USER MESSAGE
    # ======================================

    st.session_state.messages.append({
        "role": "user",
        "content": query
    })

    # ======================================
    # TRACKING NUMBER DETECTION
    # ======================================

    tracking_match = re.search(
        r"(FDX[A-Z0-9]+)",
        query.upper()
    )

    if tracking_match:

        tracking_number = (
            tracking_match.group(1)
        )

        result = track_shipment(
            tracking_number
        )

        if isinstance(result, dict):

            st.session_state.otp = (
                result["otp"]
            )

            answer = (
                result["message"]
            )

        else:

            answer = result

    # ======================================
    # NORMAL AI CHAT
    # ======================================

    else:

        with st.spinner(
            "🤖 FedAssist is thinking..."
        ):

            answer = ask_fedex_bot(
                query
            )

    # ======================================
    # ASSISTANT MESSAGE
    # ======================================

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })

    st.rerun()